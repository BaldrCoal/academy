import aiosqlite
import asyncio
from datetime import datetime


class DataBase:
    _db_name: str = "test.db"
    _table_name: str = "Test"
    __instance = None
    con = None
    cur = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    async def db_init(self):
        self.con: aiosqlite.Connection = await aiosqlite.connect(self._db_name)
        self.cur: aiosqlite.Cursor = await self.con.cursor()
        await self.cur.execute(f"""
                                CREATE TABLE IF NOT EXISTS {self._table_name}
                                (
                                    type TEXT, 
                                    id TEXT,
                                    parentId TEXT,
                                    url TEXT,
                                    size INTEGER,
                                    updateDate TEXT,
                                    PRIMARY KEY (id)
                                )
                                """)

    async def imports(self, data: dict) -> bool:
        ts = self.datetime_valid(data['updateDate'])
        if ts < 0:
            return False
        items = [
            (
                item.get('type', None),
                item['id'],
                item.get('parentId', None),
                item.get('url', None),
                item.get('size', None),
                ts,
            ) for item in data['items']
        ]
        await self.cur.executemany(
            f"""INSERT OR REPLACE INTO {self._table_name}(
                    type,
                    id,
                    parentId,
                    url,
                    size,
                    updateDate
                ) VALUES(?, ?, ?, ?, ?, ?)""",
            items)
        await self.con.commit()
        return True

    async def delete(self, id, date) -> bool:
        await self.cur.execute(f"""DELETE FROM {self._table_name} where id == {id}""")
        return bool(self.cur.rowcount)

    async def get_node(self, id) -> dict:
        ans = dict()
        s = [id]
        return {}

    async def update(self):
        pass

    async def get_node_history(self, id):
        pass

    @staticmethod
    def datetime_valid(dt_str) -> int:
        try:
            ts = datetime.fromisoformat(dt_str.replace('Z', '+00:00')).timestamp()
            return int(ts)
        except ValueError:
            return -1


db: DataBase = DataBase()
