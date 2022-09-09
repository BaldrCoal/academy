from handlers.base_handler import BaseHandler
import json


class DeletesHandler(BaseHandler):
    async def delete(self, id):
        print(id)
        self.write("Tima lox")
