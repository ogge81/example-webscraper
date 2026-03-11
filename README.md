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
# Activate
source .venv/bin/activate

# Run server
uvicorn app.main:app --reload

# Check health (in browser)
http://127.0.0.1:8000/health

# Check FastAPI docs
http://127.0.0.1:8000/docs

```