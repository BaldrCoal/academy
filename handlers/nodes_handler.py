from handlers.base_handler import BaseHandler
import json
from db_utils import db


class NodesHandler(BaseHandler):
    async def get(self, id):
        answer = await db.get_node(id)
        if answer is None:
            answer = {'code': 404,
                      'message': "Item not found"}
            self.set_status(answer['code'])
            self.write(json.dumps(answer))
        else:
            self.set_status(200)
            self.write(json.dumps(answer))
