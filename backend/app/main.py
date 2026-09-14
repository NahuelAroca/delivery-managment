from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.drivers import router as drivers_router
from app.routers.records import router as records_router

app = FastAPI(
    title="Delivery Management API",
    version="0.1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(drivers_router)
app.include_router(records_router)

@app.get("/")
def root():
    return {"message": "Management delivery API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}