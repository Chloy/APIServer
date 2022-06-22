from aiohttp import web


def create_app() -> web.Application:
    app = web.Application()
    return app