from handlers.base_handler import BaseHandler
from db_utils import db


class NodeHistoryHandler(BaseHandler):
    async def get(self, id):
        dateStart = self.get_query_argument("dateStart", None)
        dateEnd = self.get_query_argument("dateEnd", None)
        ans = db.get_node_history(id, dateStart, dateEnd)
