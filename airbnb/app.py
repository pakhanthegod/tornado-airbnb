import asyncio
import decimal

import tornado
import tornado.web
from tornado.platform.asyncio import AsyncIOMainLoop

from airbnb.dao import HouseDAO


class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        db = HouseDAO()
        engine = await db.get_engine()
        async with engine.acquire() as connection:
            await db.create_table(connection)


if __name__ == '__main__':
    app = tornado.web.Application([
        (r'/', MainHandler),
    ])

    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()