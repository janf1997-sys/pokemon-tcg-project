import re
import pandas as pd
import psycopg2
import requests
from bs4 import BeautifulSoup

# --- 1. PostgreSQL Verbindung & Pokedex-Namen laden ---
print("Verbinde mit PostgreSQL (pokedex_db)...")

try:
    conn = psycopg2.connect(
        dbname="pokedex_db",
        user="dev",  # Deinen DB-Benutzer eintragen
        password="holland13",  # Dein DB-Passwort eintragen
        host="localhost",  # DB-Host (z.B. localhost oder IP)
        port="5432",  # Standard-Port für PostgreSQL
    )

    cursor = conn.cursor()

    # PASSE HIER DEINEN TABELLEN- UND SPALTENNAMEN AN:
    # Beispiel: SELECT name FROM pokemon_species;
    cursor.execute("SELECT pokemon_name FROM pokedex;")
    db_rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # Namen in ein Set umwandeln und säubern
    pokedex_names = {row[0].strip().lower() for row in db_rows if row[0]}
    print(
        f"Erfolg: {len(pokedex_names)} Pokémon-Namen aus 'pokedex_db' geladen.\n"
    )

except Exception as e:
    print(f"Fehler bei der Datenbankverbindung: {e}")
    exit()


# --- 2. Hilfsfunktion: Matching gegen deine Pokedex-Liste ---
def match_pokemon_from_pokedex(card_name, pokedex):
    card_name_clean = card_name.lower()

    # Nach Länge sortieren (damit z.B. "Mewtwo" vor "Mew" gematcht wird)
    for pokename in sorted(pokedex, key=len, reverse=True):
        pattern = r"\b" + re.escape(pokename) + r"\b"
        if re.search(pattern, card_name_clean):
            # Gibt den Namen sauber formatiert im Title Case zurück (z.B. "Charizard")
            return pokename.title()

    # Kein Match (Trainer, Energy etc.) -> leeres Feld
    return ""


# --- 3. Bulbapedia Scraper & CSV-Export ---
url = "https://bulbapedia.bulbagarden.net/wiki/Inferno_X_(TCG)"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

card_data = []
tables = soup.find_all("table")

for table in tables:
    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all(["td", "th"])
        cols_text = [ele.text.strip() for ele in cols if ele.text.strip()]

        if not cols_text:
            continue

        first_col = cols_text[0]

        if re.match(r"^\d+", first_col):
            card_number = first_col
            card_name_en = ""

            for text in cols_text[1:]:
                # Header & japanische Zeichen überspringen
                if text in [
                    "Card Name",
                    "English name",
                    "Type",
                    "Rarity",
                ] or re.search(r"[\u3040-\u30ff\u4e00-\u9faf]", text):
                    continue

                if len(text) >= 2:
                    card_name_en = text
                    break

            if card_name_en:
                pokemon_name = match_pokemon_from_pokedex(
                    card_name_en, pokedex_names
                )
                card_data.append([card_number, card_name_en, pokemon_name])

# --- 4. Export als CSV ---
df = pd.DataFrame(
    card_data, columns=["Card Number", "Card Name (EN)", "Pokemon Name (EN)"]
)
df = df.drop_duplicates(subset=["Card Number"])

if not df.empty:
    output_filename = "JP_Set_List_Pokedex.csv"
    df.to_csv(output_filename, index=False, encoding="utf-8-sig")
    print(
        f"Erfolg! {len(df)} Karten wurden in '{output_filename}' gespeichert."
    )
else:
    print("Keine Karten gefunden. Prüfe die Tabellenstruktur der URL.")