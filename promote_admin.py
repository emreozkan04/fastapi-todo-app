# promote_admin.py
import argparse
from sqlmodel import Session, select
from app.database import engine
from app.models import User

def promote_user_to_admin(email: str):
    """Finds a user by email and sets their is_admin flag to True."""
    with Session(engine) as session:
        # Find the user in the database
        user = session.exec(select(User).where(User.email == email)).first()

        if not user:
            print(f"Error: User with email '{email}' not found.")
            return

        if user.is_admin:
            print(f"User '{email}' is already an admin.")
            return
            
        # Promote the user
        user.is_admin = True
        session.add(user)
        session.commit()
        session.refresh(user)
        
        print(f"Success! User '{user.email}' has been promoted to an admin.")

if __name__ == "__main__":
    # This sets up the command-line argument parser
    parser = argparse.ArgumentParser(description="Promote a user to an admin.")
    parser.add_argument("email", type=str, help="The email of the user to promote.")
    
    args = parser.parse_args()
    
    promote_user_to_admin(email=args.email)