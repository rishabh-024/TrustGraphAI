from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router

app = FastAPI(
    title="TrustGraph AI",
    description="Non-Human Identity Risk & Blast-Radius Intelligence Platform",
    version="0.1.0",
)

# Development configuration.
# Restrict this to the actual frontend origin in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "application": "TrustGraph AI",
        "message": "Backend is running",
        "version": "0.1.0",
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "TrustGraph AI Backend",
        "database": "not_connected_yet",
    }
