from handlers.base_handler import BaseHandler
import json
from db_utils import db


class NodesHandler(BaseHandler):
    async def get(self, id):
        answer = await db.get_node(id)
        self.set_status(200)
        self.write(json.dumps(answer))
