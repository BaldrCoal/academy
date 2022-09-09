from handlers.base_handler import BaseHandler
import json
from db_utils import db


class ImportsHandler(BaseHandler):

    async def post(self):
        data = json.loads(self.request.body.decode())
        success = await db.imports(data)
        if success:
            self.set_status(200)
        else:
            # self.set_header("Content-Type", "application/json") ?
            self.set_status(400)
            self.write('{"code": 400,"message": "Validation Failed"}')
