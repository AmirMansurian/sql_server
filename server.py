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
            (r"/login" , login),
            (r"/logout", logout),
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

    def check_token(self, user):
        resuser = self.db.get("SELECT token from users where username = %s", user)

        if resuser=="":
            return False
        else:
            return True




class defaulthandler(BaseHandler):
    def get(self, *args, **kwargs):
            print()


class signup (BaseHandler):
    def post(self):
        user=self.get_query_argument('username')
        pas=self.get_argument('password')
        firstname=self.get_argument ('firstname', None)
        lastname=self.get_argument('lastname', None)
        token=""
        type=1

        if not self.check_user(user):

            self.db.execute ("INSERT INTO users (username, password, firstname, lastname, token, type) values (%s, %s, %s, %s, %s, %s)", user, pas, firstname, lastname, token, type)
            out={"message": "Signed Up Successfully","code": "200"}
            self.write(out)


class login (BaseHandler):
    def post(self):
        user=self.get_argument('username')
        pas=self.get_argument('password')

        pas_check=self.db.get("SELECT password from users where username = %s", user)

        if not pas_check:
            out = {"message": "check inputs!!!", "code": "400"}
            self.write(out)

        else:
            pas_check=pas_check ["password"]

            if pas==pas_check:

                 if not self.check_token(user):
                     tok=str(hexlify(os.urandom(16)))
                     self.db.execute ("UPDATE users SET token=%s WHERE username=%s ", tok, user)
                     out={"message": "Logged in Successfully", "code": "200", "token": tok}
                     self.write(out)

                 else :
                     out={"maessage": "already logged in!!!", "code": '400'}
                     self.write(out)

            else :
                out={"message": "check inputs!!!", "code": "400"}
                self.write(out)


class logout (BaseHandler):
    def post(self):
        user=self.get_argument('username')
        pas=self.get_argument('password')
        pas_check = self.db.get("SELECT password from users where username = %s", user)

        if not pas_check:
            out = {"message": "check inputs!!!", "code": "400"}
            self.write(out)

        else :
            pas_check=pas_check["password"]

            if pas==pas_check:
                if self.check_token(user):
                    tok=""
                    self.db.execute ("UPDATE users SET token=%s WHERE username=%s", tok, user)
                    out={"message": "logged out!!!", 'code': '200'}
                    self.write(out)

                else:
                    out={'message': 'already logged out!!!', 'code': '400'}
                    self.write(out)

            else:
                out = {"message": "check inputs!!!", "code": "400"}
                self.write(out)






def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
