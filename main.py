import os
from secrets import token_urlsafe
from tornado import ioloop, web, httpserver
from tornado.options import define, options, parse_command_line
from header import header
from helpers import Tokens
import urls

define("port", default=8443, type=int)
define("host", default="127.0.0.1", type=str)

URLS = urls.patterns

settings = dict({
    "ssl_options" : {
        "certfile": os.path.join("certs/server.crt"),
        "keyfile": os.path.join("certs/server.key"),
    },
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": token_urlsafe(128),
    "login_url": "/login",
    "xsrf_cookies": True,
    "debug":True,
})


if __name__ == "__main__":
    parse_command_line()

    #First run token create
    token = Tokens()
    token_value = None
    if not token.all():
        token_value = token.get(token.create('root'))["token"]


    header(options.host, options.port, token_value)
    application = web.Application(URLS, **settings)
    app = httpserver.HTTPServer(application)
    app.listen(options.port,options.host)
    ioloop.IOLoop.current().start()