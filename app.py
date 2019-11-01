import asyncio
import decimal

import tornado
import tornado.web
from tornado.platform.asyncio import AsyncIOMainLoop

from dbms import HouseDBMS


class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        db = HouseDBMS()
        await db.insert(
            description='test',
            address='test_address',
            max_person_number='2',
            price=decimal.Decimal('3.14'),
            latitude=4.346346,
            longitude=3.65243634634,
        )


if __name__ == '__main__':
    app = tornado.web.Application([
        (r'/', MainHandler),
    ])

    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()