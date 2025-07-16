# app.py
import streamlit as st
from data_fetcher import fetch_exoplanets

st.set_page_config(page_title="ExoExplorer", layout="wide")
st.title("🪐 ExoExplorer: Discover Exoplanets")

df = fetch_exoplanets()
st.dataframe(df)

st.sidebar.header("Filter Options")
orbital_period = st.sidebar.slider("Orbital Period (days)", 0, 1000, (0, 500))
filtered_df = df[(df['pl_orbper'] >= orbital_period[0]) & (df['pl_orbper'] <= orbital_period[1])]
st.write("### Filtered Results")
st.dataframe(filtered_df)
