import streamlit as st

def show_map(volunteers_df):

    if volunteers_df.empty:
        st.warning("No volunteers to display on map")
        return

    volunteers_df["lat"] = 17.3850
    volunteers_df["lon"] = 78.4867

    st.map(volunteers_df[["lat","lon"]])