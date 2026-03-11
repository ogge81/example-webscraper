import pytest
from pydantic import ValidationError

from app.schemas.scrape import ScrapeRequest


def test_scrape_request_accepts_valid_https_url() -> None:
    payload = ScrapeRequest(url="https://example.com")
    assert payload.url == "https://example.com"


def test_scrape_request_rejects_invalid_scheme() -> None:
    with pytest.raises(ValidationError):
        ScrapeRequest(url="ftp://example.com")


def test_scrape_request_rejects_missing_domain() -> None:
    with pytest.raises(ValidationError):
        ScrapeRequest(url="https://")