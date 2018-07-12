from Global import TenObj
from tornado.gen import coroutine


class TenDb(TenObj):
    """数据库基类
        """
    def __init__(self, iMaxConnections=50, iConnectTimeOut=120, szHost='', szUser='', szPassword='', szDbName=''):
        super().__init__()
        self.iMaxConnections = iMaxConnections
        self.iConnectTimeOut = iConnectTimeOut
        self.szHost = szHost
        self.szUser = szUser
        self.szPassword = szPassword
        self.szDbName = szDbName
        self.bConnected = False # 是否已经连接


    def Connect(self):
        """ 连接数据库
            Args:
            Returns:
                True or False
            """
        tmp = self._DoConnect()
        if tmp:
            self.bConnected = True
        return tmp
    def _DoConnect(self):
        return True

    def DisConnect(self):
        """ 断开连接数据库
            Args:
            Returns:
                True or False
            """
        tmp = self._DoDisConnect()
        if tmp:
            self.bConnected = False
        return tmp
    def _DoDisConnect(self):
        return True

    @coroutine
    def RecoveryConnect(self, pDbConnect):
        """ 回收连接
            Args:
                pOperate: 操作者
            Returns:
                True or False
            """
        tmp = yield self._DoRecoveryConnect(pDbConnect)
        return tmp

    @coroutine
    def _DoRecoveryConnect(self, pDbConnect):
        return False

    @coroutine
    def GetConnect(self, pDbConnect):
        """ 开始一个事务
            Args:
                pDbConnect: 操作者
            Returns:
                True or False
            """
        tmp = yield self._DoGetConnect(pDbConnect)
        return tmp
    @coroutine
    def _DoGetConnect(self, pDbConnect):
        return False

    @coroutine
    def Commit(self, pDbConnect):
        """ 执行一个事务
            Args:
                pOperate: 操作者
            Returns:
                True or False
            """
        tmp = yield self._DoCommit(pDbConnect)
        return tmp

    @coroutine
    def _DoCommit(self, pDbConnect):
        return True

    @coroutine
    def Begin(self, pDbConnect):
        tmp = yield self._DoBegin(pDbConnect)
        return tmp
    @coroutine
    def _DoBegin(self, pDbConnect):
        return True

    @coroutine
    def Rollback(self, pDbConnect):
        """ 回滚事务
            Args:
                pOperate: 操作者
            Returns:
                True or False
            """
        tmp = yield self._DoRollback(pDbConnect)
        return tmp
    @coroutine
    def _DoRollback(self, pDbConnect):
        return True

    @coroutine
    def Query(self, pTable):
        tmp = yield self._DoQuery(pTable)
        return tmp
    @coroutine
    def _DoQuery(self, pTable):
        return False

    @coroutine
    def Insert(self, pTable):
        tmp = yield self._DoInsert(pTable)
        return tmp
    @coroutine
    def _DoInsert(self, pTable):
        return False

    @coroutine
    def Update(self, pTable):
        tmp = yield self._DoUpdate(pTable)
        return tmp
    @coroutine
    def _DoUpdate(self, pTable):
        return False

    @coroutine
    def Del(self, pTable):
        tmp = yield self._DoDel(pTable)
        return tmp
    @coroutine
    def _DoDel(self, pTable):
        return False

    @coroutine
    def IOU(self, pTable):
        tmp = yield self._DoIOU(pTable)
        return tmp
    @coroutine
    def _DoIOU(self, pTable):
        return False

    async def Proc(self, pProc):
        tmp = await self._DoProc(pProc)
        return tmp

    async def _DoProc(self, pProc):
        return False

    async def BatchSql(self, pBatch):
        tmp = await self._DoBatchSql(pBatch)
        return tmp
    async def _DoBatchSql(self, pBatch):
        return False


    def InsertSql(self, pTable):
        """ 组装插入sql语句
            Args:
                pTable: TenTable对象
            Returns:
                sql语句
            """
        return self._DoInsertSql(pTable)
    def _DoInsertSql(self, pTable):
        return ''

    def QuerySql(self, pTable):
        """ 组装查询sql语句
            Args:
                pTable: TenTable对象
            Returns:
                sql语句
            """
        return self._DoQuerySql(pTable)
    def _DoQuerySql(self, pTable):
        return ''

    def UpdateSql(self, pTable):
        """ 组装更新sql语句
            Args:
                pTable: TenTable对象
            Returns:
                sql语句
            """
        return self._DoUpdateSql(pTable)
    def _DoUpdateSql(self, pTable):
        return ''

    def DelSql(self, pTable):
        """ 组装删除sql语句
            Args:
                pTable: TenTable对象
            Returns:
                sql语句
            """
        return self._DoDelSql(pTable)
    def _DoDelSql(self, pTable):
        return ''

    def IOUSql(self, pTable):
        """ 组装插入或删除sql语句
            Args:
                pTable: TenTable对象
            Returns:
                sql语句
            """
        return self._DoIOUSql(pTable)

    def _DoIOUSql(self, pTable):
        return ''

    def ProcSql(self, pProc):
        """ 组装存储过程语句
            Args:
                pProc: TenProc对象
            Returns:
                sql语句
            """
        return self._DoProcSql(pProc)
    def _DoProcSql(self, pProc):
        return ""

    def _DoLog(self, szError):
        """ 记录日志
            Args:
            Returns:
            """
        pass

class TenDbObj(TenObj):
    def __init__(self, Db):
        super().__init__()
        self.szErr = ''
        self.Db = Db
        self.Value = None
    def ConvertToObj(self, aTuple, aFields):
        a = []
        for item in aTuple:
            i = 0
            p = {}
            for szFields in aFields:
                p[szFields] = item[i]
                i += 1
            a.append(p)
        return a
    def GetAppointData(self, szName):
        try:
            if self.Value == None:
                return None
            if isinstance(self.Value, list) == False:
                return None
            for Item in self.Value:
                if 'cols_name' in Item:
                    if szName in Item['cols_name']:
                        return Item
        except:
            pass
        return None

class TenTable(TenDbObj):
    def __init__(self, Db, pDbConnect, szTableName, szQueryFields='', szQueryCon='', szUpdateFields='', szUpdateCon='', aUpdateVale=[],
                 szInsertFields='', aInsertValue=[], szDelCon='', szInsertOrUpdateFields='', szIOU_InsertType='', szIOU_UpdateFields='', aIOUVale=[],
                 szIndexs='', szGroupby='', szSortby='', szLimit=''):
        super().__init__(Db)
        self.pDbConnect = pDbConnect
        self.szTableName = szTableName

        self.szIndexs = szIndexs  # 索引
        self.szGroupby = szGroupby  # 分组
        self.szSortby = szSortby  # 排序
        self.szLimit = szLimit

        self.szQuerytFields = szQueryFields # 查询字段
        self.szQueryCon = szQueryCon # 查询条件
        self.szQuerySql = self.__QuerySql() # 查询的SQL语句

        self.szUpdateFields = szUpdateFields # 更新字段
        self.szUpdateCon = szUpdateCon # 更新条件
        self.szUpdateSql = self.__UpdateSql() # 更新的SQL语句
        self.aUpdateVale = aUpdateVale # 更新的值

        self.szInsertFields = szInsertFields # 插入字段
        self.aInsertValue = aInsertValue  # 插入的值
        self.szInsertSql = self._InsertSql() # 插入的SQL语句


        self.szDelCon = szDelCon # 删除条件
        self.szDelSql = self._DelSql() # 删除的SQL语句

        # 插入或更新
        self.szIOU_InsertFields = szInsertOrUpdateFields # 插入字段
        self.szIOU_InsertType = szIOU_InsertType # 插入的类型
        self.szIOU_UpdateFields = szIOU_UpdateFields # 更新字段
        self.szIOUSql = self.__IOUSql()  # 查询的SQL语句
        self.aIOUVale = aIOUVale

    def __QuerySql(self):
        """ 组装Query语句
            Args:
            Returns:
                sql语句
            """
        return self.Db.QuerySql(self)
    def __UpdateSql(self):
        """ 组装Update语句
            Args:
            Returns:
                sql语句
            """
        return self.Db.UpdateSql(self)
    def _InsertSql(self):
        """ 组装Insert语句
            Args:
            Returns:
                True or False
            """
        return self.Db.InsertSql(self)
    def _DelSql(self):
        """ 组装Del语句
            Args:
            Returns:
                sql语句
            """
        return self.Db.DelSql(self)
    def __IOUSql(self):
        """ 插入或更新SQL
            Args:
            Returns:
                sql语句
            """
        return self.Db.IOUSql(self)
        pass


    @coroutine
    def Query(self):
        tmp = yield self.Db.Query(self)
        return tmp

    @coroutine
    def Update(self):
        tmp = yield self.Db.Update(self)
        return tmp

    @coroutine
    def Insert(self):
        tmp = yield self.Db.Insert(self)
        return tmp

    @coroutine
    def Del(self):
        tmp = yield self.Db.Del(self)
        return tmp
    @coroutine
    def IOU(self):
        tmp = yield self.Db.IOU(self)
        return tmp

TenQuery = TenTable

class TenProc(TenDbObj):
    def __init__(self, Db, pDbConnect, szProcName, aParam=None):
        super().__init__(Db)
        self.pDbConnect = pDbConnect
        self.szProcSql = self.__ProcSql()
        self.aParam = aParam
        self.szProcName = szProcName
    def __ProcSql(self):
        """ 组装Del语句
            Args:
            Returns:
                True or False
            """
        return self.Db.ProcSql(self)
    async def Proc(self):
        """ 执行存储过程
            Args:
            Returns:
                True or False
            """
        return await self.Db.Proc(self)

class TenSQL(TenDbObj):
    def __init__(self, Db, pDbConnect, aBatchSql):
        super().__init__(Db)
        self.pDbConnect = pDbConnect
        self.aBatchSql = aBatchSql
    async def BatchSql(self):
        return await self.Db.BatchSql(self)

class TenDbConnect(TenDbObj):
    def __init__(self, Db):
        super().__init__(Db)
        self.pCon = None # 连接

    @coroutine
    def GetConnect(self):
        tmp = yield self.Db.GetConnect(self)
        return tmp

    @coroutine
    def Commit(self):
        tmp = yield self.Db.Commit(self)
        return tmp

    @coroutine
    def Begin(self,):
        tmp = yield self.Db.Begin(self)
        return tmp

    @coroutine
    def Rollback(self):
        tmp = yield self.Db.Rollback(self)
        return tmp

    @coroutine
    def Recovery(self):
        tmp = yield self.Db.RecoveryConnect(self)
        return tmp

import tormysql
class TenMySqlDb(TenDb):
    def __init__(self, iMaxConnections=50, iConnectTimeOut=120, szHost='', szUser='', szPassword='', szDbName=''):
        super().__init__(iMaxConnections=iMaxConnections, iConnectTimeOut=iConnectTimeOut, szHost=szHost,
                         szUser=szUser, szPassword=szPassword, szDbName=szDbName)
        self.pConnectPool = None
    def _DoConnect(self):
        if self.pConnectPool != None:
            return True
        try:
            self.pConnectPool = tormysql.ConnectionPool(
                max_connections=self.iMaxConnections,  # max open connections
                idle_seconds=0,  # conntion idle timeout time, 0 is not timeout
                wait_connection_timeout=self.iConnectTimeOut,  # wait connection timeout
                host=self.szHost,
                user=self.szUser,
                passwd=self.szPassword,
                db=self.szDbName,
                charset="utf8",
                autocommit=True
            )
        except:
            return False
        return True
    def _DoDisConnect(self):
        if self.pConnectPool == None:
            return True
        try:
            self.pConnectPool.close()
            self.pConnectPool = None
        except:
            return False
        return True

    @coroutine
    def _DoRecoveryConnect(self, pDbConnect):
        try:
            try:
                yield pDbConnect.pCon['cursor'].close()
            except:
                pass
            try:
                yield pDbConnect.pCon['con'].close()
            except:
                pass
            return True
        except Exception as e:
            if len(e.args) >= 2:
                self._DoLog(e.args[1])
                pDbConnect.szErr = e.args[1]
        return False

    @coroutine
    def _DoGetConnect(self, pDbConnect):
        try:
            pCon = (yield self.pConnectPool.Connection())
            pDbConnect.pCon = {}
            pDbConnect.pCon['con'] = pCon
            pDbConnect.pCon['cursor'] = pCon.cursor()
            return True
        except Exception as e:
            if len(e.args) >= 2:
                self._DoLog(e.args[1])
                pDbConnect.szErr = e.args[1]
            return False

    @coroutine
    def _DoCommit(self, pDbConnect):
        try:
            yield pDbConnect.pCon['con'].commit()
            return True
        except Exception as e:
            if len(e.args) >= 2:
                self._DoLog(e.args[1])
                pDbConnect.szErr = e.args[1]
        return False

    @coroutine
    def _DoBegin(self, pDbConnect):
        try:
            yield pDbConnect.pCon['con'].begin()
            return True
        except Exception as e:
            if len(e.args) >= 2:
                self._DoLog(e.args[1])
                pDbConnect.szErr = e.args[1]
        return False

    @coroutine
    def _DoRollback(self, pDbConnect):
        try:
            b = yield pDbConnect.pCon['con'].rollback()
            return True
        except Exception as e:
            if len(e.args) >= 2:
                self._DoLog(e.args[1])
                pDbConnect.szErr = e.args[1]
        return False

    @coroutine
    def _DoQuery(self, pTable):
        try:
            sql = pTable.szQuerySql
            if pTable.szQueryCon != '':
                sql += ' WHERE {} '.format(pTable.szQueryCon)
            if pTable.szGroupby != '':
                sql += ' GROUP BY {} '.format(pTable.szGroupby)
            if pTable.szSortby != '':
                sql += ' ORDER BY {} '.format(pTable.szSortby)
            if pTable.szLimit != '':
                sql += ' LIMIT {} '.format(pTable.szLimit)
            pCursor = pTable.pDbConnect.pCon['cursor']
            yield pCursor.execute(sql)
            datas = pCursor.fetchall()
            col_name_list = [tuple[0] for tuple in pCursor.description]
            pTable.Value = {}
            pTable.Value['datas'] = datas
            pTable.Value['cols_name'] = col_name_list
            return True
        except Exception as e:
            if len(e.args) >= 2:
                self._DoLog(e.args[1])
                pTable.szErr = e.args[1]
        return False

    @coroutine
    def _DoInsert(self, pTable):
        try:
            sql = self._DoInsertSql(pTable)
            pCursor = pTable.pDbConnect.pCon['cursor']
            tmp = yield pCursor.execute(sql)
            return True
            # # 字段
            # aFields = (pTable.szInsertFields.strip()).split(',')
            #
            # # 拼接插入值
            # values = ' '
            # for item in pTable.aInsertVale:
            #     tmp = ''
            #     for fieldName in aFields:
            #         tmp += item[fieldName] + ','
            #     values += '({}),'.format(tmp[:-1])
            # values = values[:-1] + ';'
            #
            # sql = pTable.szInsertSql + values
            # pCursor = pTable.pDbConnect.pCon['cursor']
            # yield pCursor.execute(sql)
            #
            # return True
        except Exception as e:
            if len(e.args) >= 2:
                self._DoLog(e.args[1])
                pTable.szErr = e.args[1]
        return False

    @coroutine
    def _DoUpdate(self, pTable):
        # # async def _DoUpdate(self, pData={}, szConditions='', szIndex='', szTableName=''):
        # #     # sql = 'UPDATE {} FROM {}'.format(szFields, szTableName)
        # #     # cur.executemany("UPDATE Writers SET Name = %s WHERE Id = %s ",
        # #     #                 [("new_value", "3"), ("new_value", "6")])
        # #     return ''
        try:
            sql = pTable.szUpdateSql + ' ' + pTable.szUpdateFields + ' WHERE ' + pTable.szUpdateCon
                  # + pTable.aUpdateVale
            pCursor = pTable.pDbConnect.pCon['cursor']
            v = []
            for item in pTable.aUpdateVale:
                v.append(tuple(item))
            b = yield pCursor.executemany(sql, v)

            # sql = pCursor.mogrify(sql, tuple(aParams))

            return True
        except Exception as e:
            if len(e.args) >= 2:
                self._DoLog(e.args[1])
                pTable.szErr = e.args[1]
        return False


    @coroutine
    def _DoDel(self, pTable):
        try:
            # sql = pTable.szDelSql
            # if pTable.szDelCon != '':
            #     sql += ' {} '.format(pTable.szDelCon)
            sql = self._DoDelSql(pTable)
            pCursor = pTable.pDbConnect.pCon['cursor']
            tmp = yield pCursor.execute(sql)
            return True
        except Exception as e:
            if len(e.args) >= 2:
                self._DoLog(e.args[1])
                pTable.szErr = e.args[1]
        return False

    @coroutine
    def _DoIOU(self, pTable):
        try:
            if len(pTable.aIOUVale) <= 0:
                return True

            cols = len(pTable.aIOUVale[0])
            str = ",".join(["(" + ",".join(["%s"] * cols) + ")"] * len(pTable.aIOUVale))
            sql = pTable.szIOUSql + str + 'on duplicate key update {}'.format(pTable.szIOU_UpdateFields)

            aParams = []
            for row in pTable.aIOUVale:
                aParams.extend(row)
            pCursor = pTable.pDbConnect.pCon['cursor']
            b = yield pCursor.execute(sql, tuple(aParams))
            return True
        except Exception as e:
            if len(e.args) >= 2:
                self._DoLog(e.args[1])
                pTable.szErr = e.args[1]
        return False

    async def _DoProc(self, pProc):
        try:
            pCursor = pProc.pDbConnect.pCon['cursor']
            if pProc.aParam != None:
                tmp = await pCursor.callproc(pProc.szProcName,tuple(pProc.aParam))
            else:
                tmp = await pCursor.callproc(pProc.szProcName)
            pProc.Value = []
            while True:
                datas = pCursor.fetchall()
                # if len(datas) > 0:
                tmp = {}
                col_name_list = []
                if pCursor.description != None:
                    col_name_list = [tuple[0] for tuple in pCursor.description]

                tmp['datas'] = datas
                tmp['cols_name'] = col_name_list
                pProc.Value.append(tmp)
                rs3 = pCursor.nextset()
                if rs3.result() != True:
                    break
            return True
        except Exception as e:
            if len(e.args) >= 2:
                self._DoLog(e.args[1])
                pProc.szErr = e.args[1]
        return False

    async def _DoBatchSql(self, pBatch):
        try:
            pCursor = pBatch.pDbConnect.pCon['cursor']
            szBatchSql = ';'.join(pBatch.aBatchSql)
            tmp = await pCursor.callproc('batch_sqls',tuple([szBatchSql]))
            pBatch.Value = []
            while True:
                datas = pCursor.fetchall()
                # if len(datas) > 0:
                tmp = {}
                col_name_list = ''
                if pCursor.description != None:
                    col_name_list = [tuple[0] for tuple in pCursor.description]

                tmp['datas'] = datas
                tmp['cols_name'] = col_name_list
                pBatch.Value.append(tmp)
                if pCursor.nextset().result() != True:
                    break
            return True
        except Exception as e:
            if len(e.args) >= 2:
                self._DoLog(e.args[1])
                pBatch.szErr = e.args[1]
        return False


    def _DoInsertSql(self, pTable):
        try:
            sql = 'INSERT INTO {} ({}) VALUES '.format(pTable.szTableName, pTable.szInsertFields)

            if len(pTable.aInsertValue) > 0:
                cols = len(pTable.aInsertValue[0])
                str = ",".join(["(" + ",".join(["%s"] * cols) + ")"] * len(pTable.aInsertValue))
                sql += ' ' + str
            else:
                return ''
            aParams = []
            for row in pTable.aInsertValue:
                aParams.extend(row)

            pCursor = pTable.pDbConnect.pCon['cursor']
            sql = pCursor.mogrify(sql, tuple(aParams))
        except:
            import traceback
            traceback.print_exc()
            return ''
        return sql

    def _DoQuerySql(self, pTable):
        return 'SELECT {} FROM {}'.format(pTable.szQuerytFields, pTable.szTableName)
        if szConditions != '':
            sql += ' WHERE {} '.format(szConditions)
        if szGroupby != '':
            sql += ' GROUP BY {} '.format(szGroupby)
        if szSort != '':
            sql += ' ORDER BY '.format(szSort)
        return sql

    def _DoUpdateSql(self, pTable):
        return 'UPDATE {} SET '.format(pTable.szTableName)

    def _DoDelSql(self, pTable):
        try:
            sql = 'DELETE FROM {} WHERE '.format(pTable.szTableName)
            if pTable.szDelCon != '':
                sql += ' {} '.format(pTable.szDelCon)
        except:
            return ''
        return sql

    def _DoIOUSql(self, pTable):
        return 'INSERT INTO {}({}) VALUES '.format(pTable.szTableName, pTable.szIOU_InsertFields,)