from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "AVISENA"
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_DESCRIPTION: str = "Aplicación para gestionar granjas avicolas"

    DB_HOST: str = Field("localhost", env="DB_HOST")
    DB_PORT: int = Field(3306, env="DB_PORT")
    DB_USER: str = Field("root", env="DB_USER")
    DB_PASSWORD: str = Field("", env="DB_PASSWORD")
    DB_NAME: str = Field("", env="DB_NAME")

    jwt_secret: str = Field(..., env="JWT_SECRET")  # obligatorio
    jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

# Instancia única para toda la app
settings = Settings()

