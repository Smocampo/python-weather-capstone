import os
import sqlite3
import pandas as pd

def clean_and_transform_data():
    csv_path = "data/raw_weather_data.csv"
    
    if not os.path.exists(csv_path):
        print("Error: 'raw_weather_data.csv' not found. Please run the scraper first.")
        return

    print("Loading raw data into Pandas DataFrame...")
    df = pd.read_csv(csv_path)
    
    clean_temps = []
    
    print("Cleaning temperature units and formatting data types...")
    for index, row in df.iterrows():
        raw_temp = str(row["Temperature"])
        
        just_digits = raw_temp.replace("°F", "").replace("°C", "").replace("°", "").strip()
        
        try:
            clean_temps.append(int(just_digits))
        except ValueError:
            clean_temps.append(None)

    df["Temperature"] = clean_temps
    
    # Drop rows missing numerical data and clear out duplicates to protect DB health
    df = df.dropna(subset=["Temperature"])
    df = df.drop_duplicates(subset=["City"])
    
    print("\nCleaned DataFrame Preview:")
    print(df)
    
    #SQLITE MIGRATION
    db_dir = "data"
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "weather_data.db")
    
    print("\nMigrating cleaned data to SQLite database...")
    conn = sqlite3.connect(db_path)
    
    # Write the clean DataFrame into an SQL table named 'world_cup_weather'
    df.to_sql("world_cup_weather", conn, if_exists="replace", index=False)
    conn.close()
    
    print("Migration complete! Saved to '" + db_path + "' in table 'world_cup_weather'.")

if __name__ == "__main__":
    clean_and_transform_data()