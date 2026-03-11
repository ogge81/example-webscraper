import argparse
import asyncio
import json
from typing import Any

from pydantic import ValidationError

from app.schemas import ScrapeRequest
from app.services.scraper import FetchError, ResponseTooLargeError, fetch_page, parse_page


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="webscraper",
        description="Minimal CLI for scraping a webpage and printing structured JSON.",
    )
    parser.add_argument("url", help="The URL to scrape.")
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output.",
    )
    parser.add_argument(
        "--links-only",
        action="store_true",
        help="Return only extracted links and skip page metadata extraction.",
    )
    parser.add_argument(
        "--internal-only",
        action="store_true",
        help="Return only internal links from the same domain.",
    )
    return parser


async def run_scrape(
        url: str,
        *,
        links_only: bool = False,
        internal_only: bool = False,
    ) -> dict[str, Any]:
    payload = ScrapeRequest(
        url=url,
        links_only=links_only,
        internal_only=internal_only,
    )
    page = await fetch_page(payload.url)
    result = parse_page(
        page,
        links_only=payload.links_only,
        internal_only=payload.internal_only,
    )
    return result.model_dump()


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = asyncio.run(
            run_scrape(
                args.url,
                links_only=args.links_only,
                internal_only=args.internal_only,
            )
        )
    except ValidationError as exc:
        print("Validation error:")
        print(exc)
        raise SystemExit(1) from exc
    except ResponseTooLargeError as exc:
        print(f"Scrape failed: {exc}")
        raise SystemExit(1) from exc
    except FetchError as exc:
        print(f"Scrape failed: {exc}")
        raise SystemExit(1) from exc
    except KeyboardInterrupt:
        print("Cancelled.")
        raise SystemExit(130)

    if args.pretty:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()