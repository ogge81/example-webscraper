from urllib.parse import urljoin, urlparse

from pydantic import BaseModel, Field, field_validator

from app.core.config import get_settings


settings = get_settings()


class ScrapeRequest(BaseModel):
    url: str = Field(..., min_length=1, max_length=2048)
    links_only: bool = False
    internal_only: bool = False

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        raw_value = value.strip()

        if not raw_value:
            raise ValueError("URL cannot be empty.")

        parsed = urlparse(raw_value)

        if parsed.scheme not in settings.allowed_schemes_list:
            raise ValueError(
                f"URL scheme must be one of: {', '.join(settings.allowed_schemes_list)}."
            )

        if not parsed.netloc:
            raise ValueError("URL must include a valid domain.")

        return raw_value


class LinkItem(BaseModel):
    href: str
    text: str
    is_internal: bool


class ScrapeResponse(BaseModel):
    url: str
    final_url: str
    title: str | None = None
    meta_description: str | None = None
    h1_headings: list[str] = Field(default_factory=list)
    h2_headings: list[str] = Field(default_factory=list)
    links: list[LinkItem] = Field(default_factory=list)
    text_preview: str = ""