from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional

from database.connection import get_db
from database.models import ClickEvent, PageView, Link, LinkProfile
from models.click import (
    ClickEventCreate, 
    ClickEventResponse, 
    PageViewCreate, 
    PageViewResponse, 
    TrackingResponse
)

router = APIRouter(prefix="/api/track", tags=["tracking"])

def get_client_ip(request: Request) -> str:
    """Read the client IP address."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host

@router.post("/click", response_model=TrackingResponse)
async def track_click_event(
    request: Request,
    link_id: int,
    profile_id: int,
    referrer: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Record a click on a link owned by the supplied profile."""
    link = db.query(Link).filter(Link.id == link_id, Link.profile_id == profile_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found for this profile")

    click_data = ClickEventCreate(
        link_id=link_id,
        profile_id=profile_id,
        ip_address=get_client_ip(request),
        user_agent=request.headers.get("User-Agent"),
        referrer=referrer
    )

    db_click = ClickEvent(**click_data.model_dump())
    db.add(db_click)
    db.commit()
    db.refresh(db_click)

    return TrackingResponse(
        status="success",
        message="Click tracked successfully",
        timestamp=db_click.clicked_at,
        event_id=db_click.id
    )


@router.post("/view", response_model=TrackingResponse)
async def track_page_view(
    request: Request,
    profile_id: int,
    referrer: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Record a page view for a profile."""
    profile = db.query(LinkProfile).filter(LinkProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    view_data = PageViewCreate(
        profile_id=profile_id,
        ip_address=get_client_ip(request),
        user_agent=request.headers.get("User-Agent"),
        referrer=referrer
    )

    db_view = PageView(**view_data.model_dump())
    db.add(db_view)
    db.commit()
    db.refresh(db_view)

    return TrackingResponse(
        status="success",
        message="Page view tracked successfully",
        timestamp=db_view.viewed_at,
        event_id=db_view.id
    )


@router.get("/clicks/{link_id}")
async def get_link_clicks(
    link_id: int,
    db: Session = Depends(get_db)
):
    """List recorded clicks for a link."""
    clicks = db.query(ClickEvent).filter(ClickEvent.link_id == link_id).all()
    return {
        "link_id": link_id,
        "total_clicks": len(clicks),
        "clicks": [ClickEventResponse.model_validate(click) for click in clicks]
    }

@router.get("/views/{profile_id}")
async def get_profile_views(
    profile_id: int,
    db: Session = Depends(get_db)
):
    """List recorded page views for a profile."""
    views = db.query(PageView).filter(PageView.profile_id == profile_id).all()
    return {
        "profile_id": profile_id,
        "total_views": len(views),
        "views": [PageViewResponse.model_validate(view) for view in views]
    }
