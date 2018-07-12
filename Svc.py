import tornado
import asyncio
import json
import tornado.ioloop
import tornado.web
import urllib
import Const

from Db import TenDbConnect
from Db import TenSQL
from Global import TenObj
from Global import TenDataSend
from Db import TenProc
from Db import TenTable


class TenSvc(TenObj):
    """服务基类
        """
    def __init__(self, pCoro=None, iIntv=1000):
        super().__init__()
        self.szSvcName = '' # 服务名
        self.iTotalInt = -1 # 累计间隔时间(毫秒)
        self.iIntv = iIntv # LOOP间隔(毫秒)
        self.isStarted = False # 是否已经启动
        self.IsStopped = False # 是否手动停止
        self.isError = False # 是否出错
        self.isPaused = False # 是否暂停服务
        self.pCoro = pCoro # 协程对象
        self.bDoing = False # 是否正在执行
    async def Run(self, pNow, iTimeLen):
        """ 执行业务逻辑
            Args:
                pNow: 当前时间类
            Returns:
                True or False
            """
        # TODO _DoPackageStatus 组装状态
        if self.iTotalInt != -1 and self.iTotalInt < self.iIntv:
            self.iTotalInt += iTimeLen
            return True

        self.iTotalInt = 0
        return await self._DoRun(pNow)
    async def _DoRun(self, pNow):
        return True

    def Start(self):
        """ 开启服务
            Args:
            Returns:
                True or False
            """
        tmp = self._DoStart()
        if tmp:
            self.isStarted = True
            self.isError = False
            self.IsStopped = False
            self.isPaused = False
    def _DoStart(self):
        return True

    def Stop(self):
        """ 停止服务
            Args:
            Returns:
                True or False
            """
        tmp = self._DoStop()
        if tmp:
            self.isStarted = False
            self.isError = False
            self.IsStopped = True
            self.isPaused = False

    def _DoStop(self):
        return True

    def Pause(self):
        """ 暂停服务
            Args:
            Returns:
                True or False
            """
        if self.isStarted == False:
            return False
        tmp = self._DoPause()
        if tmp:
            self.isStarted = False
            self.isError = False
            self.IsStopped = False
            self.isPaused = True
    def _DoPause(self):
        return True

    def Resume(self):
        """ 恢复服务
            Args:
            Returns:
                True or False
            """
        if self.isStarted:
            return False
        tmp = self._DoResume()
        if tmp:
            self.isStarted = False
            self.isError = False
            self.IsStopped = False
            self.isPaused = True
    def _DoResume(self):
        return True

    def IsRunTime(self):
        """ 是否可以执行Run
            Args:
            Returns:
                True or False
            """
        pass
    def IsRunning(self):
        """ 是否服务正常运行
            Args:
            Returns:
                True or False
            """
        if self.isStarted and self.IsStopped == False and self.isError == False:
            return True
        return False

    def _DoBeat(self):
        """ 发送心跳
            Args:
            Returns:
                True or False
            """
        return True

    def _DoPackageStatus(self):
        """ 组装服务器当前状态
            Args:
            Returns:
                {}
                 example:
                 {
                    'isStarted': True,
                    'isError' : False,
                    'IsStopped': False,
                    'isPaused': False
                 }
            """
        return {
            'isStarted': self.isStarted,
            'isError' : self.isError,
            'IsStopped': self.IsStopped,
            'isPaused': self.isPaused
        }

class CoroSvc(TenObj):
    """协程服务
        """

    def __init__(self, pCallback=None):
        self.pCallback = pCallback  # 回调函数
        self.bStop = True

    """Loop
        """

    async def Loop(self):
        while self.bStop == False:
            self.pCallback()

    def Start(self):
        self.bStop = False
        asyncio.ensure_future(self.Loop())

    def Stop(self):
        self.bStop = True

class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        data = urllib.parse.unquote(self.request.query)
        retData = await self.ReturnData(data)
        self.write(retData)

    async def post(self):
        try:
            data = self.request.body.decode()
            retData = await self.ReturnData(data)
            bData = bytes(retData, encoding="utf8")
            self.write(bData)
        except:
            pass

    async def ReturnData(self, szdata):
        return await self.application.server.Rev(szdata)


class TenHttpSvc(TenSvc):
    """tornado Http服务
        """
    def __init__(self, iIntv=1000, pCoro=None, iPort=0, pCmdRoute=None):
        super().__init__(pCoro, iIntv=iIntv)
        self.iPort = iPort
        self.pCmdRoute = pCmdRoute

    async def Rev(self, szData):
        """ 接收到的HTTP数据
            Args:
                szData: HTTP接收到的信息
            Returns:
            """
        return await self._DoRev(szData)
    async def _DoRev(self, szData):
        return await self.pCmdRoute.ParseCmd(szData)
    def _DoStart(self):
        try:
            app = self.make_app()
            app.server = self
            app.listen(self.iPort)
            return True
        except:
            return False
    def make_app(self):
        return tornado.web.Application([
            (r"/", MainHandler),
        ])
    def AddRouter(self, szCmd, pFunction):
        self.pCmdRoute.AddRouter(szCmd, pFunction)

class TenCoreSvc(TenHttpSvc):
    """路由服务
        """
    def __init__(self, pCoro=None, iPort=0, pCmdRoute=None, iIntv=1000*10, Db=None):
        super().__init__(pCoro=pCoro, iPort=iPort, pCmdRoute=pCmdRoute, iIntv=iIntv)
        self.Db = Db
        # 是否初始化中
        self.bIniting = True

        # 所有App状态
        self.pAppStatus = {}
        # 所有Cmd服务Map
        self.pCmdMap = {}
        # 所有其他服务Map
        self.pSvcMap = {}
        # 版本
        self.pVer = {}

        self.AddRouter('GetCmdSvc', self.GetCmdSvc)
        self.AddRouter('Other', self.Other)

    async def GetCmdSvc(self, pTenDataRcvd):

        ret = TenDataSend()
        # 检测是否初始化完毕
        if self.bIniting:
            ret.SetResult('Initing') # 服务初始化中
            return json.dumps(ret.Get())

        pData = pTenDataRcvd.GetData()
        App = pData['App']

        # 检测是否需要强制升级
        szVersion = pTenDataRcvd.GetVer()
        if self.CheckUpgrade(App, szVersion):
            ret.SetResult('Upgrade')  # 强制升级
            return json.dumps(ret.Get())

        # 检测服务状态
        if App in self.pAppStatus:
            if self.pAppStatus[App] == 2:
                ret.SetResult('Maintain')  # 维护中
                return json.dumps(ret.Get())

        # 获取CmdSvc服务器列表
        data = []
        if App in self.pCmdMap:
            data = self.pCmdMap[App]

        ret.SetData(data)
        return json.dumps(ret.Get())
    async def Other(self, pTenDataRcvd):
        szCmd = pTenDataRcvd.GetCmd()
        if szCmd == 'Login':
            return await self.Login(pTenDataRcvd)
        elif szCmd == 'AddLog':
            return await self.AddLog(pTenDataRcvd)
        pass
    async def Login(self, pTenDataRcvd):
        ret = TenDataSend()
        ret.SetFalse()
        pData = pTenDataRcvd.GetData()
        iType = int(pData['Type'])
        App = pData['App']

        pConnect = TenDbConnect(self.Db)
        b = await pConnect.GetConnect()
        if b == False:
            ret.SetFalse()
            return json.dumps(ret.Get())

        if iType == 0:
            Phone = pData['Phone']
            if len(Phone) > 0:
                Code = pData['Code']
                pProc = TenProc(self.Db, pConnect, 'LoginByCode',
                                aParam=[App, Phone, Code])
                b = await pProc.Proc()
                if b == False:
                    ret.SetFalse()
                else:
                    LoginResult = pProc.GetAppointData('Result')
                    LoginResultData = pProc.ConvertToObj(LoginResult['datas'], LoginResult['cols_name'])
                    if len(LoginResultData) > 0:
                        tmp = LoginResultData[0]
                        if int(tmp['Result']) == 1:
                            ret.SetTrue()
                            szSession = tmp['Session']
                            ret.SetData({
                                'Session': szSession
                            })
                        else:
                            ret.SetFalse()
                            ret.SetHints(tmp['Err'])

            else:
                ret.SetFalse()
                ret.SetHints(u'手机格式不正确')
        else:
            ret.SetFalse()
            ret.SetHints(u'不支持的登录类型')

        await pConnect.Recovery()
        return json.dumps(ret.Get())
    async def AddLog(self, pTenDataRcvd):
        ret = TenDataSend()
        pData = pTenDataRcvd.GetData()
        Type = pData['Type']
        Platform = pData['Platform']
        Log = pData['Log']
        App = pData['App']
        if len(App) <= 0:
            ret.SetFalse()
            ret.SetHints(u'App为空')
            return json.dumps(ret.Get())
        if len(Platform) <= 0:
            ret.SetFalse()
            ret.SetHints(u'Platform为空')
            return json.dumps(ret.Get())

        pConnect = TenDbConnect(self.Db)
        b = await pConnect.GetConnect()
        if b == False:
            ret.SetFalse()
            return json.dumps(ret.Get())
        try:
            pTable = TenTable(self.Db, pConnect, 'Log', szInsertFields='App,Log,LogType',
                              aInsertValue=[[App, Log, Type]])
            b = await pTable.Insert()
            if b == False:
                ret.SetFalse()
        except:
            ret.SetFalse()
            import traceback
            traceback.print_exc()

        await pConnect.Recovery()
        return json.dumps(ret.Get())

    def CheckUpgrade(self, App, szClientVer):
        b = False
        if App in self.pVer:
            All = self.pVer[App]
            for Item in All:
                if szClientVer >= Item['Ver']:
                    continue
                if Item['ForceUpgrade'] == 1:
                    b = True
                    break
        return b
    async def _DoRun(self, pNow):
        if self.bDoing:
            return True
        self.bDoing = True
        # 获取所有APP状态及CmdSvc Map
        await self.GetAllAppAndCmdMap()
        self.bDoing = False
        return True
    async def GetAllAppAndCmdMap(self):
        try:
            # 获取所有Cmd服务IP:Port
            pConnect = TenDbConnect(self.Db)
            b = await pConnect.GetConnect()
            if b == False:
                return
            if b:
                aBatchSql = []
                aBatchSql.append('select App, State, 0 as AppStates from SvcState where SvcStateId >= 0')
                aBatchSql.append('select App, SvcType, Ip, Port, 0 as Cmds from Route where RouteId >= 0')
                aBatchSql.append('select App, Ver, ForceUpgrade, CreateTime, 0 as $ from AppVer where VerId >= 0 order by Ver')

                pTenSQL = TenSQL(self.Db, pConnect, aBatchSql)
                b = await pTenSQL.BatchSql()
                if b:
                    tmpApps = pTenSQL.GetAppointData('AppStates')
                    tmpAppsData = pTenSQL.ConvertToObj(tmpApps['datas'], tmpApps['cols_name'])
                    tmpCmds = pTenSQL.GetAppointData('Cmds')
                    tmpCmdsData = pTenSQL.ConvertToObj(tmpCmds['datas'], tmpCmds['cols_name'])
                    tmpVer = pTenSQL.GetAppointData('$')
                    tmpVerData = pTenSQL.ConvertToObj(tmpVer['datas'], tmpVer['cols_name'])

                    self.pAppStatus = {}
                    for item in tmpAppsData:
                        self.pAppStatus[item['App']] = int(item['State'])

                    self.pCmdMap = {}
                    for item in tmpCmdsData:
                        App = item['App']
                        SvcType = item['SvcType']
                        if SvcType == 'CmdSvc':
                            if not App in self.pCmdMap:
                                self.pCmdMap[App] = []
                            p = self.pCmdMap[App]
                            p.append({
                                'App': App,
                                'SvcType': item['SvcType'],
                                'Ip': item['Ip'],
                                'Port': item['Port'],
                            })
                        else:
                            if not App in self.pSvcMap:
                                self.pSvcMap[App] = {}
                            p = self.pSvcMap[App]
                            if not SvcType in p:
                                p[SvcType] = []
                            p = p[SvcType]
                            p.append({
                                'App': App,
                                'SvcType': item['SvcType'],
                                'Ip': item['Ip'],
                                'Port': item['Port'],
                            })


                    self.pVer = {}
                    for item in tmpVerData:
                        App = item['App']
                        if not App in self.pVer:
                            self.pVer[App] = []
                        p = self.pVer[App]
                        p.append({
                            'CreateTime': item['CreateTime'],
                            'ForceUpgrade' : int(item['ForceUpgrade']),
                            'Ver' : item['Ver']
                        })
                    self.bIniting = False

                else:
                    self.iTotalInt = self.iIntv
            pass
        except:
            pass
        await pConnect.Recovery()

    def Delivery(pTenDataRcvd):
        pass