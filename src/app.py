import os
print("hellooo", os.getcwd())
print(os.listdir())
from typing import Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app_config.index_routes import docs
from database.config import Postgres_init, Postgres_shutdown
from features.oauth.google.google_oauth_routes import GOOGLE_OAUTH_ROUTER
from features.users.users_routes import USERS_ROUTER

from starlette.middleware.sessions import SessionMiddleware
from app_config.logger import logger
from fastapi.openapi.utils import get_openapi
from app_config.app_info import description, tags_metadata

# import sentry_sdk
# from sentry_sdk.integrations.starlette import StarletteIntegration
# from sentry_sdk.integrations.fastapi import FastApiIntegration


# # Sentry
# sentry_sdk.init(
#     dsn=os.getenv("SENTRY_DSN"),
#     integrations=[
#         StarletteIntegration(),
#         FastApiIntegration(),
#     ],
#     traces_sample_rate=1.0,
# )

# App
app = FastAPI()

""" SessionMiddleware(
    app=app,
    secret_key=str(os.getenv("JWT_SECRET")),
    same_site="none",
    https_only=True
)
@app.middleware("http")
async def validate_user(request: Request, call_next):
    logger.debug(f"requestion midd yupiii {request.get('session_cookie')} ")
    response = await call_next(request)
    return response """

# Events
app.add_event_handler("startup", Postgres_init)
app.add_event_handler("shutdown", Postgres_shutdown)


# Index Routes
app.add_api_route("/", tags=["Greetings"], methods=["GET"], endpoint=docs)  # type: ignore


# Routers
app.include_router(GOOGLE_OAUTH_ROUTER, prefix="/api/oauth")
app.include_router(USERS_ROUTER, prefix="/api/users")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=[
        "Access-Control-Allow-Headers",
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Origin",
        "Set-Cookie"
    ],
)

# SWAGGER
app.openapi_schema = get_openapi(
    title="NOW ME",
    version="2.5.0",
    description=description,
    tags=tags_metadata,
    routes=app.routes,
)
