from __future__ import print_function

from tornado import ioloop, gen
from tornado_mysql import pools


pools.DEBUG = True


POOL = pools.Pool(
    dict(host='104.155.227.39', port=3306, user='root', passwd='Lhj13950822156', db='IDO'),
    max_idle_connections=1,
    max_recycle_sec=3)


@gen.coroutine
def worker(n):
    for i in range(10):
        t = 1
        print(n, "sleeping", t, "seconds")
        cur = yield POOL.execute("SELECT SLEEP(%s)", (t,))
        print(n, cur.fetchall())


@gen.coroutine
def main():
    workers = [worker(i) for i in range(10)]
    yield workers


ioloop.IOLoop.current().run_sync(main)
print(POOL._opened_conns)