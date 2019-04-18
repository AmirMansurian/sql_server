import torndb
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import datetime
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
            (r"/sendticket", sendticket),
            (r"/closeticket", closeticket),
            (r"/getticketcli", getticketcli),
            (r"/restoticketmod", restoticketmod),
            (r"/changestatus", changestatus),
            (r"/getticketmod", getticketmod),
            (r".*", defaulthandler),
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
        resuser=resuser['token']

        if resuser=="":
            return False
        else:
            return True


class defaulthandler(BaseHandler):
    def post(self):
        out={'message': 'unknown command!!!', 'code' : '400'}
        self.write(out)


class signup (BaseHandler):
    def post(self):
        user=self.get_query_argument('username')
        pas=self.get_argument('password')
        firstname=self.get_argument ('firstname', None)
        lastname=self.get_argument('lastname', None)
        type=self.get_argument('type', 0)

        if not self.check_user(user):

            self.db.execute ("INSERT INTO users (username, password, firstname, lastname, type) values (%s, %s, %s, %s, %s)", user, pas, firstname, lastname, type)
            out={"message": "Signed Up Successfully","code": "200"}
            self.write(out)

        else :
            out={'message': 'username already taken!!!', 'code': '400'}
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
                     out={"message": "already logged in!!!", "code": '400'}
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


class sendticket (BaseHandler):
    def post(self):
        tok=self.get_argument('token')
        subject=self.get_argument('subject')
        body=self.get_argument('body')
        user = self.db.get("SELECT id from users where token = %s", tok)
        user=user['id']
        now=datetime.datetime.now()
        date=str(now.strftime("%Y-%m-%d %H:%M:%S"))
        status=self.get_argument('type', "open")
        self.db.execute("INSERT INTO tickets (subject, body, user_related, date, status) VALUES (%s, %s, %s, %s, %s)", subject, body, user, date, status)

        max_id=self.db.get("SELECT MAX(id)  FROM tickets")
        max_id=max_id['MAX(id)']

        out={'message': 'ticket sent!!!', 'id': str(max_id), 'code': '200'}
        self.write(out)


class closeticket (BaseHandler):
    def post (self):
        tok=self.get_argument('token')
        id=self.get_argument('id')

        id_check=self.db.get("SELECT user_related from tickets where id=%s", id)
        id_check2=self.db.get("SELECT id from users where token =%s", tok)

        id_check2=id_check2['id']
        id_check=id_check['user_related']

        if id_check==id_check2 :
            self.db.execute("UPDATE tickets SET status=%s WHERE id=%s", 'close', id)

            message="Ticket With id -"+str(id)+"- Closed Successfully"
            out = {'message' : message, 'code': '200'}
            self.write(out)

        else :
            out = {"message": 'permision denied!!!', 'code': '400'}
            self.write(out)


class getticketcli (BaseHandler):
    def post(self):
        tok=self.get_argument('token')
        id=self.db.get ("SELECT id from users where token=%s", tok)
        id=id['id']
        count=self.db.get("SELECT COUNT(id) from tickets where user_related=%s", id)
        count=count['COUNT(id)']

        message="There Are -"+str(count)+"- Ticket"
        out={'tickets': message, 'code': '200'}

        messages=self.db.query("SELECT * from tickets where  user_related=%s", id)

        counter=0

        for x in messages:
            subject=x['subject']
            body=x['body']
            status=x['status']
            id=x['id']
            date=x['date']
            out1={'subject': subject, 'body': body, 'status': status, 'id': id, 'date': date}
            mes="block "+str(counter)
            out2={mes: out1}
            out.update(out2)
            counter=counter+1

        self.write(out)


class restoticketmod (BaseHandler):
        def post(self):
            tok=self.get_argument('token')
            body=self.get_argument('body')
            id=self.get_argument('id')
            check_admin=self.db.get("SELECT type from users where token=%s", tok)
            check_admin=check_admin['type']


            if check_admin:
                self.db.execute("UPDATE tickets SET replay=%s where id=%s", body, id)

                message="Response to Ticket With id - "+str(id)+" - Sent Successfully"
                out={'message': message, 'code': '200'}
                self.write(out)

            else:
                out={'message': 'permision dineid!!!', 'code': '400'}
                self.write(out)


class changestatus(BaseHandler):
    def post(self):
        tok=self.get_argument('token')
        id=self.get_argument('id')
        status=self.get_argument('status')
        check_admin = self.db.get("SELECT type from users where token=%s", tok)
        check_admin = check_admin['type']

        if check_admin:
            self.db.execute("UPDATE tickets SET status=%s where id=%s", status, id)

            message= "Status Ticket With id -"+str(id)+"- Changed Successfully"
            out={'message': message, 'code': '200'}
            self.write(out)

        else:
            out = {'message': 'permision dineid!!!', 'code': '400'}
            self.write(out)


class getticketmod(BaseHandler):

    def post(self):
        tok=self.get_argument('token')
        id=self.db.get ("SELECT id from users where token=%s", tok)
        id=id['id']
        count=self.db.get("SELECT COUNT(id) from tickets")
        count=count['COUNT(id)']

        check_admin = self.db.get("SELECT type from users where token=%s", tok)
        check_admin = check_admin['type']

        if check_admin:

            message="There Are -"+str(count)+"- Ticket"
            out={'tickets': message, 'code': '200'}

            messages=self.db.query("SELECT * from tickets")

            counter=0

            for x in messages:
                subject=x['subject']
                body=x['body']
                status=x['status']
                id=x['id']
                date=x['date']
                out1={'subject': subject, 'body': body, 'status': status, 'id': id, 'date': date}
                mes="block "+str(counter)
                out2={mes: out1}
                out.update(out2)
                counter=counter+1

            self.write(out)

        else:
            out={'message': 'permision denied!!!', 'code': '200'}
            self.write(out)


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
