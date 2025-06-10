from decouple import config
from pathlib import Path


class Settings:
    # Paths
    PROJ_ROOT: Path = Path(__file__).resolve().parents[1]

    # Service Configuration
    SERVICE_NAME: str = config("SERVICE_NAME", default="task-service")
    SERVICE_PORT: int = config("SERVICE_PORT", default=8002, cast=int)

    # Database Configuration
    DATABASE_URL: str = config(
        "DATABASE_URL",
        default="postgresql+asyncpg://tasks_user:tasks_password@localhost:5432/tasks_db",
    )

    # Firebase Configuration (for token verification)
    FIREBASE_PROJECT_ID: str = config("FIREBASE_PROJECT_ID", default="")
    FIREBASE_SERVICE_ACCOUNT: str = PROJ_ROOT / config(
        "FIREBASE_SERVICE_ACCOUNT", default=""
    )

    # Gateway API Configuration
    GATEWAY_API_URL: str = config("GATEWAY_API_URL", default="http://localhost:8000")
    USER_SERVICE_URL: str = config("USER_SERVICE_URL", default="http://localhost:8001")

    # API Configuration
    VERSION: str = config("VERSION", default="1.0.0")
    API_V1_STR: str = config("API_V1_STR", default="/api/v1")
    ENVIRONMENT: str = config("ENVIRONMENT", default="development")
    DEBUG: bool = config("DEBUG", default=True, cast=bool)

    # Pagination Configuration
    DEFAULT_PAGE_SIZE: int = config("DEFAULT_PAGE_SIZE", default=20, cast=int)
    MAX_PAGE_SIZE: int = config("MAX_PAGE_SIZE", default=100, cast=int)


settings = Settings()
