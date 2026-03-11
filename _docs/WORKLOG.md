# WORKLOG

## Project

**Name:** boilerplate-webscraping  
**Purpose:** learn webscraping by building a minimal but extendable FastAPI-based scraper project

---

## Task plan

### Phase 1 — Foundation
- [x] Create README and worklog
- [x] Initialize Python project
- [x] Create virtual environment
- [x] Install base dependencies
- [x] Create folder structure
- [x] Add gitignore
- [ ] Add env example

### Phase 2 — App skeleton
- [x] Create FastAPI app entrypoint
- [x] Add health route
- [ ] Add settings/config module
- [ ] Add request/response schemas

### Phase 3 — Scraping MVP
- [ ] Add URL validation
- [ ] Add HTTP fetch service
- [ ] Add HTML parsing service
- [ ] Extract title, meta description, headings, links, text preview
- [ ] Create scrape endpoint
- [ ] Add error handling for bad URLs / failed requests

### Phase 4 — Quality
- [ ] Add tests for parsing logic
- [ ] Add tests for validation
- [ ] Add API test for health endpoint
- [ ] Add API test for scrape endpoint
- [ ] Refine docs

### Phase 5 — Later upgrades
- [ ] Add Postgres
- [ ] Add Docker
- [ ] Save scrape results
- [ ] Add crawl mode
- [ ] Add async/background jobs
- [ ] Add JS-rendered scraping option
