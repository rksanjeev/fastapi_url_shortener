from datetime import datetime
from hashlib import sha256
import validators
from fastapi import APIRouter, HTTPException, status, Response, Depends, Path
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session

from .schema import URLBase
from .models import URL as URLMODEL
from db import get_db
from config import config

router = APIRouter()


@router.get("/{key}", response_class=RedirectResponse, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def get_url(key: str = Path(max_length=8, min_length=8), db: Session = Depends(get_db)):
    if not key.isalnum():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid url key")
    db_url = db.query(URLMODEL) .filter(URLMODEL.key == key.upper(), URLMODEL.is_active).first()
    if db_url:
        db_url.clicks +=1
        db.add(db_url)
        db.commit()
        return RedirectResponse(db_url.target_url)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")


@router.post("/url", status_code=status.HTTP_201_CREATED)
def create_url(url: URLBase, response: Response, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,  detail="Your provided URL is not valid")
    try:
        target_url = url.target_url.lower()
        existing_url = db.query(URLMODEL).filter(URLMODEL.target_url==target_url).first()
        if existing_url and existing_url.is_active:
            response.status_code = status.HTTP_200_OK
            short_url = existing_url.key
        else:
            short_url= sha256(f'{target_url}:{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}'.encode()).hexdigest()[:8].upper()
            url = URLMODEL(target_url=target_url, is_active=True, clicks=0, key=short_url)
            db.add(url)
            db.commit()
        return {"short_url": f'{config.get("BASE_URL")}{short_url}'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error while processing request")