from aiohttp import web
from api import create_app
from aiohttp_swagger import setup_swagger


app = create_app()
setup_swagger(app, swagger_url="/api/v1/doc", ui_version=2)


if __name__ == '__main__':
    web.run_app(app)