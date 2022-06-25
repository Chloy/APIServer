from aiohttp import web
from aiohttp_security import setup, SessionIdentityPolicy
from api import create_app
from aiohttp_swagger import setup_swagger
from api.middleware import setup_middleware
from api.models import get_engine


app = create_app()
setup_swagger(app, swagger_url="/api/v1/doc", ui_version=2)
app.cleanup_ctx.append(get_engine)
setup_middleware(app)


if __name__ == '__main__':
    web.run_app(app)