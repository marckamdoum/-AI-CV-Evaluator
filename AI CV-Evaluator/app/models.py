from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import List, Optional

class User(SQLModel, table=True):
    """Repräsentiert einen Benutzer in der Datenbank."""
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    # Das Passwortfeld sollte den HASH des Passworts speichern, niemals Klartext.
    # repr=False verhindert, dass es versehentlich in Logs angezeigt wird.
    password: str = Field(nullable=False, sa_column_kwargs={"repr": False})

    # Definiert die "viele"-Seite der Beziehung: Ein User kann viele CV-Analysen haben.
    analyses: List["CVAnalysis"] = Relationship(back_populates="user")

class CVAnalysis(SQLModel, table=True):
    """
    Repräsentiert eine einzelne, in der Datenbank gespeicherte Lebenslauf-Analyse.
    """
    __tablename__ = "cvanalysis"

    id: Optional[int] = Field(default=None, primary_key=True)

    # repr=False bei langen Textfeldern für eine saubere Konsolenausgabe.
    text: str = Field(sa_column_kwargs={"repr": False})
    result: str = Field(sa_column_kwargs={"repr": False})
    language: str

    # Verwendet timezone.utc, um zeitzonen-bewusste Zeitstempel zu erstellen (Best Practice).
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Definiert die "eine"-Seite der Beziehung: Eine Analyse gehört zu genau einem User.
    user_id: int = Field(foreign_key="user.id", nullable=False)
    user: User = Relationship(back_populates="analyses")
