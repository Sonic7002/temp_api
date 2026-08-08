from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine


# Load environment variables from .env file


from app.api.v1.router import api_v1_router
from app.api.v1.auth import router

app = FastAPI(
    title="Educational Platform API",
    description="A Role-Based Access Control (RBAC) API for Educational Interactions, Note Management, Quiz Generation, and Automated Assessment Tracking.",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(api_v1_router)
app.include_router(router)

@app.get("/health", tags=["root"])
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "ok", "service": app.title}
