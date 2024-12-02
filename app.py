import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq

# Initialize Pytrends
pytrends = TrendReq()

# Function to fetch Google Trends data
def get_google_trends(keywords, timeframe="today 1-m"):
    try:
        if not keywords or not isinstance(keywords, list):
            raise ValueError("Keywords must be a non-empty list.")
        
        pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo="US", gprop="")
        data = pytrends.interest_over_time()

        if data.empty:
            raise ValueError("No data found for the given keywords.")
        return data
    except Exception as e:
        raise ValueError(f"Error fetching Google Trends: {e}")

# Map user-friendly names to Pytrends timeframes
timeframe_mapping = {
    "Monthly": "today 1-m",
    "Quarterly": "today 3-m",
    "Yearly": "today 12-m",
    "All Time": "all"
}

# Streamlit App
st.title("Google Trends Tracker")

# Google Trends Section
st.header("Google Search Trends")

# Keywords input
keywords_input = st.text_input("Enter keywords (comma-separated, e.g., fashion, style):", "fashion, style")

# Timeframe options (user-friendly)
timeframe_label = st.selectbox(
    "Select Timeframe", 
    ["Monthly", "Quarterly", "Yearly", "All Time"], 
    index=0  # Default to Monthly
)

# Map the selected label to the Pytrends timeframe
timeframe = timeframe_mapping[timeframe_label]

# Widgets: Slider to adjust the number of rows displayed
num_rows = st.slider("Number of rows to display (For raw data)", min_value=1, max_value=50, value=10, step=1)

# Checkbox to show/hide raw data
show_raw_data = st.checkbox("Show Raw Data")

# Button to fetch Google Trends data
if st.button("Fetch Google Trends"):
    try:
        keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
        if not keywords:
            st.warning("Please enter at least one valid keyword.")
        else:
            with st.spinner("Fetching Google Trends data..."):
                google_data = get_google_trends(keywords, timeframe)
                if not google_data.empty:
                    st.success("Google Trends data fetched successfully!")

                    # Display line chart
                    st.line_chart(google_data.drop(columns=["isPartial"], errors="ignore"))

                    # Display data in a table if checkbox is checked
                    if show_raw_data:
                        st.subheader("Raw Google Trends Data")
                        st.dataframe(google_data.head(num_rows))
                else:
                    st.warning("No data found for the entered keywords.")
    except Exception as e:
        st.error(e)

# Optional: Add a data download feature
st.sidebar.header("Download Data")
if st.sidebar.button("Download Google Trends Data"):
    try:
        keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
        google_data = get_google_trends(keywords, timeframe)
        if not google_data.empty:
            csv_data = google_data.to_csv(index=True)
            st.sidebar.download_button("Download CSV", csv_data, "google_trends_data.csv", "text/csv")
        else:
            st.sidebar.warning("No data available for download.")
    except Exception as e:
        st.sidebar.error(e)