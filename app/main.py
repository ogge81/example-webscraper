from fastapi import FastAPI


app = FastAPI(
    title="Example Webscraper",
    description="Minimal FastAPI webscraping boilerplate",
    version="0.1.0"
)

@app.get("/health")
async def health():
    return {"status": "ok"}