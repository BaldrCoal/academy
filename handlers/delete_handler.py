from handlers.base_handler import BaseHandler
import json
from db_utils import db


class DeletesHandler(BaseHandler):
    async def delete(self, id):
        answer: dict = dict()
        date = self.get_query_argument("date", None)
        await db.delete(id, date)
        answer["code"] = 200
        answer["message"] = "123ZXC"
        self.set_status(answer["code"])
        self.write(json.dumps(answer))
