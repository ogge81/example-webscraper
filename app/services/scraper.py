from __future__ import annotations

from dataclasses import dataclass

import certifi
import httpx
from bs4 import BeautifulSoup

from app.core.config import get_settings
from app.schemas.scrape import LinkItem, ScrapeResponse

settings = get_settings()


class ScraperError(Exception):
    """Base scraper exception."""


class FetchError(ScraperError):
    """Raised when a page could not be fetched."""


class ResponseTooLargeError(ScraperError):
    """Raised when the response exceeds the configured size limit."""


@dataclass
class FetchedPage:
    requested_url: str
    final_url: str
    html: str


async def fetch_page(url: str) -> FetchedPage:
    headers = {
        "User-Agent": settings.user_agent,
        "Accept": "text/html,application/xhtml+xml",
    }

    timeout = httpx.Timeout(settings.request_timeout)

    try:
        async with httpx.AsyncClient(
            headers=headers,
            timeout=timeout,
            follow_redirects=True,
            verify=certifi.where() if settings.verify_ssl else False,
        ) as client:
            response = await client.get(url)
            response.raise_for_status()

            content_length = response.headers.get("Content-Length")
            if content_length is not None:
                try:
                    if int(content_length) > settings.max_response_size:
                        raise ResponseTooLargeError(
                            "Response exceeds the maximum allowed size."
                        )
                except ValueError:
                    pass

            content = await _read_response_content(response)

            return FetchedPage(
                requested_url=url,
                final_url=str(response.url),
                html=content,
            )

    except ResponseTooLargeError:
        raise
    except httpx.HTTPStatusError as exc:
        raise FetchError(
            f"Request failed with status code {exc.response.status_code}."
        ) from exc
    except httpx.RequestError as exc:
        raise FetchError(f"Request failed: {exc}") from exc


async def _read_response_content(response: httpx.Response) -> str:
    content = response.text

    if len(content.encode("utf-8")) > settings.max_response_size:
        raise ResponseTooLargeError("Response exceeds the maximum allowed size.")

    return content


def parse_page(page: FetchedPage) -> ScrapeResponse:
    soup = BeautifulSoup(page.html, "html.parser")

    title = _extract_title(soup)
    meta_description = _extract_meta_description(soup)
    h1_headings = _extract_headings(soup, "h1")
    h2_headings = _extract_headings(soup, "h2")
    links = _extract_links(soup)
    text_preview = _extract_text_preview(soup)

    return ScrapeResponse(
        url=page.requested_url,
        final_url=page.final_url,
        title=title,
        meta_description=meta_description,
        h1_headings=h1_headings,
        h2_headings=h2_headings,
        links=links,
        text_preview=text_preview,
    )


def _extract_title(soup: BeautifulSoup) -> str | None:
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
        return title or None
    return None


def _extract_meta_description(soup: BeautifulSoup) -> str | None:
    tag = soup.find("meta", attrs={"name": "description"})
    if not tag:
        return None

    content = tag.get("content")
    if not isinstance(content, str):
        return None

    content = content.strip()
    return content or None


def _extract_headings(soup: BeautifulSoup, tag_name: str) -> list[str]:
    headings: list[str] = []

    for tag in soup.find_all(tag_name):
        text = tag.get_text(" ", strip=True)
        if text:
            headings.append(text)

    return headings


def _extract_links(soup: BeautifulSoup, limit: int = 25) -> list[LinkItem]:
    items: list[LinkItem] = []

    for tag in soup.find_all("a", href=True):
        href = tag.get("href")
        if not isinstance(href, str):
            continue

        text = tag.get_text(" ", strip=True)

        items.append(
            LinkItem(
                href=href.strip(),
                text=text,
            )
        )

        if len(items) >= limit:
            break

    return items


def _extract_text_preview(soup: BeautifulSoup, max_length: int = 500) -> str:
    text = soup.get_text(" ", strip=True)
    text = " ".join(text.split())

    if len(text) <= max_length:
        return text

    return text[: max_length - 3].rstrip() + "..."