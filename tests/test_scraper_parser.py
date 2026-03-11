from app.services.scraper import FetchedPage, parse_page


def test_parse_page_extracts_expected_fields() -> None:
    html = """
    <html>
      <head>
        <title>Test Page</title>
        <meta name="description" content="A short description." />
      </head>
      <body>
        <h1>Main Heading</h1>
        <h2>Section Heading</h2>
        <a href="/about">About</a>
        <a href="https://external.example.org/page">External</a>
        <p>Hello world from the parser test.</p>
      </body>
    </html>
    """

    page = FetchedPage(
        requested_url="https://example.com",
        final_url="https://example.com/final",
        html=html,
    )

    result = parse_page(page)

    assert result.url == "https://example.com"
    assert result.final_url == "https://example.com/final"
    assert result.title == "Test Page"
    assert result.meta_description == "A short description."
    assert result.h1_headings == ["Main Heading"]
    assert result.h2_headings == ["Section Heading"]
    assert len(result.links) == 2
    assert result.links[0].href == "https://example.com/about"
    assert result.links[0].text == "About"
    assert result.links[0].is_internal is True
    assert result.links[1].is_internal is False
    assert "Hello world from the parser test." in result.text_preview

def test_parse_page_links_only_internal_only_filters_links() -> None:
    html = """
    <html>
      <body>
        <a href="/about">About</a>
        <a href="https://example.com/contact">Contact</a>
        <a href="https://external.example.org/page">External</a>
      </body>
    </html>
    """

    page = FetchedPage(
        requested_url="https://example.com",
        final_url="https://example.com/start",
        html=html,
    )

    result = parse_page(page, links_only=True, internal_only=True)

    assert result.title is None
    assert result.meta_description is None
    assert result.h1_headings == []
    assert result.h2_headings == []
    assert result.text_preview == ""
    assert len(result.links) == 2
    assert all(link.is_internal for link in result.links)