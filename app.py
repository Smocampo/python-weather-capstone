import sqlite3
import pandas as pd
import streamlit as st

# Set up page configurations
st.set_page_config(page_title="2026 World Cup Weather Dashboard", layout="wide")

# App Title & Header
st.title("⚽ 2026 World Cup Host Cities Weather Tracker")
st.markdown("""
    Welcome to the real-time weather monitoring dashboard for the **FIFA World Cup 2026** host cities across Canada, Mexico, and the United States. 
    This application pulls live-scraped data from a local SQLite database backend.
""")

# Connect to the SQLite database and extract data
def load_db_data():
    conn = sqlite3.connect("data/weather_data.db")
    query = "SELECT * FROM world_cup_weather"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

try:
    df = load_db_data()

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Filter Options")
    all_cities = sorted(df["City"].unique())
    selected_cities = st.sidebar.multiselect(
        "Select Cities to View:", 
        options=all_cities, 
        default=all_cities
    )

    # Filter DataFrame based on selection
    filtered_df = df[df["City"].isin(selected_cities)]

    # --- MAIN DASHBOARD LAYOUT ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📊 Structured Data View")
        # Display the data table
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    with col2:
        st.subheader("🌡️ Temperature Comparison (°F)")
        if not filtered_df.empty:
            # Create a simple, interactive native bar chart
            st.bar_chart(
                data=filtered_df, 
                x="City", 
                y="Temperature", 
                color="Condition",
                use_container_width=True
            )
        else:
            st.warning("Please select at least one city in the sidebar to display the chart.")

except Exception as e:
    st.error("Could not load data from database. Make sure you have run 'src/pipeline.py' to generate the data table first!")