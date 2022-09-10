from handlers.base_handler import BaseHandler
import json
from db_utils import db


class UpdatesHandler(BaseHandler):
    async def get(self):
        date = self.get_query_argument("date", None)
        answer = await db.updates(date)
        if answer:
            self.set_status(200)
            self.write(json.dumps(answer))
        else:
            answer = {
                "code": 400,
                "message": "Validation Failed"
            }
            self.set_status(answer['code'])
            self.write(json.dumps(answer))
