import torndb
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
from binascii import hexlify
from tornado.options import define, options

define("port", default=1104, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="amir", help="database name")
define("mysql_user", default="x", help="database user")
define("mysql_password", default="123456", help="database password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/signup", signup),
            (r"/login" , login)
        ]
        settings = dict()
        super(Application, self).__init__(handlers, **settings)
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)



class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def check_user(self, user):
        resuser = self.db.get("SELECT * from users where username = %s", user)
        if resuser:
            return True
        else:
            return False

    def token(self, token):
        resuser = self.db.get("SELECT * from users where token = %s", token)
        if resuser:
            return True
        else:
            return False




class defaulthandler(BaseHandler):
    def get(self, *args, **kwargs):
            print()


class signup (BaseHandler):
    def post(self):
        user=self.get_query_argument('username')
        pas=self.get_argument('password')
        firstname=self.get_argument ('firstname', None)
        lastname=self.get_argument('lastname', None)

        if not self.check_user(user):

            self.db.execute ("INSERT INTO users (password, username, firstname, lastname) values (%s, %s, %s, %s)", user, pas, firstname, lastname)


class login (BaseHandler):
    def post(self):
        user=self.get_argument('username')
        pas=self.get_argument('password')


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
