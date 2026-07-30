import os
import re
import pandas as pd
import psycopg2
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# --- 1. `.env`-Datei laden ---
load_dotenv()

# --- EINSTELLUNGEN FÜR DES AKTUELLE SET ---
SET_ID = "SV2a"  # Hier die Set-ID manuell eintragen
URL = "https://bulbapedia.bulbagarden.net/wiki/Pokemon_Card_151_(TCG)"


# --- 2. PostgreSQL Verbindung via ENV-Variablen ---
print("Verbinde mit PostgreSQL über Umgebungsvariablen...")

try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),  # Fallback auf localhost
        port=os.getenv("DB_PORT", "5432"),  # Fallback auf 5432
    )

    cursor = conn.cursor()
    cursor.execute("SELECT pokemon_name FROM pokedex;")
    db_rows = cursor.fetchall()
    cursor.close()
    conn.close()

    pokedex_names = {row[0].strip().lower() for row in db_rows if row[0]}
    print(
        f"Erfolg: {len(pokedex_names)} Pokémon-Namen aus '{os.getenv('DB_NAME')}' geladen.\n"
    )

except Exception as e:
    print(f"Fehler bei der Datenbankverbindung: {e}")
    exit()


# --- 3. Hilfsfunktion: Pokedex-Matching ---
def match_pokemon_from_pokedex(card_name, pokedex):
    card_name_clean = card_name.lower()
    for pokename in sorted(pokedex, key=len, reverse=True):
        pattern = r"\b" + re.escape(pokename) + r"\b"
        if re.search(pattern, card_name_clean):
            return pokename.title()
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