import aiohttp_jinja2
import jinja2
from api.settings import BASE_DIR
from os import path
from aiohttp import web
from api import create_app
from aiohttp_swagger import setup_swagger
from api.middleware import setup_middleware
from api.models import get_engine


app = create_app()
# app.cleanup_ctx.append(get_engine)
setup_middleware(app)
aiohttp_jinja2.setup(
    app, 
    loader=jinja2.FileSystemLoader(
        path.join(BASE_DIR, 'api', 'templates')
    )
)
setup_swagger(app, swagger_url="/api/v1/doc", ui_version=2)


if __name__ == '__main__':
    web.run_app(app)