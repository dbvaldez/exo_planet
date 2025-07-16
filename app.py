import streamlit as st
from data_fetcher import fetch_exoplanets

st.set_page_config(page_title="ExoExplorer", layout="wide", page_icon="🪐")

st.title("🪐 ExoExplorer: Discover Exoplanets")
st.markdown("Explore real-time data from NASA's Exoplanet Archive. Filter planets by orbital period, size, and more!")

# Fetch data with caching
df = fetch_exoplanets()

if df.empty:
    st.warning("No exoplanet data available. Please try again later.")
else:
    # Sidebar filters
    st.sidebar.header("🔍 Filter Planets")

    # Orbital period filter
    orbital_period = st.sidebar.slider("Orbital Period (days)", 0, int(df['pl_orbper'].max()), (0, 500))

    # Radius filter
    radius = st.sidebar.slider("Planet Radius (Earth radii)", 0.0, float(df['pl_rade'].max()), (0.0, 10.0))

    # Apply filters
    filtered_df = df[
        (df['pl_orbper'] >= orbital_period[0]) & (df['pl_orbper'] <= orbital_period[1]) &
        (df['pl_rade'] >= radius[0]) & (df['pl_rade'] <= radius[1])
    ]

    st.subheader("🔭 Filtered Exoplanets")
    st.dataframe(filtered_df, use_container_width=True)

    st.markdown(f"Showing **{len(filtered_df)}** planets based on selected criteria.")
