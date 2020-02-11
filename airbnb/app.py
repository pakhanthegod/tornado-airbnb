from __future__ import annotations

from typing import TYPE_CHECKING

import tornado
import tornado.web

from urls import urls


if TYPE_CHECKING:
    from annotations import List
    from tornado.web import Application


def make_app(urls: List) -> Application:
    return tornado.web.Application(urls)


if __name__ == '__main__':
    app = make_app(urls)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
    print('Server is started')
