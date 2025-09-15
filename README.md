# LinkPro Analytics

A FastAPI and PostgreSQL service for recording events and comparing link activity.

## Overview

The API records clicks and views for link profiles and returns profile, link, traffic, and time metrics.

## Features

### Core Functionality
- **Event tracking**: Track clicks and page views with detailed metadata
- **Profile and link analytics**: Query click and view totals for profiles and individual links
- **Traffic Source Analysis**: Identify and categorize traffic sources (Instagram, TikTok, Twitter, direct traffic)
- **Time-based Insights**: Group events by hour or day
- **Performance Comparisons**: Compare current performance against previous periods

### Technical Features
- RESTful API architecture with FastAPI
- PostgreSQL for event storage
- Pydantic models for data validation
- SQLAlchemy ORM for database operations
- CORS-enabled for frontend integration
- Interactive API documentation with Swagger UI
- Scripts for testing tracking and analytics

## Architecture

```
backend/
├── src/
│   ├── database/
│   │   ├── connection.py      # Database configuration and connection
│   │   └── models.py          # SQLAlchemy database models
│   ├── models/
│   │   ├── analytics.py       # Pydantic models for analytics responses
│   │   ├── click.py          # Event tracking models
│   │   ├── link.py           # Link management models
│   │   └── user.py           # User profile models
│   ├── routes/
│   │   ├── analytics.py      # Analytics endpoints
│   │   ├── tracking.py       # Event tracking endpoints
│   │   └── websocket.py      # WebSocket prototype
│   ├── services/
│   │   ├── analytics.py      # Analytics business logic
│   │   └── report_generator.py # PDF report generation
│   ├── config.py             # Application configuration
│   └── main.py               # Application entry point
├── tests/
│   ├── test_analytics.py     # Analytics checks
│   └── test_db.py           # Database connectivity tests
├── database_setup.sql        # Database schema initialization
└── requirements.txt          # Python dependencies
```

## API Endpoints

### Event Tracking
- `POST /api/track/click` - Track link click events
- `POST /api/track/view` - Track page view events
- `GET /api/track/clicks/{link_id}` - Retrieve clicks for specific link
- `GET /api/track/views/{profile_id}` - Retrieve views for profile

### Analytics
- `GET /api/analytics/profile/{profile_id}` - Complete profile analytics
- `GET /api/analytics/traffic/{profile_id}` - Traffic source analysis
- `GET /api/analytics/time/{profile_id}` - Time-based performance insights
- `GET /api/analytics/quick-stats/{profile_id}` - Summary statistics
- `GET /api/analytics/compare/{profile_id}` - Period comparison analysis

### System
- `GET /health` - Health check with database connectivity test
- `GET /api/system/info` - System information and status
- `GET /docs` - Interactive API documentation

## Data Models

### Core Entities
- **LinkProfile**: User profiles with username and title
- **Link**: Individual links with title, URL, and position
- **ClickEvent**: Click tracking with IP, user agent, and referrer
- **PageView**: Page view tracking with session information

### Analytics Models
- **BasicMetrics**: Core performance metrics (clicks, views, CTR)
- **LinkAnalytics**: Per-link performance analysis
- **ProfileAnalytics**: Profile totals and link metrics
- **TrafficAnalytics**: Traffic source breakdown
- **TimeAnalytics**: Time-based performance patterns

## Technology Stack

### Backend Framework
- **FastAPI**: Modern, high-performance web framework
- **Uvicorn**: ASGI server for running the API
- **Pydantic**: Data validation and serialization
- **SQLAlchemy**: Object-relational mapping and database toolkit

### Database
- **PostgreSQL 17.6**: Primary database for data persistence
- **Psycopg2**: PostgreSQL adapter for Python
- **Alembic**: Database migration management

### Development Tools
- **Python 3.13.7**: Core programming language
- **Pip 25.2**: Package management
- **Python-dotenv**: Environment configuration
- **ReportLab**: PDF report generation

## Database connection

The database connection uses a pool. The schema defines indexes on event timestamps.

## Security Features

- IP address validation and sanitization
- User agent truncation to prevent data overflow
- Input validation on all endpoints
- SQL injection prevention through ORM usage
- CORS configuration for controlled access

## Testing

The test scripts generate sample events and check tracking and analytics endpoints.

## Documentation

Interactive API documentation is available at `/docs` when the server is running, providing detailed endpoint descriptions, request/response schemas, and testing capabilities.

## License

This project is designed for educational and professional development purposes in data engineering and analytics systems.
