from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="Example Webscraper", alias="APP_NAME")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    debug: bool = Field(default=True, alias="DEBUG")

    request_timeout: float = Field(default=10.0, alias="REQUEST_TIMEOUT")
    max_response_size: int = Field(default=2_000_000, alias="MAX_RESPONSE_SIZE")
    user_agent: str = Field(
        default="example-webscraper/0.1 (+learning project)",
        alias="USER_AGENT",
    )

    allowed_schemes: str = Field(default="http,https", alias="ALLOWED_SCHEMES")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def allowed_schemes_list(self) -> list[str]:
        return [scheme.strip() for scheme in self.allowed_schemes.split(",") if scheme.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()