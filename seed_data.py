"""Seed script to create admin and rider users"""
import os
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User, UserRole, UserStatus, BuyerProfile, SellerProfile, RiderProfile
from app.models.location import Province, Municipality
from app.auth import get_password_hash


def seed_users(db: Session):
    """Create admin and rider users"""
    # Check if users already exist
    admin = db.query(User).filter(User.email == "admin@gmail.com").first()
    rider = db.query(User).filter(User.email == "rider@gmail.com").first()
    
    if admin and rider:
        print("Admin and rider users already exist")
        return
    
    # Create admin
    if not admin:
        admin = User(
            email="admin@gmail.com",
            password_hash=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            email_verified=True
        )
        db.add(admin)
        db.flush()
        print(f"Created admin user: admin@gmail.com / admin123")
    
    # Create rider
    if not rider:
        rider = User(
            email="rider@gmail.com",
            password_hash=get_password_hash("rider123"),
            role=UserRole.RIDER,
            status=UserStatus.ACTIVE,
            email_verified=True
        )
        db.add(rider)
        db.flush()
        
        # Create rider profile
        rider_profile = RiderProfile(
            user_id=rider.id,
            phone="09123456789",
            vehicle_type="Motorcycle",
            license_number="RIDER-001",
            available=True
        )
        db.add(rider_profile)
        print(f"Created rider user: rider@gmail.com / rider123")
    
    db.commit()


def seed_locations(db: Session):
    """Create sample provinces and municipalities"""
    # Check if locations already exist
    existing_province = db.query(Province).first()
    if existing_province:
        print("Locations already seeded")
        return
    
    # Create South Cotabato
    south_cotabato = Province(
        name="South Cotabato",
        code="SCT"
    )
    db.add(south_cotabato)
    db.flush()
    
    # Add municipalities
    polomolok = Municipality(
        name="Polomolok",
        province_id=south_cotabato.id
    )
    db.add(polomolok)
    
    general_santos = Municipality(
        name="General Santos",
        province_id=south_cotabato.id
    )
    db.add(general_santos)
    
    db.commit()
    print("Seeded South Cotabato with Polomolok and General Santos")


def main():
    """Main seed function"""
    print("Starting seed...")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        seed_locations(db)
        seed_users(db)
        print("Seed completed successfully")
    except Exception as e:
        print(f"Error during seed: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
