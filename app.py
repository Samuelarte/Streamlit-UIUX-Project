import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
import tweepy
import os
import time

# Initialize Pytrends
pytrends = TrendReq()

# Function to fetch Google Trends data
def get_google_trends(keywords, timeframe="today 7-d", geo="US"):
    try:
        if not keywords or not isinstance(keywords, list):
            raise ValueError("Keywords must be a non-empty list.")
        
        pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo=geo, gprop="")
        data = pytrends.interest_over_time()
        if data.empty:
            raise ValueError("No data found for the given keywords.")
        return data
    except Exception as e:
        raise ValueError(f"Error fetching Google Trends: {e}")

# Twitter API setup
api_key = st.secrets["TWITTER_API_KEY"]
api_key_secret = st.secrets["TWITTER_API_KEY_SECRET"]
access_token = st.secrets["TWITTER_ACCESS_TOKEN"]
access_token_secret = st.secrets["TWITTER_ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Function to fetch Twitter Trends
def get_twitter_trends(woeid=1):
    try:
        trends = api.get_place_trends(woeid)
        trends_data = [
            {"name": trend["name"], "tweet_volume": trend.get("tweet_volume", "N/A")}
            for trend in trends[0]["trends"]
        ]
        return trends_data
    except tweepy.TooManyRequests:
        raise RuntimeError("Twitter API rate limit reached. Please wait and try again.")
    except Exception as e:
        raise RuntimeError(f"Error fetching Twitter Trends: {e}")

# Streamlit App
st.title("Social Media and Search Trends Tracker")

# Google Trends Section
st.header("Google Search Trends")
keywords_input = st.text_input("Enter keywords (comma-separated, e.g., fashion, style):", "fashion, style")
timeframe = st.selectbox("Select Timeframe", ["today 7-d", "today 1-m", "today 3-m", "today 12-m", "all"])
geo = st.text_input("Enter Geo Code (default: US):", "US")

if st.button("Fetch Google Trends"):
    try:
        keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
        if not keywords:
            st.warning("Please enter at least one valid keyword.")
        else:
            with st.spinner("Fetching Google Trends data..."):
                google_data = get_google_trends(keywords, timeframe, geo)
                st.line_chart(google_data.drop(columns=["isPartial"]))
    except Exception as e:
        st.error(e)

# Twitter Trends Section
st.header("Twitter Trending Hashtags")
woeid = st.number_input("Enter WOEID (e.g., 1 for worldwide):", min_value=1, step=1, value=1)

if st.button("Fetch Twitter Trends"):
    try:
        with st.spinner("Fetching Twitter Trends..."):
            twitter_data = get_twitter_trends(woeid)
            df = pd.DataFrame(twitter_data)

            if not df.empty:
                # Display trends in a table
                st.dataframe(df)

                # Plot top trends by tweet volume
                st.subheader("Top Twitter Trends by Tweet Volume")
                df = df[df["tweet_volume"] != "N/A"]
                df = df.sort_values(by="tweet_volume", ascending=False).head(10)

                fig, ax = plt.subplots()
                ax.barh(df["name"], df["tweet_volume"], color="skyblue")
                ax.set_xlabel("Tweet Volume")
                ax.set_title("Top 10 Twitter Trends")
                st.pyplot(fig)
            else:
                st.warning("No trends found for the given WOEID.")
    except Exception as e:
        st.error(e)

# Optional: Add a data download feature
st.sidebar.header("Download Data")
if st.sidebar.button("Download Twitter Trends Data"):
    if "df" in locals():
        csv_data = df.to_csv(index=False)
        st.sidebar.download_button("Download CSV", csv_data, "twitter_trends.csv", "text/csv")
    else:
        st.sidebar.warning("No data available for download.")



