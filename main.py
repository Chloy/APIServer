import asyncio
import json
from aiohttp import web
from aiohttp_swagger import *


async def home(request: web.Request) -> web.Response:
    """
    ---
    description: This end-point allow to test that service is up.
    tags:
    - Health check
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation. Return "pong" text
        "405":
            description: invalid HTTP Method
    """
    return web.Response(
        text=json.dumps({'response': 'nicecock'}), 
        status=200
    )

app = web.Application()
app.router.add_get('/', home)
setup_swagger(app, swagger_url="/api/v1/doc", ui_version=2)
web.run_app(app)