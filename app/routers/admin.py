from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.user import User

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/dashboard")
async def admin_dashboard(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Admin dashboard - placeholder for now"""
    return {
        "message": "Admin Dashboard",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role.value
        },
        "stats": {
            "total_users": db.query(User).count(),
            "active_users": db.query(User).filter(User.status == "active").count()
        }
    }
