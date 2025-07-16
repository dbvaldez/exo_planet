import pandas as pd
from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive
import streamlit as st

@st.cache_data
def fetch_exoplanets():
    try:
        # Verified column names from the PS table
        df = NasaExoplanetArchive.query_criteria(
            table="ps",
            select="pl_name,pl_orbper,pl_rade,pl_bmasse,pl_orbeccen,st_dist"
        )
        return df.to_pandas()
    except Exception as e:
        st.error("🚨 Failed to fetch exoplanet data. Please check your query or try again later.")
        st.exception(e)
        return pd.DataFrame()
