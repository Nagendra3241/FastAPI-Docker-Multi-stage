from tortoise import Tortoise
from database.postgres import POSTGRES_DB_PARAMS
from app_config.logger import logger


# https://github.com/tortoise/aerich
# aerich init -t src.database.config.TORTOISE_ORM --location "src/database/migrations/"
# aerich init-db
# aerich migrate --name "migration_name"
# aerich upgrade

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": POSTGRES_DB_PARAMS
        },
    },
    "apps": {
        "DMP": {
            "models": [
                "aerich.models",
                "features.users.users_schema",
            ],
            # If no default_connection specified, defaults to "default"
            "default_connection": "default",
        }
    },
}

# Postgress
async def Postgres_init():
    # await Tortoise.init(config=TORTOISE_ORM)
    # Generate the schema
    # await Tortoise.generate_schemas(safe=True)
    logger.debug("🔥 DataBase Connected !! 🔥")


async def Postgres_shutdown():
    await Tortoise.close_connections()
    logger.debug("🔥 DataBase closed !! 🔥")
