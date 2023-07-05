import streamlit as st
import pandas as pd
from streamlit_folium import folium_static, st_folium
import folium
from folium.plugins import Draw
import numpy as np

MP = [-33.867127376303834, 151.21005889816965]

@st.cache_data
def data_load():
    df = pd.read_csv('data/data.csv')
    df = df.dropna()
    return df

def layout_config():
    st.set_page_config(
     page_title="Eats of MP",
     page_icon=":tada:",
     layout="wide",
     initial_sidebar_state="expanded",
    )
    hide_streamlit_style = """
	    <style>
	    /* This is to hide Streamlit footer */
	    footer {visibility: hidden;}
	    </style>
    """
    st.markdown("""<style>
	    /* This is to hide Streamlit footer */
	    footer {visibility: hidden;}
	    </style>""", unsafe_allow_html=True)

def sidebar_config():
    with st.sidebar:
        st.write("Welcome to the Eats of MP Map Integration! Still being developed and worked through so feel free to post any suggestions.")
        st.divider()

def map_setups(data, names_selected):
    st.write("Select the sidebar list of options you'd like to view on the map!")
    map = folium.Map(location = MP, zoom_start = 14)
    folium.TileLayer('OpenStreetMap').add_to(map)
    folium.Marker(MP, marker_icon = "cloud", color = 'red').add_to(map)

    fg = folium.FeatureGroup(name="dine data")
    filtered_df = data[data['name'].isin(names_selected)]

    for d in filtered_df.itertuples():
        fg.add_child(
            folium.Marker(
                location=[d.lat, d.lon],
                popup=f"{d.name}, {d.address}, {d.phone}",
                tooltip=f"{d.name}",
                icon=folium.Icon(color="green")
        )
        )

    Draw(export=True).add_to(map)
    
    out = st_folium(
        map,
        feature_group_to_add=fg,
        width=1200,
        height=800,
        )    

def main():
    layout_config()
    sidebar_config()

    st.title("Eats of MP Tracker")
    st.divider()

    df = data_load()
    names_list = df['name'].unique().tolist()
    name_selected = st.sidebar.multiselect("What places do you want on the map?", names_list)

    map_setups(df, name_selected)

    st.divider()


    with st.expander("Total List of Places Below!"):
        st.dataframe(df)





if __name__ == "__main__":
    main()