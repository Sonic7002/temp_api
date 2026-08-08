import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
load_dotenv()

from app.api.v1.router import api_v1_router

app = FastAPI(
    title="Educational Platform API",
    description="A Role-Based Access Control (RBAC) API for Educational Interactions, Note Management, Quiz Generation, and Automated Assessment Tracking.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_v1_router)

@app.get("/", tags=["root"])
def root_endpoint():
    """Root endpoint delivering API overview and documentation links."""
    return {
        "title": app.title,
        "version": app.version,
        "status": "online",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "api_v1_prefix": "/api/v1"
    }

@app.get("/health", tags=["root"])
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "ok", "service": app.title}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
