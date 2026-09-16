from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import PyMongoError

from app.config import settings


# MongoClient manages its own connection pool and connects lazily on first use.
client = MongoClient(
    settings.mongodb_url,
    serverSelectionTimeoutMS=5000,
    tz_aware=True,
)
database: Database = client[settings.mongodb_database]
tasks_collection = database["tasks"]


def mongodb_is_healthy() -> bool:
    """Return whether MongoDB responds to a lightweight ping command."""
    try:
        client.admin.command("ping")
    except PyMongoError:
        return False
    return True
