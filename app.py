import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
import tweepy
import os

# Initialize Pytrends
pytrends = TrendReq()

# Function to fetch Google Trends data
def get_google_trends(keywords, timeframe="today 7-d", geo="US"):
    pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo=geo, gprop="")
    data = pytrends.interest_over_time()
    return data

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
    trends = api.get_place_trends(woeid)
    trends_data = [{"name": trend["name"], "tweet_volume": trend.get("tweet_volume", "N/A")} for trend in trends[0]["trends"]]
    return trends_data

# Streamlit App
st.title("Social Media and Search Trends Tracker")

# Google Trends Section
st.header("Google Search Trends")
keywords = st.text_input("Enter keywords (comma-separated, e.g., fashion, style):", "fashion, style")
if st.button("Fetch Google Trends"):
    try:
        keyword_list = [k.strip() for k in keywords.split(",")]
        google_data = get_google_trends(keyword_list)

        if not google_data.empty:
            st.line_chart(google_data.drop(columns=["isPartial"]))
        else:
            st.warning("No data found for the entered keywords.")
    except Exception as e:
        st.error(f"Error fetching Google Trends: {e}")

# Twitter Trends Section
st.header("Twitter Trending Hashtags")
woeid = st.number_input("Enter WOEID (e.g., 1 for worldwide):", min_value=1, step=1, value=1)
if st.button("Fetch Twitter Trends"):
    try:
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
            ax.barh(df["name"], df["tweet_volume"])
            ax.set_xlabel("Tweet Volume")
            ax.set_title("Top 10 Twitter Trends")
            st.pyplot(fig)
        else:
            st.warning("No trends found for the given WOEID.")
    except Exception as e:
        st.error(f"Error fetching Twitter Trends: {e}")


