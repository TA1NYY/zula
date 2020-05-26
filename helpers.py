from secrets import token_urlsafe
from tinydb import TinyDB, Query, where
from tornado.options import  define, options, parse_command_line
from storage import AESJSONStorage
from datetime import datetime


define("db", default='db.zula', type=str)

parse_command_line()


class Tokens(object):
    def __init__(self, db=options.db):
        self.db = TinyDB(db, storage=AESJSONStorage)
        self.table = self.db.table('tokens')
        
    def all(self)-> list:
        return self.table.all()

    def create(self, name: str, token=None) -> int:
        return self.table.insert(
            {
                'name':name,
                'token': token if token else token_urlsafe(24),
                'create_date':str(datetime.now())
            }
        )

    def search(self, token: str) -> list:
        Token = Query()
        return self.table.get(Token.token==token)

    def get(self, id: int) -> dict:
        Token = Query()
        return self.table.get(doc_id=id)

    def delete(self, ids: list) -> dict:
        return self.table.remove(doc_ids=ids)


class Data(object):

    def __init__(self, db=options.db):
        self.db = TinyDB(db, storage=AESJSONStorage)
        self.table = self.db.table('data')
    
    def all(self)-> list:
        return self.table.all()

    def create(self, name: str, path: str, values: dict, secret_path: str =None) -> bool:
        self.table.insert(
            {
                "name":name,
                "path":path,
                "secret_path":secret_path if secret_path else token_urlsafe(24),
                "values":values
            }
        )
        return True

    def update(self, ids: list, name: str, path: str, values: dict, secret_path: str =None) -> bool:

        self.table.update(
            {
                "name":name,
                "path":path,
                "secret_path":secret_path if secret_path else token_urlsafe(24),
                "values":values
            },
            doc_ids=ids
        )
        return True

    def search(self, path: str, secret_path: str)  -> dict:
        Values = Query()
        return self.table.search((Values.path == path) & (Values.secret_path == secret_path))

    def delete(self, ids: list) -> dict:
        return self.table.remove(doc_ids=ids)