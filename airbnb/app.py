import tornado
import tornado.web

from urls import urls


if __name__ == '__main__':
    app = tornado.web.Application(urls)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
    print('Server is started')
