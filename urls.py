import tornado.web
from handlers.index_handler import IndexHandler
from handlers.imports_handler import ImportsHandler
from handlers.delete_handler import DeletesHandler
from handlers.nodes_handler import NodesHandler
from handlers.updates_handler import UpdatesHandler
from handlers.nodes_history_handler import NodesHistoryHandler

urls = [
    (r'/', IndexHandler,),
    (r'/imports', ImportsHandler,),
    (r'/delete/(.*)', DeletesHandler),
    (r'/nodes/(.*)', NodesHandler),
    (r'/nodes/(.*)/history', NodesHistoryHandler),
    (r'/updates', UpdatesHandler),


    (r"/tmp/(.)", tornado.web.StaticFileHandler, {"path": "./tmp"}),
    (r"/(.)/?", tornado.web.StaticFileHandler, {"path": "./static"}),
]