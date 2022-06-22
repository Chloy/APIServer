from aiohttp.web import Request, Response
import json


def home(request: Request) -> Response:
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