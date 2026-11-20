from getpass import getpass

from app.database import SessionLocal
from app.models import User
from app.security.password import hash_password


def main():
    username = input("Admin username: ").strip()
    password = getpass("Admin password: ")

    if len(password) < 12:
        print("Password must contain at least 12 characters.")
        return

    db = SessionLocal()

    try:
        existing = db.query(User).filter(
            User.username == username
        ).first()

        if existing:
            print("Username already exists.")
            return

        admin = User(
            username=username,
            password_hash=hash_password(password),
            role="admin",
            is_active=True,
        )

        db.add(admin)
        db.commit()

        print("Admin account created successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    main()