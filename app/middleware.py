import jwt
import os
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.auth import get_current_user


class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # if request.url.path in ["/docs", "/openapi.json", "/login", "/signup."]:
        #     return await call_next(request)

        authorization: str = request.headers.get("Authorization")
        if not authorization:
            return JSONResponse(status_code=401, content={"detail": "Authorization header missing."})

        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=401, detail="Invalid token scheme.")

            payload = get_current_user(token)  # Decode JWT
            request.state.user = payload  # Attach user info to request

        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "Token has expired."})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token."})
        except Exception as e:
            return JSONResponse(status_code=401, content={"detail": str(e)})

        return await call_next(request)
