from fastapi import FastAPI

app = FastAPI(
    title="Delivery Management API",
    version="0.1.0"
)


@app.get("/")
def root():
    return {"message": "Management delivery API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}