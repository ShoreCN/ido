import tornado
import asyncio
import datetime

import ppInitPath as ppInitPath

from Config import Config
pConfig = Config()
pConfig.CheckEnv()



import Const as Const
from Db import TenMySqlDb
from Global import CmdService
from Svc import CoroSvc
from Svc import TenCoreSvc

import sys
import os
os.chdir(os.path.split( os.path.realpath( sys.argv[0] ) )[0])

async def Loop():
    iSleep = 2000
    while True:
        try:
            # 爬取WF数据
            asyncio.ensure_future(pCoreSvc.Run(datetime.datetime.now(), iSleep))
            await asyncio.sleep(iSleep/1000)
        except:
            import traceback
            traceback.print_exc()
            await asyncio.sleep(iSleep / 1000)
            i = 33

Const.g_pTenPublicDb = TenMySqlDb(szHost='104.155.227.39', szUser='root', szPassword='Lhj13950822156', szDbName=pConfig.GetPublicDbName(), iMaxConnections=15)

if Const.g_pTenPublicDb.Connect():
    pCoroSvc = CoroSvc(pCallback=Loop)
    pCmdService = CmdService()

    pCoreSvc = TenCoreSvc(pCoro=pCoroSvc, iPort=pConfig.GetCoreSvcPort(), pCmdRoute=pCmdService, Db=Const.g_pTenPublicDb)
    pCoreSvc.Start()

    asyncio.ensure_future(Loop())
    tornado.ioloop.IOLoop.current().start()