import streamlit as st
import pandas as pd

def load_data(filename):
    data = pd.read_csv(filename)
    return data

# Load csv datasets
df_prod_copy = load_data('df_prod_copy.csv')
df_birch_wl_birch = load_data('cluster_list_wl.csv')
fwl_transformed = load_data('fwl_transformed.csv')

clusters_list_birch_foodprod = df_prod_copy[['Item', 'Cluster_Class']].sort_values(by='Cluster_Class').reset_index(drop=True)
clusters_list_birch_foodwl = df_birch_wl_birch[['Item', 'Cluster_Class']].sort_values(by='Cluster_Class').reset_index(drop=True)

st.title('Crop Analysis Overview')
st.header('Results from our Analysis')
st.image("crop_ana1.jpg", use_column_width=True)
st.image("cluster_results_fp.png", caption="Result of Clustering on FP Dataset", use_column_width=True)
st.image("cluster_results_fwl.png", caption="Result of Clustering on FWL Dataset", use_column_width=True)

#Recap on last shown dataset on FWL Dataset to further explain 
st.subheader('Recap on FWL Dataset')
main_df = pd.read_csv("fwl_transformed.csv")
st.dataframe(main_df)

st.image("overall_perf.png", caption="Model Performance Overview", use_column_width=True)

st.header('Crop Analysis')
selected_crop = st.selectbox('Choose a crop (all crops are from the FAOSTAT dataset):', df_birch_wl_birch['Item'].unique())

# clustering info based on selected crop
prod_cluster = clusters_list_birch_foodprod[clusters_list_birch_foodprod['Item'] == selected_crop]['Cluster_Class'].values[0]
prod_efficiency = {0: 'High production efficiency', 1: 'Low production efficiency', 2: 'Consistent Production Efficiency'}

wl_cluster = clusters_list_birch_foodwl[clusters_list_birch_foodwl['Item'] == selected_crop]['Cluster_Class'].values[0]
emission = {0: 'Moderate GHG level Emission', 1: 'High level GHG Emission', 2: 'Low GHG level Emission'}
utilisation = {0: '(1. Feed) (2. Import Quantity) (3. Loss) (4. Other Uses) (5. Processed)', 
               1: '(1. Feed) (2. Import Quantity) (3. Loss) (4. Processed) (5. Stock Variation)', 
               2: '(1. Loss) (2. Processed) (3. Stock Variation)'}



# Define function to get color based on the efficiency or emission level
def get_color_pe(cluster_num):
    if cluster_num == 0:
        return '#2ECC71'  # green
    elif cluster_num == 1:
        return '#E74C3C'  # red
    else:
        return '#F39C12'  # yellow

def get_color_fwl(cluster_num):
    if cluster_num == 0:
        return '#F39C12'  # yellow 
    elif cluster_num == 1: 
        return '#E74C3C'  # red        
    else:
        return '#2ECC71'  # green
        
    
def get_color_util(cluster_num):
    if cluster_num == 0:
        return '#2ECC71'  # red
    elif cluster_num == 1:
        return '#2ECC71'  # yellow
    else:
        return '#2ECC71'  # green

# Retrieve the production efficiency and GHG emission level descriptions
prod_val = prod_efficiency[prod_cluster]
emission_val = emission[wl_cluster]
util_val = utilisation[wl_cluster]

# Display the information using cards with color coding
st.markdown(f"""
<style>
    .info-card {{
        padding: 10px 20px;
        margin: 10px 0px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }}
</style>

<div class="info-card" style="background-color: {get_color_pe(prod_cluster)};">
    <h4>Production Efficiency for {selected_crop}</h4>
    <p>{prod_val}</p>
</div>

<div class="info-card" style="background-color: {get_color_fwl(wl_cluster)};">
    <h4>GHG Emission Level for {selected_crop}</h4>
    <p>{emission_val}</p>
</div>

<div class="info-card" style="background-color: {get_color_util(wl_cluster)};">
    <h4>Utilisation for {selected_crop}</h4>
    <p>{util_val}</p>
</div>
""", unsafe_allow_html=True)

# Display the dataset for the selected crop
selected_crop_data_fs = df_prod_copy[df_prod_copy['Item'] == selected_crop]
selected_crop_data_fwl = df_birch_wl_birch[df_birch_wl_birch['Item'] == selected_crop]
st.subheader(f'Data for {selected_crop}')
st.dataframe(selected_crop_data_fs)
st.write("Food Production Clustered Dataset")
st.write("")
st.dataframe(selected_crop_data_fwl)
st.write("FWL Clustered Dataset")
