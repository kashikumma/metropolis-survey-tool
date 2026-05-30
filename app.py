import streamlit as st
import requests
from streamlit_searchbox import st_searchbox

# --- CONFIG ---
st.set_page_config(page_title="Metropolis AI", layout="wide")

# --- SEARCH LOGIC ---
def search_address_api(search_term: str):
    """
    Fetches suggestions from Nominatim.
    We use a unique User-Agent that includes your app's name 
    to comply with their usage policy.
    """
    if not search_term or len(search_term) < 3:
        return[]
    
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": search_term,
        "format": "json",
        "limit": 5,
        "countrycodes": "us",
        "addressdetails": 1
    }
    # IMPORTANT: Change this to something unique to your project
    headers = {"User-Agent": "MetropolisGarageSurveyTool_v1_User"}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [item["display_name"] for item in data]
        else:
            return [f"Error: Server returned {response.status_code}"]
    except Exception as e:
        return [f"Search unavailable: {str(e)}"]

# --- UI ---
st.markdown("# 🅿️ Metropolis Market Intelligence")

selected_address = st_searchbox(
    search_function=search_address_api,
    placeholder="Start typing a US address...",
    key="addr_search"
)

if selected_address:
    st.write(f"Selected: {selected_address}")
