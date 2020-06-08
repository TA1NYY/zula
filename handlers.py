from tornado.web import authenticated, RequestHandler
from helpers import Tokens, Data
from yaml import load, dump


class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("token")


class LoginHandler(RequestHandler):

    def get(self):
        if self.current_user:
            self.redirect("/")
        else:
            self.render("login.html")

    def post(self):
        token = Tokens()
        if token.search(self.get_argument("token")):
            self.set_secure_cookie(
                "token",
                self.get_argument("token"),
                expires_days=None
            )
            self.redirect("/")
        else:
            self.redirect("/login")


class LogoutHandler(RequestHandler):

    @authenticated
    def get(self):
        self.clear_cookie("token")
        self.redirect("/")


class TokenListHandler(BaseHandler):

    @authenticated
    def get(self):
        token = Tokens()
        self.render(
            "token_list.html",
            tokens=token.all()
        )


class DeleteTokenHandler(BaseHandler):

    @authenticated
    def post(self):
        token = Tokens()
        id = [int(self.get_argument("id"))]
        token.delete(id)
        self.redirect("/tokens")


class CreateTokenHandler(BaseHandler):

    @authenticated
    def post(self):
        token = Tokens()
        token.create(
            name=self.get_argument("name")
        )
        self.redirect("/tokens")


class MainHandler(BaseHandler):

    @authenticated
    def get(self):
        data = Data()
        self.render(
            "values.html",
            data=data.all()
        )


class CreateValueHandler(BaseHandler):

    @authenticated
    def post(self):
        data = Data()
        data.create(
            name=self.get_argument("name"),
            path=self.get_argument("path"),
            values=self.get_argument("value")
        )
        self.redirect("/")


class DeleteValueHandler(BaseHandler):

    @authenticated
    def post(self):
        data = Data()
        id = [int(self.get_argument("id"))]
        data.delete(id)
        self.redirect("/")


class APIHandler(BaseHandler):

    @authenticated
    def get(self):
        self.render("api_doc.html")


class APIGetValuesHandler(BaseHandler):

    def get(self):
        data = Data()
        token = Tokens()

        if token.search(self.get_argument("token")):

            value = data.search(
                self.get_argument("path"),
                self.get_argument("secret_path")
            )

            if value:
                self.write(load(value[0]["values"]))
            else:
                self.set_status(404)
                self.write("Not Value")
        else:
            self.set_status(403)
            self.write("Forbident")
