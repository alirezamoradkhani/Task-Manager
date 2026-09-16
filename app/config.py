import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    app_name = "Task Manager"
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://task:task@localhost:5432/task_manager",
    )


settings = Settings()
