import sqlite3
import pandas as pd
import streamlit as st

# PAGE CONFIGURATION 
st.set_page_config(
    page_title="2026 World Cup Host Cities Weather Dashboard",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ 2026 World Cup Host Cities Dashboard")
st.markdown("""
Welcome to the official 2026 World Cup Host Cities Explorer! This dashboard combines real-time scraped weather metrics 
with city profiles directly from our database to help fans plan their tournament trips.
""")

# DATABASE INTEGRATION 
def load_data():
    conn = sqlite3.connect("data/weather_data.db")
    
    # Read both tables
    df_weather = pd.read_sql_query("SELECT * FROM world_cup_weather", conn)
    df_metadata = pd.read_sql_query("SELECT * FROM city_metadata", conn)
    
    conn.close()
    
    # Merge on City to create a relational dataset
    merged_df = pd.merge(df_weather, df_metadata, on="City", how="inner")
    return merged_df

try:
    df = load_data()
    
    # SIDEBAR FILTERS
    st.sidebar.header("Filter Options")
    countries = ["All"] + list(df["Country"].unique())
    selected_country = st.sidebar.selectbox("Select a Country:", countries)
    
    if selected_country != "All":
        filtered_df = df[df["Country"] == selected_country]
    else:
        filtered_df = df

    # METRIC CARDS
    st.subheader("📊 Quick Metrics Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Host Cities Displayed", value=len(filtered_df))
    with col2:
        st.metric(label="Average Temperature", value=f"{round(filtered_df['Temperature'].mean(), 1)}°F")
    with col3:
        st.metric(label="Hottest City Selected", value=f"{filtered_df.loc[filtered_df['Temperature'].idxmax(), 'City']} ({filtered_df['Temperature'].max()}°F)")

    st.markdown("---")

    # VISUALIZATION 1: TEMPERATURE BAR CHART
    st.subheader("🌡️ Visual 1: Current Temperatures by Host City")
    st.markdown("Compare the varying climates across the selected tournament locations.")
    
    # Sort data for better visual layout
    chart_data = filtered_df.sort_values(by="Temperature", ascending=False)
    st.bar_chart(data=chart_data, x="City", y="Temperature", use_container_width=True)

    # VISUALIZATIONS 2 & 3: TWO-COLUMN LAYOUT
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("🌎 Visual 2: Country Distribution")
        st.markdown("Proportion of matches/cities across North America in this selection.")
        country_counts = filtered_df["Country"].value_counts()
        st.bar_chart(country_counts)

    with col_right:
        st.subheader("📋 Visual 3: Weather Condition Breakdowns")
        st.markdown("See what sky conditions dominate your selected matching cities.")
        condition_counts = filtered_df["Condition"].value_counts()
        st.line_chart(condition_counts)

    st.markdown("---")

    # INTERACTIVE DATA TABLE
    st.subheader("🔍 Explore the Complete Database Relational Records")
    st.markdown("Use the columns below to sort, scan, and view stadium metadata linked alongside real-time conditions.")
    st.dataframe(filtered_df[["City", "Country", "Stadium", "Temperature", "Condition"]], use_container_width=True)

except Exception as e:
    st.error(f"Could not load database records: {e}")
    st.warning("Please ensure your data processing pipeline script has been run and 'data/weather_data.db' exists with data.")