# example-webscraper

Minimal Python/FastAPI webscraping boilerplate for learning, testing, and growing into more advanced scraping workflows.

## Goal

Build a clean, reusable project for exploring webscraping on different websites step by step.

## MVP

- Scrape different webpages
- Return structured results
- Keep code clean, typed, and easy to extend

## Out of scope

- Save results to Postgres
- Add Docker support
- Add crawling / queueing
- Add JS-rendered scraping if needed

## Principles

- Minimal and easy to understand
- Production-minded, but fast to build
- Small clean commits
- Validation and error handling from the start
- Easy to extend later

## Tech stack

- Python 3.12
- FastAPI
- Pydantic
- httpx
- BeautifulSoup
- pytest

## Features

- Scrape any static HTML page
- Extract:
  - title
  - meta description
  - headings
  - links
  - text preview
- Normalize relative URLs
- Filter internal links
- API + CLI interface
- Typed schemas with Pydantic
- FastAPI documentation
- Unit and API tests

## Structure

```txt
example-webscraper/
├─ app/
│  ├─ api/
│  ├─ core/
│  ├─ schemas/
│  ├─ services/
│  ├─ cli.py
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
