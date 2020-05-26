from handlers import (
    MainHandler, LoginHandler, LogoutHandler, TokenListHandler, APIHandler,
    DeleteTokenHandler, CreateTokenHandler, CreateValueHandler, DeleteValueHandler,
    APIGetValuesHandler
)

patterns = [
    (r"/", MainHandler),

    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),

    (r"/value/create", CreateValueHandler),
    (r"/value/delete", DeleteValueHandler),

    (r"/tokens", TokenListHandler),
    (r"/token/delete", DeleteTokenHandler),
    (r"/token/create", CreateTokenHandler),

    (r"/api", APIHandler),
    (r"/api/value", APIGetValuesHandler),
]