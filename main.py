from fastapi import FastAPI

from routes.auth import auth
from routes.product import product
from routes.user import user

app = FastAPI()

app.include_router(user)
app.include_router(product)
app.include_router(auth)
