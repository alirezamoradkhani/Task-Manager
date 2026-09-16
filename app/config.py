import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    app_name = "Task Manager"
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    mongodb_database = os.getenv("MONGODB_DATABASE", "task_manager")


settings = Settings()
