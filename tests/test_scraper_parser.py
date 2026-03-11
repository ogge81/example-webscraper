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
        <a href="https://example.com/about">About</a>
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
    assert len(result.links) == 1
    assert result.links[0].href == "https://example.com/about"
    assert result.links[0].text == "About"
    assert "Hello world from the parser test." in result.text_preview