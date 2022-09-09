import aiosqlite
import asyncio
from datetime import datetime

class DataBase:
    _db_name: str = "test.db"
    __instance = None
    con = None
    cur = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    async def db_init(self):
        self.con = await aiosqlite.connect(self._db_name)
        self.cur = await self.con.cursor()
        await self.cur.execute("""
                                CREATE TABLE IF NOT EXISTS Test
                                (
                                    type TEXT, 
                                    id TEXT,
                                    parentId TEXT,
                                    url TEXT,
                                    size INTEGER,
                                    updateDate TEXT
                                )
                                """)

    async def imports(self, data: dict) -> bool:
        if not self.datetime_valid(data['updateDate']):
            return False
        items = data['items']
        #TODO insert items into db
        return True

    async def deletes(self, id):
        pass

    async def get_node(self, id):
        pass

    async def update(self):
        pass

    async def get_node_history(self, id):
        pass

    @staticmethod
    def datetime_valid(dt_str) -> bool:
        try:
            datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        except:
            return False
        return True


db: DataBase = DataBase()

s = "2022-05-28T21:12:01.000Z"

print(db.datetime_valid(s))
