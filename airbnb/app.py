import tornado
import tornado.web

from urls import urls


def make_app():
    return tornado.web.Application(urls)


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
    print('Server is started')
