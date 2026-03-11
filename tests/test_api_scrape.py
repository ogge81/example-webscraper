from fastapi.testclient import TestClient

from app.main import app
from app.services.scraper import FetchedPage

client = TestClient(app)


def test_scrape_returns_structured_data(monkeypatch) -> None:
    async def mock_fetch_page(url: str) -> FetchedPage:
        return FetchedPage(
            requested_url=url,
            final_url="https://example.com/final",
            html="""
            <html>
              <head>
                <title>Mock Title</title>
                <meta name="description" content="Mock description" />
              </head>
              <body>
                <h1>Mock H1</h1>
                <h2>Mock H2</h2>
                <a href="https://example.com/about">About</a>
                <p>Hello from mocked scrape endpoint test.</p>
              </body>
            </html>
            """,
        )

    monkeypatch.setattr("app.api.routes.fetch_page", mock_fetch_page)

    response = client.post("/scrape", json={"url": "https://example.com"})

    assert response.status_code == 200

    data = response.json()
    assert data["url"] == "https://example.com"
    assert data["final_url"] == "https://example.com/final"
    assert data["title"] == "Mock Title"
    assert data["meta_description"] == "Mock description"
    assert data["h1_headings"] == ["Mock H1"]
    assert data["h2_headings"] == ["Mock H2"]
    assert len(data["links"]) == 1
    assert data["links"][0]["href"] == "https://example.com/about"
    assert data["links"][0]["text"] == "About"
    assert "Hello from mocked scrape endpoint test." in data["text_preview"]


def test_scrape_rejects_invalid_url() -> None:
    response = client.post("/scrape", json={"url": "ftp://example.com"})

    assert response.status_code == 422


def test_scrape_returns_413_when_response_is_too_large(monkeypatch) -> None:
    from app.api.routes import ResponseTooLargeError

    async def mock_fetch_page(url: str) -> FetchedPage:
        raise ResponseTooLargeError("Response exceeds the maximum allowed size.")

    monkeypatch.setattr("app.api.routes.fetch_page", mock_fetch_page)

    response = client.post("/scrape", json={"url": "https://example.com"})

    assert response.status_code == 413
    assert response.json()["detail"] == "Response exceeds the maximum allowed size."


def test_scrape_returns_400_when_fetch_fails(monkeypatch) -> None:
    from app.api.routes import FetchError

    async def mock_fetch_page(url: str) -> FetchedPage:
        raise FetchError("Request failed: mock network error")

    monkeypatch.setattr("app.api.routes.fetch_page", mock_fetch_page)

    response = client.post("/scrape", json={"url": "https://example.com"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Request failed: mock network error"