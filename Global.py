import json

class TenObj():
    """万物父类
        """
    def __init__(self):
        self.szAppName = '' # APP名称
        self.szObjName = ''# 模块名称
        self.szAuthor = 'LHJ' # 作者
        self.szCreateTime = '2018-5-12'
        self.szLastUpdate = '' # 最后一次更新时间
        self.aUpdateNotes = [] # 更新历史
        self.pStatus = {} # 状态
    def _DoLog(self, szLog):
        """ 日志
            Args:
                szLog: 日志内容
            Returns:
                True or False
            """
        return True
    def _DoPackageStatus(self):
        """ 组装状态
            Args:
                szLog: 日志内容
            Returns:
                True or False
            """
        pass

class CmdService(TenObj):
    """应用内命令中转服务
        """
    def __init__(self):
        super().__init__()
        # 命令路由器
        self.pCmdRouter = {}

    async def ParseCmd(self, szData):
        try:
            pData = json.loads(szData)
            pTenDataRcvd = TenDataRcvd()
            for item, value in pData.items():
                funcName = 'Set' + item
                if hasattr(pTenDataRcvd, funcName):
                    (getattr(pTenDataRcvd, funcName))(value)
            return await self.Router(pTenDataRcvd)
        except:
            # import traceback
            # traceback.print_exc()
            pass

    async def Router(self, pTenDataRcvd):
        '''SPEC BEGIN
            Router = 路由
        END
        '''
        cmd = pTenDataRcvd.GetCmd()
        if not cmd in self.pCmdRouter:
            return await self.pCmdRouter['Other'](pTenDataRcvd)
        try:
            return await self.pCmdRouter[cmd](pTenDataRcvd)
        except:
            return ''

    def AddRouter(self, szCmd, pFunction):
        '''SPEC BEGIN
            AddRouter = 添加路由
        END
        '''
        if szCmd == '' or szCmd == None:
            return
        self.pCmdRouter[szCmd] = pFunction

class TenData():
    def __init__(self):
        self.Ver = '1'
        self.Fmt = 'json'
        self.Data = {}
    def SetVer(self, szVer):
        """ 设置版本号
            Args:
                szVer: 版本号
            Returns:
            """
        self.Ver = szVer
    def GetVer(self):
        return self.Ver
    def SetFmt(self, szFmt):
        self.Fmt = szFmt
    def GetFmt(self):
        return self.Fmt
    def SetData(self, data):
        self.Data = data
    def GetData(self):
        return self.Data
    def Get(self):
        return self._DoGet()
    def _DoGet(self):
        return {
            'Ver': self.Ver,
            'Fmt': self.Fmt,
            'Data': self.Data
        }
class TenDataRcvd(TenData):
    def __init__(self):
        super().__init__()
        self.App = ''
        self.Cmd = ''
        self.Route = ''
        self.UserData = {}
    def _DoGet(self):
        tmp = super()._DoGet()
        p = {
            'App': self.App,
            'Cmd': self.Cmd,
            'Route': self.Route,
            'UserData': self.UserData
        }
        p.update(tmp)
        return p

    def SetApp(self, szApp):
        self.App = szApp
    def GetApp(self):
        return self.App
    def SetCmd(self, szCmd):
        self.Cmd = szCmd
    def GetCmd(self):
        return self.Cmd
    def SetRoute(self, szRoute):
        self.Route = szRoute
    def GetRoute(self):
        return self.Route

class TenDataSend(TenData):
    def __init__(self):
        super().__init__()
        self.Hints = ''
        self.Result = '1'
        self.ErrCode = '0'
    def _DoGet(self):
        tmp = super()._DoGet()
        p = {
            'Hints': self.Hints,
            'Result': self.Result,
            'ErrCode': self.ErrCode
        }
        p.update(tmp)
        return p

    def SetHints(self, szHints):
        self.Hints = szHints
    def GetHints(self):
        return self.Hints
    def SetResult(self, szResult):
        self.Result = szResult
    def SetTrue(self):
        self.Result = '1'
    def SetFalse(self):
        self.Result = '0'
    def IsTrue(self):
        if self.Result == '1':
            return True
        return False
    def SetErrCode(self, szErrCode):
        self.ErrCode = szErrCode
    def GetErrCode(self):
        return self.ErrCode

