import streamlit as st
import pandas as pd
from data_fetcher import fetch_exoplanets
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 🚀 Configure Streamlit page
st.set_page_config(page_title="ExoExplorer", layout="wide", page_icon="🪐")
st.title("🪐 ExoExplorer: Discover Exoplanets")
st.markdown("Explore real-time data from NASA's Exoplanet Archive. Filter, search, visualize, and explore planetary habitability!")

# 🧠 Load data
df = fetch_exoplanets()

# 🧮 Define habitability scoring logic
def habitability_score(row):
    score = 0
    if 0.5 <= row['pl_rade'] <= 2.5:
        score += 1
    if 0.1 <= row['pl_bmasse'] <= 10:
        score += 1
    if 50 <= row['pl_orbper'] <= 500:
        score += 1
    return score

if df.empty:
    st.warning("No exoplanet data available. Please try again later.")
else:
    # 🎛️ Sidebar Filters
    st.sidebar.header("🎛️ Filter Planets")
    orbital_period = st.sidebar.slider("Orbital Period (days)", 0, int(df['pl_orbper'].dropna().max()), (0, 500))
    radius = st.sidebar.slider("Planet Radius (Earth radii)", 0.0, float(df['pl_rade'].dropna().max()), (0.0, 10.0))
    planet_name = st.sidebar.text_input("🔍 Search Planet by Name")

    filtered_df = df[
        (df['pl_orbper'] >= orbital_period[0]) & (df['pl_orbper'] <= orbital_period[1]) &
        (df['pl_rade'] >= radius[0]) & (df['pl_rade'] <= radius[1])
    ]

    if planet_name:
        filtered_df = filtered_df[filtered_df['pl_name'].str.contains(planet_name, case=False, na=False)]

    filtered_df["Habitability Score"] = filtered_df.apply(habitability_score, axis=1)

    # 🔭 Display Filtered Results
    st.subheader("🔭 Filtered Exoplanets")
    st.dataframe(filtered_df, use_container_width=True)
    st.markdown(f"Showing **{len(filtered_df)}** planets based on selected criteria.")

    # 📈 Radius vs Mass Plot
    st.subheader("📈 Radius vs Mass")
    if 'pl_rade' in filtered_df.columns and 'pl_bmasse' in filtered_df.columns:
        fig = px.scatter(
            filtered_df.dropna(subset=['pl_rade', 'pl_bmasse']),
            x="pl_rade",
            y="pl_bmasse",
            hover_name="pl_name",
            labels={"pl_rade": "Radius (Earth radii)", "pl_bmasse": "Mass (Earth masses)"},
            title="Planet Radius vs Mass"
        )
        st.plotly_chart(fig, use_container_width=True)

    # 🧬 Stellar System Clustering
    st.subheader("🌌 Stellar System Clustering (Experimental)")
    clustering_df = filtered_df[["pl_orbper", "pl_rade", "pl_bmasse"]].dropna()
    if len(clustering_df) >= 3:
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(clustering_df)
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(scaled_features)
        clustering_df["Cluster"] = clusters

        fig_cluster = px.scatter_3d(
            clustering_df,
            x="pl_orbper",
            y="pl_rade",
            z="pl_bmasse",
            color="Cluster",
            title="🧬 Exoplanet Clusters by Traits",
            labels={"pl_orbper": "Orbital Period", "pl_rade": "Radius", "pl_bmasse": "Mass"}
        )
        st.plotly_chart(fig_cluster, use_container_width=True)
    else:
        st.info("Not enough data to perform clustering. Try adjusting the filters.")

    # 🧮 Habitability Table
    st.subheader("🧮 Habitability Scores")
    st.dataframe(filtered_df[["pl_name", "pl_rade", "pl_bmasse", "pl_orbper", "Habitability Score"]])

    # 🌍 Planet Gallery
    st.subheader("🌍 Planet Gallery")
    st.image([
        "https://images-assets.nasa.gov/image/PIA00343/PIA00343~thumb.jpg",
        "https://images-assets.nasa.gov/image/PIA02963/PIA02963~thumb.jpg",
        "https://images-assets.nasa.gov/image/PIA02879/PIA02879~thumb.jpg"
    ], caption=["Earth", "Mars", "Jupiter"], width=300)

    # 🚀 Mission Logos
    st.subheader("🚀 Mission Logos")
    st.image([
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/NASA_logo.svg/1024px-NASA_logo.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/NASA_Worm_logo.svg/1024px-NASA_Worm_logo.svg.png"
    ], caption=["NASA Meatball", "NASA Worm"], width=200)
