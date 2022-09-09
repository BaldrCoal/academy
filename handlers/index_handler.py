from handlers.base_handler import BaseHandler


class IndexHandler(BaseHandler):

    async def get(self):
        await self.render('index.html')