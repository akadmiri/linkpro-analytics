from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import sys

# Import our database and models
from database.connection import Base, engine, test_connection
from routes.tracking import router as tracking_router

# Create analytics routes
from routes.analytics import router as analytics_router

# Create all database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="LinkPro Analytics API",
    description="Analytics dashboard for LinkPro - Track clicks, views, and user behavior",
    version="1.0.0",
    docs_url="/docs"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tracking_router)
app.include_router(analytics_router)

# Basic routes
@app.get("/")
async def root():
    return {
        "message": "LinkPro Analytics API is running",
        "version": "1.0.0",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "docs": "Visit /docs for interactive API documentation",
        "features": {
            "tracking": "Click and page view tracking",
            "analytics": "Comprehensive analytics and insights",
            "traffic_analysis": "Traffic source detection and analysis",
            "time_analysis": "Time-based performance insights"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint with database connectivity test"""
    # Test database connection
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
    """Get system information"""
    return {
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "python_implementation": sys.implementation.name,
        "platform": sys.platform,
        "api_version": "1.0.0",
        "environment": "development"
    }

# Only run with uvicorn if called directly (for development)
if __name__ == "__main__":
    print("Starting LinkPro Analytics API...")
    print(f"Running on Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print("Visit http://127.0.0.1:8000/docs for interactive API documentation")
    print("New Features Added:")
    print("- Profile Analytics: /api/analytics/profile/{profile_id}")
    print("- Traffic Analytics: /api/analytics/traffic/{profile_id}")
    print("- Time Analytics: /api/analytics/time/{profile_id}")
    print("- Quick Stats: /api/analytics/quick-stats/{profile_id}")
    print("- Period Comparison: /api/analytics/compare/{profile_id}")
    print("See docs/SETUP.md for local setup instructions")
    
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
