from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_rider
from app.models.user import User

router = APIRouter(prefix="/api/rider", tags=["rider"])


@router.get("/dashboard")
async def rider_dashboard(current_user: User = Depends(require_rider), db: Session = Depends(get_db)):
    """Rider dashboard - placeholder for now"""
    return {
        "message": "Rider Dashboard",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role.value
        },
        "stats": {
            "available": True,
            "deliveries_today": 0,
            "total_deliveries": 0
        }
    }
