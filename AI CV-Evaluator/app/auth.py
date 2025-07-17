from passlib.context import CryptContext
from sqlmodel import select
from database import get_session
from models import User
from logger import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

def register_user(email: str, password: str):
    with get_session() as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if user:
            logger.warning(f"Registrierung fehlgeschlagen: {email} existiert bereits.")
            return None
        hashed = hash_password(password)
        new_user = User(email=email, hashed_password=hashed)
        session.add(new_user)
        session.commit()
        logger.info(f"Neuer Benutzer registriert: {email}")
        return new_user

def authenticate_user(email: str, password: str):
    with get_session() as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if user and verify_password(password, user.hashed_password):
            logger.info(f"Benutzer angemeldet: {email}")
            return user
        logger.warning(f"Fehlerhafte Anmeldung für: {email}")
        return None
