import os
import re
from pathlib import Path  
from bs4 import BeautifulSoup
import pandas as pd

import requests
from dotenv import load_dotenv

# --- 1. `.env`-Datei laden ---
SCRIPT_DIR = Path(__file__).resolve().parent
ENV_PATH = SCRIPT_DIR / ".." / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# --- EINSTELLUNGEN FÜR DES AKTUELLE SET ---
SET_ID = "M2"  # Hier die Set-ID manuell eintragen
URL = "https://bulbapedia.bulbagarden.net/wiki/Inferno_X_(TCG)"

raw_set_name = URL.split("wiki/")[-1]
set_name_clean = re.sub(r"_\(TCG\)$", "", raw_set_name)



# --- 1. Bulbapedia Scraper & CSV-Export ---
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
response = requests.get(URL, headers=headers)
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

        # Prüft, ob die erste Spalte mit einer Kartennummer beginnt (z. B. 001/165)
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
                # Fügt jetzt direkt die SET_ID als erste Spalte hinzu
                card_data.append([SET_ID, card_number, card_name_en])
# --- 2. Export als CSV ---
df = pd.DataFrame(
    card_data, columns=["set_id", "card_number", "card_name_en"]
)
df = df.drop_duplicates(subset=["card_number"])

if not df.empty:
    output_filename = f"JP_Set_List_{set_name_clean}.csv"
    output_path = SCRIPT_DIR / ".." / "CSV" / output_filename
    
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(
        f"Erfolg! {len(df)} Karten wurden in '{output_path.resolve()}' gespeichert."
    )
else:
    print("Keine Karten gefunden. Prüfe die Tabellenstruktur der URL.")