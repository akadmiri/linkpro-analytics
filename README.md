# LinkPro Analytics

A project for tracking clicks and page views on link profiles.

## Project Overview

The API records click and page-view events. The dashboard fetches the event summaries.

The project uses FastAPI, PostgreSQL, and a JavaScript dashboard.

## Core Features

**Event Tracking System**
Record clicks and page views with IP addresses, user agents, and referrers.

**Analytics Engine** 
Compare event counts and click-through rates by time, referrer, and period.

**Interactive Dashboard**
Chart.js displays metrics returned by the API.

**Machine Learning Integration**
Use the notebook to explore events and compare posting-time models.

## Architecture

The dashboard calls the FastAPI server, which queries PostgreSQL through SQLAlchemy.

PostgreSQL stores profiles, links, and events.

The dashboard fetches metrics through REST endpoints.

## Technology Stack

**Backend Services**
- FastAPI for asynchronous request handling and automatic API documentation
- SQLAlchemy for mapping Python models to PostgreSQL.
- PostgreSQL for profile, link, and event storage.
- Pydantic for data validation and response serialization

**Frontend Interface**
- HTML5 and modern CSS3 with Tailwind framework for responsive design
- JavaScript ES6+ for interactive functionality and API integration
- Chart.js for professional data visualization and analytics presentation

**Development Environment**
- Python 3.13.7 used during development.
- Virtual environment isolation for dependency management
- Environment-based configuration supporting multiple deployment scenarios

## API Endpoints

The API records events and returns analytics as JSON.

Primary tracking functions include click event logging and page view recording with automatic metadata capture. Analytics functions provide profile performance summaries, traffic source analysis, temporal pattern identification, and comparative period analysis.

Interactive API documentation is available through the automatic Swagger interface, enabling immediate testing and integration development.

## Data Models

The database schema centers around user profiles containing multiple tracked links with associated event histories. Click events and page views maintain complete context information for detailed analysis and reporting.

Response models define the fields returned for profile, traffic, and time analytics.

## Machine Learning Pipeline

The notebook explores event patterns, tests group differences, and compares models.

The notebook ranks posting slots using time, traffic source, and model scores.

## Development Standards

Use a local database and keep its credentials outside Git.

The testing framework validates core functionality across tracking accuracy, analytics calculations, and API response consistency through automated validation procedures.

## Requirements

- Windows 10/11 operating system
- Python 3.13.7 with pip 25.2 package manager
- PostgreSQL 17.6 database server
- Modern web browser supporting ES6+ JavaScript features

## Getting Started

Detailed installation procedures and configuration instructions are provided in the SETUP.md documentation. The setup process includes database initialization, virtual environment configuration, and sample data generation for immediate testing.

Use the API health endpoint and tracking routes to check local setup.

## Project Goals
