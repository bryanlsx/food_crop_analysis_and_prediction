import streamlit as st
import pandas as pd

def load_data(filename):
    data = pd.read_csv(filename)
    return data

# Load csv datasets
df_prod_copy = load_data('df_prod_copy.csv')
df_birch_wl_birch = load_data('df_birch_wl_birch.csv')
fwl_transformed = load_data('fwl_transformed.csv')

clusters_list_birch_foodprod = df_prod_copy[['Item', 'Cluster_Class']].sort_values(by='Cluster_Class').reset_index(drop=True)
clusters_list_birch_foodwl = df_birch_wl_birch[['Item', 'Cluster_Class']].sort_values(by='Cluster_Class').reset_index(drop=True)

# Streamlit UI
st.title('Crop Analysis Overview')
st.header('Results from our Analysis')
st.image("cluster_img_food_sec.png", caption="Cluster for Food Security", use_column_width=True)
st.image("cluster_img_food_wl.png", caption="Cluster for Food Waste & Loss", use_column_width=True)
st.image("performance_measure.png", caption="Performance Measure of Attempted Models", use_column_width=True)

st.header('Crop Analysis')
selected_crop = st.selectbox('Choose a crop (all crops are from the FAOSTAT dataset):', df_birch_wl_birch['Item'].unique())

# Display clustering info based on selected crop
prod_cluster = clusters_list_birch_foodprod[clusters_list_birch_foodprod['Item'] == selected_crop]['Cluster_Class'].values[0]
prod_efficiency = {0: 'High production efficiency', 1: 'Low production efficiency', 2: 'Consistent Production Efficiency'}
st.write(f"Production efficiency for <{selected_crop}> : {prod_efficiency[prod_cluster]}")

wl_cluster = clusters_list_birch_foodwl[clusters_list_birch_foodwl['Item'] == selected_crop]['Cluster_Class'].values[0]
emission = {0: 'Moderate GHG level Emission', 1: 'High level GHG Emission', 2: 'Low level GHG Emission'}
st.write(f"GHG emission level for <{selected_crop}> : {emission[wl_cluster]}")

