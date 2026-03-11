# example-webscraper

Minimal Python/FastAPI webscraping boilerplate for learning, testing, and growing into more advanced scraping workflows.

## Goal

Build a clean, reusable project for exploring webscraping on different websites step by step.

## MVP

- Scrape different webpages
- Return structured results
- Keep code clean, typed, and easy to extend

## Later

- Save results to Postgres
- Add Docker support
- Add crawling / queueing
- Add JS-rendered scraping if needed

## Tech stack

- Python
- FastAPI
- Pydantic
- httpx
- BeautifulSoup
- pytest

## Principles

- Minimal and easy to understand
- Production-minded, but fast to build
- Small clean commits
- Validation and error handling from the start
- Easy to extend later

## Planned structure

```txt
example-webscraper/
├─ app/
│  ├─ api/
│  ├─ core/
│  ├─ schemas/
│  ├─ services/
│  └─ main.py
├─ tests/
├─ .env.example
├─ .gitignore
├─ README.md
└─ WORKLOG.md
```

## Run app

```bash
# Create viritual enviroment
python3 -m venv .venv

# Activate (to deactivate, command "deactivate")
source .venv/bin/activate

# Run server
uvicorn app.main:app --reload

# Check health (in browser)
http://127.0.0.1:8000/health

# Check FastAPI docs
http://127.0.0.1:8000/docs

# Run tests
python -m pytest

{
  "url": "https://example.com"
}

# CLI Usage (run scraper directly from terminal)
python -m app.cli https://example.com --pretty

# Or without pretty output
python -m app.cli https://example.com

# Return all normalized links
python -m app.cli https://books.toscrape.com/ --links-only --pretty

# Return only internal links
python -m app.cli https://books.toscrape.com/ --links-only --internal-only --pretty

```

## Example URLs to test with

Start with simple pages:

- `https://example.com`
- `https://httpbin.org/html`
- `https://books.toscrape.com/`

What to expect:

- `example.com`
  - very small and stable
  - good first test
  - one main heading and one link

- `httpbin.org/html`
  - simple HTML test page
  - useful for checking text extraction

- `books.toscrape.com`
  - classic scraping practice site
  - useful for exploring links, headings, and later multi-page scraping

Note:
Some websites block bots, require JavaScript, or have anti-scraping protections. For this MVP, prefer simple static pages.

## How to play around

Try changing one thing at a time and compare the output.

Ideas:

- scrape different pages and compare titles, headings, links, and text preview
- inspect how redirecting URLs affect `final_url`
- test invalid URLs and see validation errors
- try a very large page and observe size protection
- change `USER_AGENT` in `.env` and test again
- reduce `REQUEST_TIMEOUT` in `.env` and see how failures behave

Suggested learning path:

1. run the CLI on a simple page
2. run the same URL in Swagger
3. compare outputs
4. inspect the HTML of the page in browser dev tools
5. map HTML elements to the parsed JSON fields
6. modify parser functions and observe what changes