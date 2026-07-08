from fastapi import FastAPI
from app.api.repository_routes import router as repository_router

app = FastAPI(
    title="GitHub Repository Intelligence API",
    description="Backend API for analyzing and understanding GitHub repositories",
    version="0.1.0"
)

app.include_router(
    repository_router,
    prefix="/api/repositories",
    tags=["Repositories"]
)


@app.get("/")
def root():
    return {
        "message": "GitHub Repository Intelligence API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }