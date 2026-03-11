from fastapi import APIRouter

from app.schemas import ScrapeRequest, ScrapeResponse

router = APIRouter()


@router.post("/scrape", response_model=ScrapeResponse)
async def scrape_page(payload: ScrapeRequest) -> ScrapeResponse:
    return ScrapeResponse(
        url=payload.url,
        final_url=payload.url,
        title=None,
        meta_description=None,
        h1_headings=[],
        h2_headings=[],
        links=[],
        text_preview="",
    )