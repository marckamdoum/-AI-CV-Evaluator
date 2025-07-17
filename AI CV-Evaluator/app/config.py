import json
import os
import sys
from pathlib import Path
from logging.config import fileConfig
from dotenv import load_dotenv
import logging

# --- Grundlegende Pfad-Konfiguration ---
# Definiert das Basisverzeichnis der Anwendung (der Ordner, in dem diese Datei liegt).
# .resolve() sorgt für einen absoluten Pfad, was robuster ist.
BASE_DIR = Path(__file__).resolve().parent

# Lade Umgebungsvariablen aus der .env-Datei im Basisverzeichnis
load_dotenv(BASE_DIR / ".env")

# --- Logging-Konfiguration ---
# Konfiguriere das Logging-System aus der logging.ini-Datei.
# Die Verwendung von BASE_DIR vermeidet Probleme mit dem aktuellen Arbeitsverzeichnis.
LOGGING_CONFIG_PATH = BASE_DIR / "logging.ini"
if not LOGGING_CONFIG_PATH.is_file():
    # Notfall-Logging, falls die .ini-Datei fehlt
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger().critical(f"FATAL: logging.ini nicht gefunden unter: {LOGGING_CONFIG_PATH}")
else:
    # Deaktiviert nicht die Logger von installierten Bibliotheken
    fileConfig(LOGGING_CONFIG_PATH, disable_existing_loggers=False)

# Hole den für dieses Modul konfigurierten Logger (Best Practice)
logger = logging.getLogger(__name__)

# --- Lade Anwendungseinstellungen ---

# 1. Lade kritische Werte aus Umgebungsvariablen und validiere sie
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.critical("FATAL: OPENAI_API_KEY wurde nicht in der .env-Datei gefunden oder ist leer!")
    # Beendet das Programm mit einer klaren Fehlermeldung, anstatt später abzustürzen
    sys.exit("Fehler: OPENAI_API_KEY ist nicht konfiguriert. Die Anwendung kann nicht starten.")

# 2. Lade zusätzliche, weniger kritische Konfigurationen aus einer JSON-Datei
APP_TITLE = 'AI CV Evaluator (Default)' # Standardwert, falls JSON-Datei fehlt
CONFIG_JSON_PATH = BASE_DIR / "config.json"
try:
    logger.info(f"Lade Konfiguration aus {CONFIG_JSON_PATH}...")
    with open(CONFIG_JSON_PATH, mode="r", encoding="UTF-8") as f:
        cfg = json.load(f)
    # Überschreibe den Standardwert nur, wenn der Schlüssel in der Datei existiert
    APP_TITLE = cfg.get('app_title', APP_TITLE)
    logger.info("Konfiguration erfolgreich geladen.")
except FileNotFoundError:
    logger.warning(f"Konfigurationsdatei config.json nicht gefunden. Verwende Standardwerte.")
except json.JSONDecodeError:
    logger.error(f"Fehler beim Parsen von config.json. Die Datei ist möglicherweise fehlerhaft.")

# 3. Statische Konfigurationen, die direkt im Code leben
ANALYSIS_SECTIONS = [
    'result',
    'summary',
    'skills',
    'recommendations',
    'strengths'
]

logger.info(f"Anwendungskonfiguration abgeschlossen. App-Titel: '{APP_TITLE}'")