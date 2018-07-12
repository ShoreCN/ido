import tornado
import asyncio
import datetime
# import os
# a = os.path.abspath(__file__)

import ppInitPath as ppInitPath

from Config import Config
pConfig = Config()
pConfig.CheckEnv()

from WFSvc import WfSvc
from Svc import CoroSvc
from Global import CmdService
from Db import TenMySqlDb
import Const as Const

import sys
import os
os.chdir(os.path.split( os.path.realpath( sys.argv[0] ) )[0])

async def Loop():
    iSleep = 1000
    while True:
        try:
            # 爬取WF数据
            asyncio.ensure_future(pWfSvc.Run(datetime.datetime.now(), iSleep))
            await asyncio.sleep(iSleep/1000)
        except:
            import traceback
            traceback.print_exc()
            await asyncio.sleep(iSleep / 1000)
            i = 33

# Const.g_pTenMySqlObj = TenMySqlDb(szHost='104.155.227.39', szUser='root', szPassword='Lhj13950822156', szDbName=pConfig.GetDbName())
# test
Const.g_pTenMySqlObj = TenMySqlDb(szHost='104.155.227.39', szUser='root', szPassword='Lhj13950822156', szDbName='IDO')

if Const.g_pTenMySqlObj.Connect():
    pCoroSvc = CoroSvc(pCallback=Loop)
    pCmdService = CmdService()

    pWfSvc = WfSvc(pCoro=pCoroSvc, iPort=pConfig.GetWfSvcPort(), pCmdRoute=pCmdService)
    pWfSvc.Start()

    asyncio.ensure_future(Loop())
    tornado.ioloop.IOLoop.current().start()