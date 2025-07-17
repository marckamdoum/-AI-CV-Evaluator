from sqlmodel import SQLModel, create_engine, Session
from config import BASE_DIR, logger # Importiert aus deiner robusten config.py

# --- Datenbank-Konfiguration ---
# Definiert den Speicherort der SQLite-Datei relativ zum Anwendungs-Basisverzeichnis.
# Dies stellt sicher, dass die Datenbank immer am gleichen, vorhersehbaren Ort liegt.
DATABASE_FILE = "database.db"
DATABASE_PATH = BASE_DIR / DATABASE_FILE
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# --- Datenbank-Engine ---
# 'connect_args' ist KRITISCH für die Verwendung von SQLite mit FastAPI,
# da FastAPI Anfragen in verschiedenen Threads bearbeitet.
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Loggt alle SQL-Anweisungen in der Konsole. Nützlich für die Entwicklung.
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    """
    Erstellt die Datenbankdatei und alle Tabellen, die von deinen SQLModel-Modellen
    definiert werden. Diese Funktion sollte einmal beim Start der Anwendung aufgerufen werden.
    """
    logger.info("Überprüfe und erstelle Datenbank und Tabellen, falls notwendig...")
    SQLModel.metadata.create_all(engine)
    logger.info("Datenbank und Tabellen sind bereit.")

def get_session():
    """
    Liefert eine Datenbank-Session für die Verwendung in FastAPI-Abhängigkeiten.

    Die Verwendung von 'with' stellt sicher, dass die Session nach Abschluss der
    Anfrage (oder im Fehlerfall) immer korrekt geschlossen wird, um Ressourcenlecks
    zu vermeiden.
    """
    # Diese 'with'-Anweisung ist der moderne, sichere Weg, um eine Session zu verwalten.
    with Session(engine) as session:
        # 'yield' übergibt die Session an den API-Endpunkt und wartet,
        # bis dieser seine Arbeit beendet hat, bevor der Code hier weiterläuft.
        yield session
