# from openai import OpenAI, APIError
# from logger import logger
# from config import OPENAI_API_KEY
#
# # --- Client-Initialisierung ---
# # Sicherstellen, dass der API-Schlüssel vorhanden ist, bevor der Client erstellt wird.
# if not OPENAI_API_KEY:
#     logger.critical("FATAL: Der OPENAI_API_KEY wurde in der Konfiguration nicht gefunden!")
#     raise ValueError("Der OpenAI API-Schlüssel ist nicht konfiguriert. Die Anwendung kann nicht starten.")
#
# # Erstellt eine einzige, wiederverwendbare Client-Instanz mit dem API-Schlüssel.
# # Dies ist der moderne und empfohlene Weg.
# client = OpenAI(api_key=OPENAI_API_KEY)
#
# def analyze_cv(text: str, language: str = "de") -> str | None:
#     """
#     Analysiert einen Lebenslauftext mithilfe der OpenAI Chat Completions API.
#
#     Args:
#         text (str): Der rohe Text des Lebenslaufs.
#         language (str): Die Sprache, in der die Analyse erfolgen soll.
#
#     Returns:
#         str | None: Der von der KI generierte Analysetext als String,
#                     oder None, wenn ein Fehler auftritt.
#     """
#     # Ein klar definierter System-Prompt verbessert die Qualität der Antwort erheblich.
#     system_prompt = """
#     Du bist ein erfahrener und professioneller HR-Berater.
#     Deine Aufgabe ist es, den bereitgestellten Lebenslauf objektiv zu analysieren.
#     Strukturiere deine Antwort klar und übersichtlich mit Markdown-Formatierung.
#     Beginne mit einer kurzen, prägnanten Zusammenfassung.
#     Liste anschließend die "Stärken" und "Potenziale" (statt Schwächen) in Stichpunkten auf.
#     Gib zum Abschluss eine konstruktive Einschätzung zur allgemeinen Passung für den modernen Arbeitsmarkt.
#     """
#     user_prompt = f"Bitte analysiere den folgenden Lebenslauf in der Sprache '{language}':\n\n---LEBENSLAUF---\n{text}\n---ENDE---"
#
#     try:
#         # Verwendung der modernen Chat-Completions-API
#         response = client.chat.completions.create(
#             model="gpt-4o",  # Aktuelles und leistungsstarkes Modell
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_prompt}
#             ],
#             temperature=0.3,
#             max_tokens=1024  # Genug Token für eine detaillierte Analyse
#         )
#         logger.info("Analyse erfolgreich durchgeführt.")
#         return response.choices[0].message.content.strip()
#     except APIError as e:
#         logger.error(f"Ein Fehler bei der OpenAI API ist aufgetreten: {e}")
#         return None # Gibt None zurück, damit der aufrufende Code den Fehler behandeln kann.
#     except Exception as e:
#         logger.error(f"Ein unerwarteter Fehler ist bei der Analyse aufgetreten: {e}", exc_info=True)
#         return None


from logger import logger

def analyze_cv(text: str, language: str = "de") -> str:
    """
    Simulierte Analyse eines Lebenslaufs. Gibt eine Dummy-Antwort zurück.

    Args:
        text (str): Der Lebenslauftext.
        language (str): Sprache der Analyse.

    Returns:
        str: Simulierte Analyse.
    """

    logger.warning("⚠️ Dummy-Analyse wird verwendet. Keine Verbindung zu OpenAI.")

    dummy_response = f"""
**Zusammenfassung:**  
Der Lebenslauf zeigt solide Erfahrungen und relevante Qualifikationen.  
Die Präsentation ist klar strukturiert und professionell.

**Stärken:**  
- Praktische Erfahrungen in relevanten Bereichen  
- Gute Sprachkenntnisse  
- Bereitschaft zur Weiterentwicklung  

**Potenziale:**  
- Ausbau von Führungs- oder Projektmanagementerfahrungen  
- Vertiefung branchenspezifischer Kenntnisse  

**Einschätzung:**  
Der Kandidat bringt gute Voraussetzungen mit und hat Potenzial für den modernen Arbeitsmarkt.  
Eine gezielte Weiterbildung könnte die Chancen weiter verbessern.
    """

    logger.info("Dummy-Analyse erfolgreich erstellt.")
    return dummy_response.strip()
