from pydantic import BaseModel


class Settings(BaseModel):
    app_env: str = "local"
    cors_origins: list[str] = [
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ]


settings = Settings()
