# data_fetcher.py
import pandas as pd
from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive

def fetch_exoplanets():
    df = NasaExoplanetArchive.query_criteria(table="ps", select="pl_name,pl_orbper,pl_rade,pl_bmasse,pl_orbeccen,st_dist")
    return df.to_pandas()
