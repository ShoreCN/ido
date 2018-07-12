import tornado
import asyncio
import datetime

import tornado.ioloop
import tornado.web
import tormysql

pool = tormysql.ConnectionPool(
    max_connections=50,  # max open connections
    idle_seconds=7200,  # conntion idle timeout time, 0 is not timeout
    wait_connection_timeout=60,  # wait connection timeout
    host="104.155.227.39",
    user="root",
    passwd="Lhj13950822156",
    db="IDO",
    charset="utf8"
)

from WFSvc import WfSvc

async def test():
    with (await pool.Connection()) as conn:
        with conn.cursor() as cursor:
            await cursor.execute('call test();')
            results = cursor.fetchall()
            col_name_list = [tuple[0] for tuple in cursor.description]
            print(col_name_list)
            b = cursor.nextset()
            tmp = cursor.fetchall()
            ii = 3


asyncio.ensure_future(test())
tornado.ioloop.IOLoop.current().start()