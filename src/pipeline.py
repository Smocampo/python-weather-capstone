import os
import sqlite3
import pandas as pd

def clean_and_transform_data():
    weather_csv = "data/raw_weather_data.csv"
    info_csv = "data/host_cities_info.csv"
    
    if not os.path.exists(weather_csv) or not os.path.exists(info_csv):
        print("Error: Missing required CSV files in data/ directory.")
        return

    # --- TABLE 1: WEATHER DATA ---
    print("=== TABLE 1: PROCESSING WEATHER DATA ===")
    df_weather = pd.read_csv(weather_csv)
    
    print("\n[BEFORE CLEANING] Weather Data Rows: {}".format(len(df_weather)))
    
    clean_temps = []
    for index, row in df_weather.iterrows():
        raw_temp = str(row["Temperature"])
        just_digits = raw_temp.replace("°F", "").replace("°C", "").replace("°", "").strip()
        try:
            clean_temps.append(int(just_digits))
        except ValueError:
            clean_temps.append(None)

    df_weather["Temperature"] = clean_temps
    df_weather = df_weather.dropna(subset=["Temperature"]).drop_duplicates(subset=["City"])
    
    print("\n[AFTER CLEANING] Weather Data Snapshot:")
    print(df_weather.head(3))
    print("-" * 40)
    
    # --- TABLE 2: CITY METADATA ---
    print("\n=== TABLE 2: PROCESSING CITY METADATA ===")
    df_info = pd.read_csv(info_csv)
    
    print("\n[BEFORE CLEANING] Info Rows: {}".format(len(df_info)))
    df_info = df_info.drop_duplicates(subset=["City"]).dropna()
    
    print("\n[AFTER CLEANING] City Metadata Snapshot:")
    print(df_info.head(3))
    print("-" * 40)
    
    # --- SQLITE MIGRATION ---
    print("\n=== STAGE 3: MULTI-TABLE SQLITE MIGRATION ===")
    db_path = "data/weather_data.db"
    conn = sqlite3.connect(db_path)
    
    # Saving into separate tables
    print("Writing 'world_cup_weather' table...")
    df_weather.to_sql("world_cup_weather", conn, if_exists="replace", index=False)
    
    print("Writing 'city_metadata' table...")
    df_info.to_sql("city_metadata", conn, if_exists="replace", index=False)
    
    conn.close()
    print("\nSuccess! Both CSVs imported into separate tables in '{}'!".format(db_path))

if __name__ == "__main__":
    clean_and_transform_data()