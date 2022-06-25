from aiohttp.web import Request, Response, RouteTableDef
import json
from . import models


routes = RouteTableDef()


@routes.get('/index')
async def index(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(models.question.select())
        records = await cursor.fetchall()
        questions = [dict(q) for q in records]
        return Response(text=str(questions))


@routes.get('/')
async def get_home(request: Request) -> Response:
    """
    ---
    description: Just test
    tags:
    - Health check
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation.
        "405":
            description: invalid HTTP Method
    """
    return Response(text=json.dumps({'hella': 'hella'}), status=200)

@routes.get('/cook')
async def post_test(request: Request) -> Response:
    """
    description: Test body
    tags:
    - Health check
    produces:
    - text/plain
    responses:
        "200": success response
    """
    
    return Response(text=json.dumps({
        'cookies': {
            'nice': 'cock'
        }
    }), status=200)