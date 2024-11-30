import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import folium_static

st.title("My UI/UX Design Project")

# Sidebar Navigation
menu = st.sidebar.radio("Menu", ["Home", "Interactive Charts", "Map", "Feedback"])

# Home Page
if menu == "Home":
    st.header("Welcome to Our Web Application!")
    st.write("This application is designed to showcase the principles of HCI.")
    st.info("Navigate through the sidebar to explore features.")

# Interactive Charts
elif menu == "Interactive Charts":
    st.header("Charts and Visualizations")
    data = {
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "Visitors": [50, 70, 90, 100, 120],
    }
    df = pd.DataFrame(data)
    st.line_chart(df.set_index("Day"))
    st.bar_chart(df.set_index("Day"))

# Map Page
elif menu == "Map":
    st.header("Map Visualization")
    m = folium.Map(location=[25.7617, -80.1918], zoom_start=10)
    folium.Marker([25.7617, -80.1918], tooltip="Location").add_to(m)
    folium_static(m)

# Feedback Page
elif menu == "Feedback":
    st.header("Your Feedback")
    feedback = st.text_area("Let us know your thoughts!")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")

