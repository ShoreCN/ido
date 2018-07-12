import time
import json
import datetime
import random
import Const
import uuid
import re
import copy
# from operator import itemgetter

from Db import TenTable
from Db import TenProc
from Db import TenSQL
from Db import TenDbConnect
from Global import TenObj
from Svc import TenHttpSvc
from Global import TenDataSend
import Lib.Http as Http

class WfObj(TenObj):
    def __init__(self, szWFID='', szText=''):
        self.szWFID = szWFID
        self.szText = szText

class WfSvc(TenHttpSvc):
    def __init__(self, pCoro=None, iPort=0, pCmdRoute=None, iIntv=1000*60): # 60000*10
        super().__init__(pCoro=pCoro, iPort=iPort, pCmdRoute=pCmdRoute, iIntv=iIntv)
        self.iLastLoadDate = 0
        self.bDoing = False
        self._Index = {
            'TaskId': 0,
            'ParentId': 1,
            'Txt': 2,
            'Seq': 3,
            'LevelSort': 4,
            'NotTask': 5
        }

        self.pCmds = {
            'TIP': 1,
            'TAG': 1
        }

        # # Temp 临时用户映射
        self.aUser = []
        self.aUser.append({
            'UserId': '1',
            'Address': 'COUx.m8DN4eiVDo',
            'iLastLoadDate': 0
        })
        self.aUser.append({
            'UserId': '2',
            'Address': 'F544.elHcfp6LHO',
            'iLastLoadDate': 0
        })
        self.aUser.append({
            'UserId': '3',
            'Address': 'HOiD.uQ4tNsyedg',
            'iLastLoadDate': 0
        })
        self.aUser.append({
            'UserId': '4',
            'Address': 'HE-f.rr4mC7tkOW',
            'iLastLoadDate': 0
        })

        self.aUser.append({
            'UserId': '5',
            'Address': 'COUx.KrHBWHbvgr',
            'iLastLoadDate': 0
        })
        self.aUser.append({
            'UserId': '6',
            'Address': 'IJ3x.TjiOiGTg4m',
            'iLastLoadDate': 0
        })
        self.aUser.append({
            'UserId': '7',
            'Address': 'HpHr.SmQgALXLQs',
            'iLastLoadDate': 0
        })

        self.AddRouter('GetTasks', self.GetTasks)
        self.AddRouter('Test', self.Test)
        self.AddRouter('ReTasks', self.ReTasks)

        self.AddRouter('ModifyTasks', self.ModifyTasks)
        self.AddRouter('GetDialog', self.GetDialog)
        self.AddRouter('GetFriends', self.GetFriends)

    async def Test(self, pTenDataRcvd):
        pConnect = TenDbConnect(Const.g_pTenMySqlObj)
        b = await pConnect.GetConnect()
        # b = await pConnect.Begin()
        pTable = TenTable(Const.g_pTenMySqlObj, pConnect, 'Test', szInsertFields='x',
                          aInsertValue=[[json.dumps(['D', 'M', 'W'])]])

        b = await pTable.Insert()

        # aBatchSql = []
        # aBatchSql.append("INSERT INTO TaskLabel(Rid, Label, TaskId) VALUES ('1', '番茄工作法', 'f7a12288699611e8a6a09cb6d016fb8e')")
        # aBatchSql.append(
        #     "INSERT INTO TaskLabel(Rid, Label, TaskId) VALUES ('1', 'XXX', 'XXXXX')")
        # pTenSQL = TenSQL(Const.g_pTenMySqlObj, pConnect, aBatchSql)
        # b = await pTenSQL.BatchSql()
        # b = await pConnect.Commit()
        iii = 4

    def __Public(self, pProc, ret, tmpDialogData, tmpAllTaskData):
        if pProc.Value != None:

            # 递归算法恢复树形结构
            tD = []
            if len(tmpAllTaskData) > 0:
                tD = tmpAllTaskData[0]['TaskDatas']
                tD = json.loads(tD)
            tD = self.RecoveryTree(tD)

            for item in tmpDialogData:
                item['CreateTime'] = str(item['CreateTime'])
                Txt = item['Txt']
                item['Txt'] = {}
                CurTaskId = item['TaskId']
                for ppItem in tD:
                    ppItem['NotTask'] = str(ppItem['NotTask'])
                    if ppItem['TaskId'] == CurTaskId:
                        item['Txt'] = ppItem
                        break
            ret.SetData(tmpDialogData)

    async def GetDialog(self, pTenDataRcvd):
        ret = TenDataSend()
        pData = pTenDataRcvd.GetData()
        szUserId = pData['Phone']
        iUpdateTime = int(pData['UpdateTime'])
        if szUserId == "":
            ret.SetFalse()
            ret.SetHints(u'Phone不能为空')
        pConnect = TenDbConnect(Const.g_pTenMySqlObj)
        b = await pConnect.GetConnect()
        if b == False:
            ret.SetFalse()
            return json.dumps(ret.Get())
        pProc = TenProc(Const.g_pTenMySqlObj, pConnect, 'GetDialog',
                        aParam=[szUserId, iUpdateTime])
        b = await pProc.Proc()
        if b:
            tmpDialog = pProc.GetAppointData('Dialog')
            tmpDialogData = pProc.ConvertToObj(tmpDialog['datas'], tmpDialog['cols_name'])

            tmpAllTask = pProc.GetAppointData('AllTask')
            tmpAllTaskData = pProc.ConvertToObj(tmpAllTask['datas'], tmpAllTask['cols_name'])

            self.__Public(pProc, ret, tmpDialogData, tmpAllTaskData)
            # if pProc.Value != None:
            #     tmpDialog = pProc.GetAppointData('Dialog')
            #     tmpDialogData = pProc.ConvertToObj(tmpDialog['datas'], tmpDialog['cols_name'])
            #
            #     tmpAllTask = pProc.GetAppointData('AllTask')
            #     tmpAllTaskData = pProc.ConvertToObj(tmpAllTask['datas'], tmpAllTask['cols_name'])
            #     # 递归算法恢复树形结构
            #     tD = []
            #     if len(tmpAllTaskData) > 0:
            #         tD = tmpAllTaskData[0]['TaskDatas']
            #         tD = json.loads(tD)
            #     tD = self.RecoveryTree(tD)
            #
            #     for item in tmpDialogData:
            #         item['CreateTime'] = str(item['CreateTime'])
            #         Txt = item['Txt']
            #         item['Txt'] = {}
            #         CurTaskId = item['TaskId']
            #         for ppItem in tD:
            #             ppItem['NotTask'] = str(ppItem['NotTask'])
            #             if ppItem['TaskId'] == CurTaskId:
            #                 item['Txt'] = ppItem
            #                 break
            #     ret.SetData(tmpDialogData)
            #     iii = 1

                    # if pProc.Value['datas'][0][0] != szVersion:
                    #     pProc = TenProc(Const.g_pTenMySqlObj, pConnect, 'GetTasks', aParam=[szVersion, szUserId])
                    #     data['Data'] = []
                    #     b = await pProc.Proc()
                    #     if b:
                    #         tmpAllTask = pProc.GetAppointData('AllTask')
                    #         tmpAllTaskData = pProc.ConvertToObj(tmpAllTask['datas'], tmpAllTask['cols_name'])
                    #
                    #         tmpLabel = pProc.GetAppointData('AllLabel')
                    #         tmpLabelData = pProc.ConvertToObj(tmpLabel['datas'], tmpLabel['cols_name'])
                    #
                            # tD = []
                            # if len(tmpAllTaskData) > 0:
                            #     tD = tmpAllTaskData[0]['TaskDatas']
                            #     tD = json.loads(tD)
                    #         # 递归算法恢复树形结构
                    #         tD = self.RecoveryTree(tD)
                    #
                    #         ppData = []
                    #         for item in tD:
                    #             pp = {}
                    #             pp['Txt'] = item
                    #             # item['Txt'] = json.loads(item['Txt'])
                    #             Txt = pp['Txt']
                    #             # 将.Tip转为.TIP 并且生成标签
                    #             if 'ch' in Txt:
                    #                 ch = Txt['ch']
                    #                 for tmpItem in ch:
                    #                     nm = tmpItem['nm']
                    #                     nm = nm.strip()
                    #                     if nm.upper() == '.TIP':
                    #                         tmpItem['nm'] = '.TIP'
                    #             # 去除标签
                    #             # Txt['nm'] = self.FilterLabel(Txt['nm'])
                    #             if Correct(Txt) == '':
                    #                 pp['Valid'] = '0'
                    #             else:
                    #                 pp['Valid'] = '1'
                    #
                    #             szTaskId = item['TaskId']
                    #
                    #             self.__AddLabels(pp, tmpLabelData, szTaskId)
                    #             # 3级标签
                    #             if 'ch' in Txt:
                    #                 ch = Txt['ch']
                    #                 for tmpItem in ch:
                    #                     self.__AddLabels(tmpItem, tmpLabelData, tmpItem['TaskId'])
                    #
                    #             # pp['Labels'] = []
                    #             # for label in tmpLabelData:
                    #             #     if label['TaskId'] == szTaskId:
                    #             #         pp['Labels'].append({
                    #             #             'Label': label['Label'],
                    #             #             'Seq': label['Seq']
                    #             #         })
                    #             # 排序
                    #             # item['Labels'] = sorted(item['Labels'], key=itemgetter('Seq'))
                    #             ppData.append(pp)
                    #
                    #         data['Data'] = ppData
                    #     else:
                    #         ret.SetFalse()
                    #
                    #     szVersion = str(pTable.Value['datas'][0][0])
        else:
            ret.SetFalse()

        await pConnect.Recovery()
        return json.dumps(ret.Get())
    async def GetFriends(self, pTenDataRcvd):
        ret = TenDataSend()
        pData = pTenDataRcvd.GetData()
        szUserId = pData['Phone']
        iType = int(pData['Type'])
        szLookRid = pData['LookRid']
        iUpdateTime = int(pData['UpdateTime'])
        if szUserId == "":
            ret.SetFalse()
            ret.SetHints(u'Phone不能为空')
        pConnect = TenDbConnect(Const.g_pTenMySqlObj)
        b = await pConnect.GetConnect()
        if b == False:
            ret.SetFalse()
            return json.dumps(ret.Get())
        aParam = []
        if iType == 1:
            aParam.append(szUserId)
        else:
            aParam.append(szLookRid)
        aParam.append(iType)
        aParam.append(iUpdateTime)
        pProc = TenProc(Const.g_pTenMySqlObj, pConnect, 'GetFriends',
                        aParam=aParam)
        b = await pProc.Proc()
        if b:
            tmpDialog = pProc.GetAppointData('Friends')
            tmpDialogData = pProc.ConvertToObj(tmpDialog['datas'], tmpDialog['cols_name'])

            tmpAllTask = pProc.GetAppointData('AllTask')
            tmpAllTaskData = pProc.ConvertToObj(tmpAllTask['datas'], tmpAllTask['cols_name'])
            self.__Public(pProc, ret, tmpDialogData, tmpAllTaskData)
        else:
            ret.SetFalse()

        await pConnect.Recovery()
        return json.dumps(ret.Get())



    async def ModifyTasks(self, pTenDataRcvd):
        ret = TenDataSend()
        szVersion = pTenDataRcvd.GetVer()
        pData = pTenDataRcvd.GetData()
        szUserId = pData['Phone']
        if szUserId == "":
            ret.SetFalse()
            ret.SetHints(u'Phone不能为空')
        pTaskData = pData['TaskData']
        iType = int(pTaskData['Type'])

        pConnect = TenDbConnect(Const.g_pTenMySqlObj)
        b = await pConnect.GetConnect()
        if b == False:
            ret.SetFalse()
            return json.dumps(ret.Get())

        b = False
        if iType == 0: # 添加任务
            szNote = pTaskData['Note']
            szTxt = pTaskData['Txt']
            szTaskId = self.CreateUUid()
            SubLabel = []
            pProc = TenProc(Const.g_pTenMySqlObj, pConnect, 'CreateTask',
                            aParam=[szTaskId, szTxt, json.dumps(SubLabel), szNote, szUserId])
            b = await pProc.Proc()
            if b == False:
                ret.SetFalse()
        elif iType == 1: # 删除任务
            szTaskId = pTaskData['TaskId']
            pTable = TenTable(Const.g_pTenMySqlObj, pConnect, 'TaskTable',
                              szDelCon='UserId={!r} and TaskId={!r}'.format(szUserId, szTaskId))
            b = await pTable.Del()
            if b == False:
                ret.SetFalse()
        elif iType == 2: # 修改
            szTaskId = pTaskData['TaskId']

            tmpFilters = []
            tmpData = []
            if 'Txt' in pTaskData:
                tmpFilters.append('Txt')
                tmpData.append(pTaskData['Txt'])
            if 'SubLabel' in pTaskData:
                tmpFilters.append('SubLabel')
                tmpData.append(pTaskData['SubLabel'])
            if 'Note' in pTaskData:
                tmpFilters.append('Note')
                tmpData.append(pTaskData['Note'])

            if len(tmpData) > 0:
                pTable = TenTable(Const.g_pTenMySqlObj, pConnect, 'TaskTable',
                                  szUpdateFields='=%s,'.join(tmpFilters) + '=%s', szUpdateCon='UserId={!r} and TaskId={!r}'.format(szUserId, szTaskId),
                                  aUpdateVale=[tmpData]
                                  )

                # str = ",".join(["(" + ",".join(["%s"] * cols) + ")"] * len(pTable.aIOUVale))

                b = await pTable.Update()
                if b == False:
                    ret.SetFalse()

        else:
            ret.SetFalse()
            ret.SetHints(u'Type不正确')

        await pConnect.Recovery()
        return json.dumps(ret.Get())

    def IsLabel(self, content):
        for c in content:
            if c == ' ':
                continue
            if c == '#' or c == '@':
                return True
            else:
                break
        return False

    def __Item(self, aTree, aData, szParentId):
        if len(aData) <= 0:
            return aData
        while len(aData) > 0:
            item = aData[0]
            CurParentId = item[self._Index['ParentId']]
            CurTaskId = item[self._Index['TaskId']]
            if szParentId != CurParentId:
                return aData
            p = {}
            p['nm'] = item[self._Index['Txt']]
            p['TaskId'] = item[self._Index['TaskId']]
            p['NotTask'] = item[self._Index['NotTask']]
            p['ch'] = []
            aTree.append(p)
            aData = self.__Item(aTree[-1]['ch'], aData[1:], CurTaskId)
        return []

    def RecoveryTree(self, aData):
        tmp = []
        for item in aData:
            if len(item) <= 0:
                continue
            self.__Item(tmp, item, item[0][self._Index['ParentId']])
        return tmp
    async def GetTasks(self, pTenDataRcvd):
        def Correct(pCur, iLevel=0):
            tmp = ''
            if 'nm' in pCur:
                pCur['nm'] = pCur['nm'].lstrip()
            tmp = pCur['nm']
            if 'ch' in pCur:
                chTxt = ''
                p = pCur['ch']
                iLen = len(p) - 1
                while iLen >= 0:
                    subTxt = Correct(p[iLen], iLevel=iLevel+1)
                    chTxt += subTxt
                    if len(subTxt) <= 0:
                        # 移除
                        del p[iLen]
                    iLen -= 1
                if len(chTxt) <= 0:
                    del pCur['ch']
                tmp += chTxt
            return tmp



        ret = TenDataSend()
        szVersion = pTenDataRcvd.GetVer()
        pConnect = TenDbConnect(Const.g_pTenMySqlObj)
        pData = pTenDataRcvd.GetData()
        szUserId = pData['Phone']

        b = await pConnect.GetConnect()
        if b == False:
            ret.SetFalse()
            return json.dumps(ret.Get())
        try:
            pTable = TenTable(Const.g_pTenMySqlObj, pConnect, 'User', szQueryFields='TaskVer',
                              szQueryCon='UserId={}'.format(szUserId))
            b = await pTable.Query()
            data = {}

            if b:
                if pTable.Value !=None:
                    if len(pTable.Value['datas']) > 0:
                        if pTable.Value['datas'][0][0] != szVersion:
                            pProc = TenProc(Const.g_pTenMySqlObj, pConnect, 'GetTasks', aParam=[szVersion, szUserId])
                            data['Data'] = []
                            b = await pProc.Proc()
                            if b:
                                tmpAllTask = pProc.GetAppointData('AllTask')
                                tmpAllTaskData = pProc.ConvertToObj(tmpAllTask['datas'], tmpAllTask['cols_name'])

                                tmpLabel = pProc.GetAppointData('AllLabel')
                                tmpLabelData = pProc.ConvertToObj(tmpLabel['datas'], tmpLabel['cols_name'])

                                tD = []
                                if len(tmpAllTaskData) > 0:
                                    tD = tmpAllTaskData[0]['TaskDatas']
                                    tD = json.loads(tD)
                                # 递归算法恢复树形结构
                                tD = self.RecoveryTree(tD)

                                ppData = []
                                for item in tD:
                                    pp = {}
                                    pp['Txt'] = item
                                    # item['Txt'] = json.loads(item['Txt'])
                                    Txt = pp['Txt']
                                    # 将.Tip转为.TIP 并且生成标签
                                    if 'ch' in Txt:
                                        ch = Txt['ch']
                                        for tmpItem in ch:
                                            nm = tmpItem['nm']
                                            nm = nm.strip()
                                            if nm.upper() == '.TIP':
                                                tmpItem['nm'] = '.TIP'
                                    # 去除标签
                                    # Txt['nm'] = self.FilterLabel(Txt['nm'])
                                    if Correct(Txt) == '':
                                        pp['Valid'] = '0'
                                    else:
                                        pp['Valid'] = '1'

                                    szTaskId = item['TaskId']

                                    self.__AddLabels(pp['Txt'], tmpLabelData, szTaskId)
                                    # 3级标签
                                    if 'ch' in Txt:
                                        ch = Txt['ch']
                                        for tmpItem in ch:
                                            self.__AddLabels(tmpItem, tmpLabelData, tmpItem['TaskId'])
                                            if 'ch' in tmpItem:
                                                ch1 = tmpItem['ch']
                                                for ttItem in ch1:
                                                    self.__AddLabels(ttItem, tmpLabelData, ttItem['TaskId'])


                                    # pp['Labels'] = []
                                    # for label in tmpLabelData:
                                    #     if label['TaskId'] == szTaskId:
                                    #         pp['Labels'].append({
                                    #             'Label': label['Label'],
                                    #             'Seq': label['Seq']
                                    #         })
                                    # 排序
                                    # item['Labels'] = sorted(item['Labels'], key=itemgetter('Seq'))
                                    ppData.append(pp)


                                data['Data'] = ppData
                            else:
                                ret.SetFalse()

                            szVersion = str(pTable.Value['datas'][0][0])
            else:
                ret.SetFalse()
        except:
            ret.SetFalse()
            import traceback
            traceback.print_exc()

        ret.SetVer(szVersion)
        ret.SetData(data)

        await pConnect.Recovery()

        return json.dumps(ret.Get())
    def __AddLabels(self, pNode, pLabels, szTaskId):
        pNode['Labels'] = []
        for label in pLabels:
            if label['TaskId'] == szTaskId:
                pNode['Labels'].append({
                    'Label': label['Label'],
                    'Seq': label['Seq']
                })

    async def ReTasks(self, pTenDataRcvd):
        ret = TenDataSend()
        pData = pTenDataRcvd.GetData()
        szRid = pData['Phone']
        result = False
        ex = ''
        for item in self.aUser:
            if item['UserId'] == szRid:
                result, ex = await self.__PullData(szRid, item['Address'])
                break
        if result:
            ret.SetTrue()
        else:
            ret.SetHints(ex)
            ret.SetFalse()
        return json.dumps(ret.Get())

    async def __PullData(self, Rid, Address):
        """ 拉取WF数据
            Args:
            Returns:
                True or False
            """
        # test
        # szUrl = 'https://workflowy.com/get_initialization_data?share_id={}&client_version=18'.format('F544.ea7JNrW8YZ')

        szUrl = 'https://workflowy.com/get_initialization_data?share_id={}&client_version=18'.format(Address)
        szData = await Http.AsyncGet(szUrl)
        if szData == False:
            return False, u'获取WF数据失败'
        try:
            aTask = []
            pData = json.loads(szData)
            pContent = pData['projectTreeData']['mainProjectTreeInfo']['rootProjectChildren']
            for item in pContent:
                nm = item['nm']
                a = nm.split(' ')
                Labels = []
                for szLabel in a:
                    result =self.IsLabel(szLabel)
                    if result:
                        Labels.append(szLabel)
                for szUrl in a:
                    if re.match(r'^https?:/{2}\w.+$', szUrl):
                        tmpAddress = szUrl.split('/')[-1]
                        tmpUrl = 'https://workflowy.com/get_initialization_data?share_id={}&client_version=18'.format(
                            tmpAddress)
                        tmpData = await Http.AsyncGet(tmpUrl)
                        try:
                            tmp = json.loads(tmpData)
                        except:
                            tmpData.index("The page you're looking for doesn't exist")
                            return False, szUrl + u' 不存在'

                        tmp = tmp['projectTreeData']['mainProjectTreeInfo']['rootProjectChildren']
                        r = {}
                        r['Task'] = tmp
                        r['aLabels'] = Labels
                        aTask.append(r)
        except:
            import traceback
            traceback.print_exc()
            return False, u'获取WF数据失败'
        tmp, szVersion, pLabels = self.__Parse(aTask, Rid)
        if tmp == None:
            return False, u'解析WF失败'
        return await self.__DbUpdate(tmp, szVersion, Rid, pLabels), True

    def FilterLabel(self, szContent):
        Labels = []
        label = ''
        iFirstLabelPos = None
        preChar = None
        iPos = -1
        iTempPos = -1
        i = 0
        for item in szContent:
            i += 1
            if item == ' ':
                if len(label) > 1:
                    Labels.append(label)
                    label = ''
                    if iPos == -1:
                        iPos = iTempPos
                else:
                    label = ''
                preChar = item
                continue
            elif (item == '@' or item == '#') and preChar == ' ':
                iTempPos = i
                label = item
                if preChar != None and iFirstLabelPos == None:
                    iFirstLabelPos = i - 2
            else:
                if label != '':
                    label += item
            preChar = item

        if len(label) > 1:
            Labels.append(label)
            result = True
        if iFirstLabelPos != None:
            return szContent[:iFirstLabelPos]
        else:
            return szContent

        # return Labels
    def CreateUUid(self):
        t = str(uuid.uuid1())
        t = t.replace('-', '')
        return t

    def __StatisticsLabels(self, subLabels, pLabels):
        tmp = []
        p = {}
        for Label in subLabels:
            Label = Label.lstrip()
            Label = Label[:50]
            if Label in p:
                continue
            else:
                p[Label] = 1
            if not Label in pLabels:
                pLabels[Label] = 0
            pLabels[Label] += 1

            tmp.append({
                'L': Label,
                'P': pLabels[Label]
            })
        return tmp
    def __Parse(self, pContent, Rid):
        """ 解析WF数据
            Args:
            Returns:
                True or False
            """
        def Version():
            nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
            randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
            if randomNum <= 10:
                randomNum = str(0) + str(randomNum);
            uniqueNum = str(nowTime) + str(randomNum);
            return uniqueNum
        def FillTab(szContent, iTabCount):
            tmp = ''
            while iTabCount > 0:
                iTabCount -= 1
                tmp += '[#1]'
            return tmp + szContent
        def FilterLabel(allContent, szContent):
            result = False
            Labels = []
            label = ''
            preChar = None
            iPos = -1
            iTempPos = -1
            i = 0
            for item in szContent:
                i += 1
                if item == ' ':
                    if len(label) > 1:
                        Labels.append(label)
                        label = ''
                        if iPos == -1:
                            iPos = iTempPos
                    else:
                        label = ''
                    preChar = item
                    continue
                elif (item == '@' or item == '#') and preChar == ' ':
                    iTempPos = i
                    label = item
                else:
                    if label != '':
                        label += item
                preChar = item

            if len(label) > 1:
                Labels.append(label)
                result = True

            return result, allContent, Labels
        def LoopNote(pTask, iNoteLevel=0, tmpContent=''):
            # tmpContent = FillTab(pTask['nm'], iNoteLevel)
            if 'ch' in pTask:
                ch = pTask['ch']
                for item in ch:
                    tmpContent += '[#0]' + LoopNote(item, iNoteLevel + 1, tmpContent=item['nm'])
            return tmpContent

        def FilterTip(szContent, pNote, pTask):
            first = ''
            iPos = -1
            i = 0
            for item in szContent:
                i += 1
                if item == ' ':
                    if first != '':
                        iPos = i
                        break
                    continue
                first += item
            if first.upper() == '.TIP':
                tmp = ''
                if iPos != -1:
                    tmp = szContent[iPos:]
                if 'ch' in pTask:
                    tmp = LoopNote(pTask, iNoteLevel=0, tmpContent=tmp)

                pNote['szNote'] = tmp
                # if len(pNote['szNote']) > 0:
                #     pNote['szNote'] += '[#0]' + szContent[iPos:]
                # else:
                #     pNote['szNote'] += szContent[iPos:]
                return True
            return False

        # 递归
        def DG(pTask, iTabCount, aSubContent, ParentId, LevelSort=1,Level=0,IsLabel=False):
            tmpContent = FillTab(pTask['nm'], iTabCount)
            # if iTabCount == 1:
            #     b = FilterTip(pTask['nm'], aSubContent, pTask)
            #     if b:
            #         return ''
            # 添加当前内容
            if iTabCount != 0:
                Labels = []
                if IsLabel and Level == 3:
                    xx, xxx, Labels = FilterLabel(tmpContent, pTask['nm'])
                aCmd, filterContent = self.GetCmds(pTask['nm'])
                aSubContent.append({
                    'id': pTask['id'],
                    'nm': pTask['nm'],
                    'ParentId': ParentId,
                    'LevelSort': LevelSort,
                    'Level': Level,
                    'Labels': Labels,
                    'aCmd': aCmd
                })
            if 'ch' in pTask:
                tmpLevelSort = 0
                ch = pTask['ch']
                for item in ch:
                    tmpLevelSort += 1
                    tmpContent += DG(item, iTabCount + 1, aSubContent, pTask['id'], LevelSort=tmpLevelSort, Level=Level+1,IsLabel=IsLabel)
            if iTabCount == 0:
                result, allContent, Labels = FilterLabel(tmpContent, pTask['nm'])
                if result:
                    return allContent, Labels
                else:
                    return tmpContent, Labels
            else:
                return '[#0]' + tmpContent

        def AddTask(globalSeq=0, task=None, pLabels=None, OuterLabel=None, ParentId='', aTask=[], LevelSort=-1, Level=0):
            if LevelSort == -1:
                LevelSort = 1
            else:
                LevelSort += 1
            szUUID = self.CreateUUid()

            aCmd, filterContent = self.GetCmds(task['nm'])

            # 判断是否是标签
            IsLabel = False
            if Level == 2:
                IsLabel = self.IsLabel(filterContent)

            aSubContent = []
            tmpContent, subLabels = DG(task, 0, aSubContent, task['id'], Level=Level, IsLabel=IsLabel)
            if OuterLabel != None:
                OuterLabel.extend(subLabels)
                subLabels = OuterLabel
                # subLabels.insert(0, OuterLabel)
            wfid = task['id']
            tmp = []
            if IsLabel == False:
                tmp = self.__StatisticsLabels(subLabels, pLabels)
            else:
                tmp = self.__StatisticsLabels(OuterLabel, pLabels)

            AddItem(szVersion=szVersion, Txt=task['nm'], Rid=Rid,
                    TaskId=task['id'], Seq=globalSeq, SubLabel=tmp,
                    NotTask=0, ParentId=ParentId, aTask=aTask, LevelSort=LevelSort, aCmd=aCmd)

            for item in aSubContent:
                TmpNotTask = 1
                SubLabel = []
                if IsLabel and item['Level'] == 3:
                    TmpNotTask = 0
                    if OuterLabel != None:
                        item['Labels'].extend(OuterLabel)
                    # 获取列表名称 当做标签
                    tripNM = task['nm'].lstrip()
                    aNM = tripNM.split(' ')
                    if len(aNM) > 0 and len(aNM) > 0:
                        item['Labels'].append(aNM[0])
                    # SubLabel = item['Labels']
                    SubLabel = self.__StatisticsLabels(item['Labels'], pLabels)
                AddItem(szVersion=szVersion, Txt=item['nm'], Rid=Rid,
                        TaskId=item['id'], Seq=globalSeq, SubLabel=SubLabel,
                        NotTask=TmpNotTask, ParentId=item['ParentId'],
                        aTask=aTask, LevelSort=item['LevelSort'], aCmd=item['aCmd'])
            return globalSeq + 1, LevelSort
        def AddItem(szVersion='',Txt='',Rid='',TaskId='',Seq=0,SubLabel=[], NotTask=1, ParentId='',
                    aTask=[], LevelSort=1, aCmd=[]):
            aTask.append([szVersion, Txt, Rid, TaskId + '_' + Rid, Seq,json.dumps(SubLabel), NotTask, ParentId + '_' + Rid, LevelSort, json.dumps(aCmd)])
        try:
            pLabels = {}
            aTask = []
            szVersion = Version()
            globalSeq = 1
            LevelSort = 0
            for pItem in pContent:
                aOuterLabel = pItem['aLabels']
                pTasks = pItem['Task']
                for pTask in pTasks:
                    LevelSort += 1
                    task = pTask
                    aCmd, filterContent = self.GetCmds(task['nm'])
                    isLabel = self.IsLabel(filterContent)
                    if isLabel:
                        # 将本行添加到数据库中
                        AddItem(szVersion=szVersion, Txt=pTask['nm'], Rid=Rid,
                                TaskId=pTask['id'], Seq=-1, SubLabel=[], NotTask=1,
                                ParentId=pTask['id'], aTask=aTask, LevelSort=LevelSort, aCmd=aCmd)
                        if 'ch' in pTask:
                            sub = pTask['ch']
                            tmpLevelSort = 0
                            for itemTask in sub:
                                tp = copy.deepcopy(aOuterLabel)
                                tp.append(filterContent.strip())
                                globalSeq, tmpLevelSort = AddTask(globalSeq=globalSeq,
                                                    task=itemTask, pLabels=pLabels,
                                                    OuterLabel=tp, ParentId=pTask['id'],
                                                    aTask=aTask, LevelSort=tmpLevelSort, Level=2)
                    else:
                        globalSeq, LevelSort = AddTask(globalSeq=globalSeq, task=task,
                                            pLabels=pLabels, OuterLabel=copy.deepcopy(aOuterLabel),
                                            ParentId=pTask['id'], aTask=aTask, LevelSort=LevelSort, Level=1)
        except:
            import traceback
            traceback.print_exc()
            return None

        return aTask, szVersion, pLabels
    def GetCmds(self, szContent):
        a = []
        bStartCmd = False
        # iCmdStartIndex = None
        iCmdContent = ''
        iContentStartIndex = None
        iFirstCharIndex = None
        i = 0
        for Char in szContent:
            # 如果遇到空格 则重置
                #非命令起始
            if Char == ' ':
                if bStartCmd and len(iCmdContent) > 1:
                    a.append(iCmdContent[1:])
                    iCmdContent = ''
                    iContentStartIndex = i
                bStartCmd = False
            else:
                if Char == '.':
                    # 如果还未遇到第一个字符 且是. 则是命令的起始
                    if iFirstCharIndex == None:
                        bStartCmd = True
                    # 弹入命令
                    if len(iCmdContent) > 1:
                        a.append(iCmdContent[1:])
                        iCmdContent = ''
                if bStartCmd:
                    iCmdContent += Char
                if iFirstCharIndex == None:
                    iFirstCharIndex = i
                    iContentStartIndex = i
            i += 1
        if iContentStartIndex == iFirstCharIndex:
            a = []
        tmp = szContent
        if iContentStartIndex != None:
            tmp = szContent[iContentStartIndex:]
        return a, tmp
        # a = []
        # tmpContent = szContent.lstrip()
        # aContent = tmpContent.split(' ')
        # if len(aContent) > 1:
        #     t = aContent[0]
        #     if len(t) > 1:
        #         if t[0] == '.':
        #             aCmd = t[1:].split('.')
        #             a = aCmd
        # return a
    async def __DbUpdate(self, aTask, szVersion, Rid, pLabels):
        if len(aTask) <= 0:
            return True
        pConnect = TenDbConnect(Const.g_pTenMySqlObj)
        b = await pConnect.GetConnect()
        if b == False:
            return False
        b = await pConnect.Begin()
        if b == False:
            return False
        # aTask.append(
            # [szVersion, Txt, Rid, TaskId + '_' + Rid, Seq, json.dumps(SubLabel), NotTask, ParentId + '_' + Rid])
        pTable = TenTable(Const.g_pTenMySqlObj, pConnect, 'TaskTable', szInsertOrUpdateFields='Ver,Txt,UserId,TaskId,Seq,SubLabel,NotTask,ParentId,LevelSort,Cmds',
                          szIOU_InsertType='%s,%s,%s,%s,%s,%s,%s,%s,%s,%s',
                          szIOU_UpdateFields='Txt=values(Txt),Ver=values(Ver),Seq=values(Seq),SubLabel=values(SubLabel),NotTask=values(NotTask),ParentId=values(ParentId),LevelSort=values(LevelSort),Cmds=values(Cmds)',
                          aIOUVale=aTask, szDelCon='UserId="{}" and Ver<>"{}"'.format(Rid, szVersion))

        # pProc = TenProc(Const.g_pTenMySqlObj, pConnect, 'CreateNowTasks', aParam=[szVersion, Rid])



        b = await pTable.IOU()
        if b:
            b = await pTable.Del()
        # if b:
        #     b = await pProc.Proc()
        # if b:
        #     b = await pTenSQL.BatchSql()
        if b:
            b = await pConnect.Commit()
        else:
            await pConnect.Rollback()
        await pConnect.Recovery()
        return b

    def CurrentTimeStampSecond_Day(self):
        t = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        return int(time.mktime(time.strptime(t, '%Y-%m-%d')))
    async def _DoRun(self, pNow):
        return
        # 判断是否可以拉取
        if pNow.hour < 4 or pNow.hour > 6:
            return

        if self.bDoing:
            return
        self.bDoing = True

        for User in self.aUser:
            if User['iLastLoadDate'] == self.CurrentTimeStampSecond_Day():
                continue
            Address = User['Address']
            Rid = User['UserId']
            # 拉取WF数据
            b, c = await self.__PullData(Rid, Address)
            if b:
                User['iLastLoadDate'] = self.CurrentTimeStampSecond_Day()

        self.bDoing = False

