from aiohttp import web
from aiohttp_security import setup, SessionIdentityPolicy
from api import create_app
from aiohttp_swagger import setup_swagger
from api import middleware
from api import models


app = create_app()
setup(app, SessionIdentityPolicy(), middleware.CustomAuthorization())
setup_swagger(app, swagger_url="/api/v1/doc", ui_version=2)
app.cleanup_ctx.append(models.get_engine)


if __name__ == '__main__':
    web.run_app(app)