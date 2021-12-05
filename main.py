from fastapi import FastAPI, Request
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.responses import JSONResponse

from routes.auth import auth
from routes.product import product
from routes.user import user

app = FastAPI()

app.include_router(user)
app.include_router(product)
app.include_router(auth)


# for handling exception for JWT
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
