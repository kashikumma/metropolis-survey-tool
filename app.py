import streamlit as st
import pandas as pd
import io
import requests
from streamlit_searchbox import st_searchbox

# --- PAGE CONFIG ---
st.set_page_config(page_title="Metropolis AI", layout="wide", page_icon="🅿️")

# --- GEOSPATIAL SEARCH LOGIC (USA ONLY) ---
def search_address_api(search_term: str):
    """Fetches suggestions from OpenStreetMap Nominatim restricted to the USA."""
    if not search_term or len(search_term) < 3:
        return[]
    
    url = "https://nominatim.openstreetmap.org/search"
    # countrycodes="us" restricts the results to the United States
    params = {
        "q": search_term, 
        "format": "json", 
        "limit": 5, 
        "countrycodes": "us"
    }
    headers = {"User-Agent": "MetropolisMarketIntelligence/1.0"}
    
    try:
        response = requests.get(url, params=params, headers=headers).json()
        return [item["display_name"] for item in response]
    except Exception:
        return[]

# --- UI INTERFACE ---
st.markdown("# 🅿️ Metropolis Market Intelligence")
st.markdown("### Automated competitive garage survey tool.")

# Search-as-you-type Box
selected_address = st_searchbox(
    search_function=search_address_api,
    placeholder="Start typing a US address...",
    key="addr_search"
)

# --- SURVEY PIPELINE ---
if selected_address:
    st.success(f"Targeting: {selected_address}")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        radius = st.slider("Survey Radius (Miles)", 1, 10, 5)
    
    if st.button("⚡ Execute Survey Pipeline", type="primary"):
        with st.spinner("Analyzing market data..."):
            # This is where your backend data logic goes
            # Mock data for demonstration:
            mock_results = {
                "Garage A": {"address": selected_address, "rates": {"1 hr": 15.00, "2 hr": 25.00}},
                "Garage B": {"address": "Nearby Garage", "rates": {"1 hr": 18.00, "2 hr": 28.00}}
            }
            st.session_state.results = mock_results
            st.success("Extraction Complete!")

# --- DISPLAY & EXPORT ---
if "results" in st.session_state:
    st.subheader("Extracted Market Entities")
    df = pd.DataFrame.from_dict(st.session_state.results, orient='index')
    st.dataframe(df, use_container_width=True)
    
    # Placeholder for Excel generation logic
    st.info("Download buttons would appear here once Excel engine is linked.")
