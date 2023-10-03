
import streamlit as st
import pandas as pd

def load_data(filename):
    data = pd.read_csv(filename)
    return data

# Load csv datasets
df_prod_copy = load_data('df_prod_copy.csv')
df_birch_wl_birch = load_data('df_birch_wl_birch.csv')
fwl_transformed = load_data('fwl_transformed.csv')

def show_crop_analysis(df_birch_wl_birch, clusters_list_birch_foodprod, clusters_list_birch_foodwl):
    st.header('Crop Analysis')
    st.write('Note: These crops are from FAOSTAT')
    selected_crop = st.selectbox('Choose a crop:', df_birch_wl_birch['Item'].unique())
    
    # Display clustering info based on selected crop
    prod_cluster = clusters_list_birch_foodprod[clusters_list_birch_foodprod['Item'] == selected_crop]['Cluster_Class'].values[0]
    prod_efficiency = {0: 'High production efficiency', 1: 'Low production efficiency', 2: 'Consistent Production Efficiency'}
    st.write(f"Production efficiency for ({selected_crop}) : {prod_efficiency[prod_cluster]}")
    
    wl_cluster = clusters_list_birch_foodwl[clusters_list_birch_foodwl['Item'] == selected_crop]['Cluster_Class'].values[0]
    emission = {0: 'High GHG level Emission', 1: 'Moderate level GHG Emission', 2: 'Low level GHG Emission'}
    st.write(f"GHG emission level for ({selected_crop}) : {emission[wl_cluster]}")
