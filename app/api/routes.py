from fastapi import APIRouter, HTTPException, status

from app.schemas import ScrapeRequest, ScrapeResponse
from app.services.scraper import (
    FetchError,
    ResponseTooLargeError,
    fetch_page,
    parse_page,
)

router = APIRouter()


@router.post(
    "/scrape",
    response_model=ScrapeResponse,
    responses={
        400: {"description": "Bad request while fetching remote page"},
        413: {"description": "Remote page exceeded max allowed size"},
    },
)
async def scrape_page(payload: ScrapeRequest) -> ScrapeResponse:
    try:
        page = await fetch_page(payload.url)
        return parse_page(page)
    except ResponseTooLargeError as exc:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=str(exc),
        ) from exc
    except FetchError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc