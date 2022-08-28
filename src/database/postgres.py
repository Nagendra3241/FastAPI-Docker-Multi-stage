import os
import dotenv
dotenv.load_dotenv()


POSTGRES_DB_PARAMS = {
    "host"      : os.getenv("DATABASE_HOST"),
    "port"      : os.getenv("DATABASE_PORT"),
    "database"  : os.getenv("DATABASE_NAME"),
    "user"      : os.getenv("DATABASE_USER"),
    "password"  : os.getenv("DATABASE_PASSWORD"),
    "ssl"       : os.getenv("DATABASE_SSL"),
}

