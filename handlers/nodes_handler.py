from handlers.base_handler import BaseHandler
import json
from db_utils import db


class NodesHandler(BaseHandler):
    async def get(self, id):
        answer = await db.get_node(id)
        answer["code"] = 200
        answer["message"] = "ok"
        self.set_status(answer["code"])
        self.write(json.dumps(answer))
