from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE')

    def post(self):
        self.write('some post')

    def get(self):
        self.write('some get')

    def delete(self):
        self.write('some delete')

    # def options(self, args):
    #     # no body
    #     # *args is for route with path arguments supports
    #     self.set_status(204)
    #     self.finish()
