from fastapi import FastAPI

from app.api.v1.router import api_v1_router
from app.core.cors import configure_cors
from app.schemas.common import HealthResponse

app = FastAPI(
    title="Siming Walkability API",
    version="0.1.0",
    description="Read-only API scaffold for Siming road network and walkability analysis.",
)

configure_cors(app)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="siming-walkability-api")


app.include_router(api_v1_router, prefix="/api/v1")
