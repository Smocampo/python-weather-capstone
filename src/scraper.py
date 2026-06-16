import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Hardcoded direct URL paths for the 16 World Cup host cities on timeanddate.com
C_URLS = {
    "Atlanta": "usa/atlanta", "Boston": "usa/boston", "Dallas": "usa/dallas",
    "Houston": "usa/houston", "Kansas City": "usa/kansas-city", "Los Angeles": "usa/los-angeles",
    "Miami": "usa/miami", "New York": "usa/new-york", "Philadelphia": "usa/philadelphia",
    "San Francisco": "usa/san-francisco", "Seattle": "usa/seattle", "Guadalajara": "mexico/guadalajara",
    "Mexico City": "mexico/mexico-city", "Monterrey": "mexico/monterrey", "Toronto": "canada/toronto",
    "Vancouver": "canada/vancouver"
}

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_weather():
    driver = setup_driver()
    scraped_rows = []
    
    print("Starting direct city weather scraping loop...")
    
    for city, path in C_URLS.items():
        url = "https://www.timeanddate.com/weather/" + path
        print("Scraping " + city + "...")
        
        try:
            driver.get(url)
            time.sleep(1.5) 
            
            qlook = driver.find_element(By.ID, "qlook")
            
            temp_text = qlook.find_element(By.CLASS_NAME, "h2").text.strip()
            
        
            condition_text = qlook.find_element(By.TAG_NAME, "p").text.strip()
            
            scraped_rows.append({
                "City": city,
                "Temperature": temp_text,
                "Condition": condition_text
            })
            print("Successfully fetched: " + city + " -> " + temp_text + ", " + condition_text)
            
        except Exception as e:
            print("Could not fetch data for " + city + ". Skipping.")
            continue

    driver.quit()
    
    if scraped_rows:
        df = pd.DataFrame(scraped_rows)
        os.makedirs("data", exist_ok=True)
        csv_path = "data/raw_weather_data.csv"
        df.to_csv(csv_path, index=False)
        print("\nSuccess! Saved updated data to {}".format(csv_path))
    else:
        print("\nNo data rows extracted. Please check network connection.")

if __name__ == "__main__":
    scrape_weather()