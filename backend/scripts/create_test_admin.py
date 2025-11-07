"""
Script to create a test admin user in the database.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import AdminUser
from app.auth import get_password_hash


def create_test_admin():
    """Create a test admin user with known credentials."""
    db = SessionLocal()

    try:
        # Test admin credentials
        username = "testadmin"
        email = "testadmin@example.com"
        password = "test"  # Simple password for testing

        # Check if user already exists
        existing_user = db.query(AdminUser).filter_by(username=username).first()
        if existing_user:
            print(f"Test admin user '{username}' already exists!")
            print(f"Username: {username}")
            print(f"Password: {password}")
            return

        # Create new admin user
        hashed_password = get_password_hash(password)
        admin_user = AdminUser(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=True,
        )

        db.add(admin_user)
        db.commit()

        print("=" * 50)
        print("Test Admin User Created Successfully!")
        print("=" * 50)
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print("=" * 50)
        print("\nYou can now use these credentials to login to the admin console.")

    except Exception as e:
        db.rollback()
        print(f"Error creating test admin user: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_test_admin()
