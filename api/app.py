from aiohttp import web
from . import routes

def create_app() -> web.Application:
    app = web.Application()
    routes.setup_routes(app)
    return app