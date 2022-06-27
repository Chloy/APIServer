import base64
from sqlalchemy.orm import Session
from sqlalchemy import select
from aiohttp.web import Request, Response, \
    RouteTableDef, View, json_response
from . import models
import json
import jwt
import time
from .middleware import secret
from api import middleware


routes = RouteTableDef()


@routes.get('/register')
async def register(request: Request) -> Response:
    # with Session(models.create_engine()) as session:
    #     users = session.execute(select(models.User.name)).all()
    token = jwt.encode(
        payload={
            "user": request.rel_url.query['user'],
            "exp": int(time.time() + 60 * 10)
        },
        key=secret
    )
    resp = Response(text=json.dumps({"message": "JWT token generated."}), status=200)
    resp.set_cookie(
        name="Authorization",
        value=f"Bearer {token}",
    )
    return resp


@routes.get('/login')
async def login(request: Request) -> json_response:
    try:
        token = request.cookies["Authorization"].split()[1]
    except KeyError:
        return json_response({"message": "You need tou generate JWT token first.\
            Go to the /register?user=<name>"})
    head, payload, sign = token.split(".")
    head = base64.b64decode(head + '=' * (-len(head) % 4)).decode("utf-8")
    payload = base64.b64decode(payload + '=' * (-len(payload) % 4)).decode("utf-8")
    print("HELLA")
    if jwt.encode(json.loads(payload), key=middleware.secret) != token:
        print(token)
        print(jwt.encode(json.loads(payload), key=middleware.secret))
        return json_response({
            "message": "Token corrupted."
        })
    
    if json.loads(payload)["exp"] <= int(time.time()) + 5:
        return json_response({
            "message": "Token expired."
        })
    

    return json_response({
        "message": "Your token info",
        "token": {
            "head": head,
            "payload": payload,
            "sign": sign
            },
        "token1": jwt.encode(json.loads(payload), key=middleware.secret)
        }
    )