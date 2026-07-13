from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.repository_routes import router as repository_router
from app.api.auth_routes import router as auth_router

app = FastAPI(
    title="GitHub Repository Intelligence API",
    description="Backend API for analyzing and understanding GitHub repositories",
    version="0.1.0"
)

# Enable CORS for the frontend developer server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Auth Router for history, profile and auth endpoints
app.include_router(
    auth_router,
    prefix="/api",
    tags=["Authentication & User"]
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