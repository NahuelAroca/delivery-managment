from fastapi import FastAPI

from app.routers.drivers import router as drivers_router
from app.routers.loads import router as loads_router

app = FastAPI(
    title="Delivery Management API",
    version="0.1.0"
)


app.include_router(drivers_router)
app.include_router(loads_router)

@app.get("/")
def root():
    return {"message": "Management delivery API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}