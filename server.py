import sys
import os
import asyncio
import logging
import tornado.web
import tornado.platform.asyncio
import tornado.log
from tornado.options import define, options, parse_config_file
import urls
from db_utils import db

define("port", type=int)
define("debug", type=str)
parse_config_file("application.conf")
tornado.options.parse_command_line()


class Application(tornado.web.Application):
    def init(self, args, **kwargs):
        super(Application, self).init(args, **kwargs)


async def main():
    tornado.log.enable_pretty_logging()

    logging_mode = logging.DEBUG if options.debug == 'yes' else logging.INFO
    tornado.log.app_log.setLevel(logging_mode)

    application = Application(
        urls.urls,
        template_path='./templates',
        debug=(True if options.debug == "yes" else False))
    await db.db_init()
    application.listen(options.port)
    print('server started on port {}'.format(options.port))
    asyncio.get_event_loop()
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()


if __name__ == "__main__":
    asyncio.run(main())
