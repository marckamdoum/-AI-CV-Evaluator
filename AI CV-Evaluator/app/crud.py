from typing import List, Optional
from sqlmodel import Session, select

from models import CVAnalysis, User
from database import get_session

# --- User CRUD ---

def get_user_by_email(email: str) -> Optional[User]:
    """
    Sucht einen Benutzer anhand seiner E-Mail-Adresse in der Datenbank.

    Args:
        email (str): Die E-Mail-Adresse des zu suchenden Benutzers.

    Returns:
        Optional[User]: Das User-Objekt, falls gefunden, sonst None.
    """
    with get_session() as session:
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()


def create_user(email: str, hashed_password: str) -> User:
    """
    Erstellt einen neuen Benutzer in der Datenbank.
    Die Überprüfung, ob der Benutzer bereits existiert, sollte vor dem Aufruf dieser Funktion erfolgen.

    Args:
        email (str): Die E-Mail-Adresse des neuen Benutzers.
        hashed_password (str): Das bereits gehashte Passwort.

    Returns:
        User: Das neu erstellte und in der Datenbank gespeicherte User-Objekt.
    """
    with get_session() as session:
        db_user = User(email=email, password=hashed_password)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


# --- CVAnalysis CRUD ---

def save_analysis(user_id: int, text: str, result: str, language: str) -> CVAnalysis:
    """Speichert eine neue Lebenslauf-Analyse in der Datenbank."""
    with get_session() as session:
        db_analysis = CVAnalysis(user_id=user_id, text=text, result=result, language=language)
        session.add(db_analysis)
        session.commit()
        session.refresh(db_analysis)
        return db_analysis


def get_user_analyses(user_id: int) -> List[CVAnalysis]:
    """
    Holt alle Analysen für einen bestimmten Benutzer aus der Datenbank,
    sortiert nach Erstellungsdatum (neueste zuerst).
    """
    with get_session() as session:
        statement = select(CVAnalysis).where(CVAnalysis.user_id == user_id).order_by(CVAnalysis.created_at.desc())
        results = session.exec(statement).all()
        return results
