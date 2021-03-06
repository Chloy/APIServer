from __future__ import annotations
from aiohttp import web
from aiohttp_jwt import JWTMiddleware
import jwt


secret = 'secret'


async def handle_404(request: web.Request) -> web.Response:
    return web.Response(text='Error 404')


async def handle_500(request: web.Request) -> web.Response:
    return web.Response(text='Error 500')


def create_error_middleware(override: dict[int, str]):

    @web.middleware
    async def error_middleware(request: web.Request, handler):
        try:
            return await handler(request)
        except web.HTTPException as ex:
            code = override.get(ex.status)
            if code:
                return await code(request)
            raise
        except Exception as e:
            request.protocol.logger.exception('Error handling exception')
            return await override[500](request)

    return error_middleware


# def get_token(request: web.Request) -> str:
#     return jwt.encode(
#         {"user": request.content}
#     )


def setup_middleware(app: web.Application) -> None:
    error_middleware = create_error_middleware({
        404: handle_404,
        500: handle_500
    })
    app.middlewares.append(error_middleware)
    # app.middlewares.append(JWTMiddleware(
    #     secret_or_pub_key=secret,
    #     request_property="user",
    #     token_getter=get_token
    # ))