import os
import sqlite3
import pandas as pd

def clean_and_transform_data():
    csv_path = "data/raw_weather_data.csv"
    
    if not os.path.exists(csv_path):
        print("Error: 'raw_weather_data.csv' not found. Please run the scraper first.")
        return

    print("=== STAGE 1: LOADING RAW DATA ===")
    df = pd.read_csv(csv_path)
    
    # --- BEFORE SNAPSHOT ---
    print("\n[BEFORE CLEANING] Raw DataFrame Snapshot:")
    print("Total rows pulled from scraper: {}".format(len(df)))
    print(df.head())
    print("-" * 40)
    
    clean_temps = []
    
    print("\n=== STAGE 2: DATA CLEANING & TRANSFORMATION ===")
    print("Stripping temperature units, changing data types to integers...")
    
    for index, row in df.iterrows():
        raw_temp = str(row["Temperature"])
        just_digits = raw_temp.replace("°F", "").replace("°C", "").replace("°", "").strip()
        
        try:
            clean_temps.append(int(just_digits))
        except ValueError:
            clean_temps.append(None)

    # Apply transformations
    df["Temperature"] = clean_temps
    
    # Drop rows missing numerical data and clear out duplicates
    df = df.dropna(subset=["Temperature"])
    df = df.drop_duplicates(subset=["City"])
    
   
    print("\n[AFTER CLEANING] Transformed DataFrame Snapshot:")
    print("Total rows after removing missing/duplicate data: {}".format(len(df)))
    print(df.head())
    print("-" * 40)
    
    # --- SQLITE MIGRATION ---
    print("\n=== STAGE 3: SQLITE DATABASE MIGRATION ===")
    db_dir = "data"
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "weather_data.db")
    
    print("Migrating clean table to SQLite database...")
    conn = sqlite3.connect(db_path)
    df.to_sql("world_cup_weather", conn, if_exists="replace", index=False)
    conn.close()
    
    print("Migration complete! Saved to '" + db_path + "' in table 'world_cup_weather'.")

if __name__ == "__main__":
    clean_and_transform_data()