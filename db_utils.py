import aiosqlite
import asyncio
from datetime import datetime
import typing as tp


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
                                    ts INTEGER,
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
                data['updateDate'],
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
                    updateDate,
                    ts
                ) VALUES(?, ?, ?, ?, ?, ?, ?)""",
            items)
        await self.con.commit()
        return True

    async def delete(self, id, date) -> bool:
        await self.cur.execute(f"""DELETE FROM {self._table_name} WHERE id = ?""", (id,))
        count = bool(self.cur.rowcount)
        await self.con.commit()
        return count

    async def get_node(self, id) -> dict:
        import sqlite3

        async def inner(id: tp.Union[str, sqlite3.Row, tuple]) -> dict:
            info = dict()
            if isinstance(id, str):
                # get info about node
                node = await self.cur.execute(f"SELECT * FROM {self._table_name} WHERE id = ?", (id,))
                result = await node.fetchone()

            elif isinstance(id, (sqlite3.Row, tuple)):
                result, id = id, id[1]
            else:
                raise ValueError(f"Unsuported type {type(id)} supported ( str | sqlite3.row )")

            info['type'] = result[0]
            info['id'] = result[1]
            info['parentId'] = result[2]
            info['url'] = result[3]
            if info['type'] == 'FILE':
                info['children'] = None
                info['size'] = result[4]
            else:
                info['children'] = []
                info['size'] = 0
                childs = await self.cur.execute(f"SELECT * FROM {self._table_name} WHERE parentId = ?", (id,))
                childs_info = await childs.fetchall()
                for c in childs_info:
                    info_c = await inner(c)
                    info['size'] += info_c['size']
                    info['children'].append(info_c)

            info['date'] = result[5]
            return info
        return await inner(id)

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
