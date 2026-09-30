from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.database import get_db
from app.models.location import Province, Municipality

router = APIRouter(prefix="/api/location", tags=["location"])


class ProvinceResponse(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        from_attributes = True


class MunicipalityResponse(BaseModel):
    id: int
    name: str
    province_id: int

    class Config:
        from_attributes = True


@router.get("/provinces", response_model=List[ProvinceResponse])
async def get_provinces(db: Session = Depends(get_db)):
    """Get all provinces"""
    provinces = db.query(Province).all()
    return provinces


@router.get("/municipalities", response_model=List[MunicipalityResponse])
async def get_municipalities(province_id: int = None, db: Session = Depends(get_db)):
    """Get municipalities, optionally filtered by province"""
    query = db.query(Municipality)
    if province_id:
        query = query.filter(Municipality.province_id == province_id)
    municipalities = query.all()
    return municipalities
