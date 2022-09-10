from handlers.base_handler import BaseHandler
import json
from db_utils import db


class ImportsHandler(BaseHandler):

    async def post(self) -> None:
        answer: dict = dict()
        try:
            data: dict = json.loads(self.request.body.decode())
        except json.decoder.JSONDecodeError:
            answer["code"] = 400
            answer["message"] = "Invalid document scheme"
        else:
            success: bool = await db.imports(data)
            if success is True:
                answer["code"] = 200
                answer["message"] = "ok"
            else:
                answer["code"] = 400
                answer["message"] = "Validation fail"
        finally:
            self.set_status(answer["code"])
            self.write(json.dumps(answer))
