import logging
import os
import sys
from datetime import datetime
from traceback import format_tb

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database.connection import Base, engine, test_connection
from routes.tracking import router as tracking_router

from routes.analytics import router as analytics_router

logger = logging.getLogger(__name__)
cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS", "http://127.0.0.1:8080,http://localhost:8080"
    ).split(",")
    if origin.strip()
]
if "*" in cors_origins:
    raise ValueError("CORS_ORIGINS must list explicit origins")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LinkPro Analytics API",
    description="Record clicks and page views and query profile analytics.",
    version="1.0.0",
    docs_url="/docs"
)

@app.middleware("http")
async def handle_unexpected_errors(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as error:
        route = getattr(request.scope.get("route"), "path", "<unmatched>")
        # Exception messages can contain database or request data.
        logger.error(
            "Unhandled %s on %s %s\n%s",
            type(error).__name__,
            request.method,
            route,
            "".join(format_tb(error.__traceback__)),
        )
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})


# Register CORS last so its headers also apply to error responses.
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["GET", "POST"],
)

app.include_router(tracking_router)
app.include_router(analytics_router)

@app.get("/")
async def root():
    return {
        "message": "LinkPro Analytics API is running",
        "version": "1.0.0",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "docs": "Visit /docs for interactive API documentation",
        "features": {
            "tracking": "Click and page view tracking",
            "analytics": "Profile and link metrics",
            "traffic_analysis": "Traffic sources grouped by referrer",
            "time_analysis": "Hourly and daily trends"
        }
    }

@app.get("/health")
async def health_check():
    """Check whether PostgreSQL is reachable."""
    db_connected, db_info = test_connection()
    
    return {
        "status": "healthy" if db_connected else "unhealthy",
        "timestamp": datetime.now(),
        "service": "LinkPro Analytics API",
        "database": "Connected" if db_connected else "Disconnected",
        "database_info": db_info,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    }

@app.get("/api/system/info")
async def system_info():
    """Return the Python and API versions."""
    return {
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "python_implementation": sys.implementation.name,
        "platform": sys.platform,
        "api_version": "1.0.0",
        "environment": "development"
    }

if __name__ == "__main__":
    print("Starting LinkPro Analytics API...")
    print(f"Running on Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print("Visit http://127.0.0.1:8000/docs for interactive API documentation")

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
