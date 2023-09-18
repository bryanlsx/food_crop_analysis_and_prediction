import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pickle

st.set_page_config(page_title="Deployment", page_icon="🐨")

# Load models
with open('foodprod_model.pkl', 'rb') as f:
    birch = pickle.load(f)
with open('foodwaste_model.pkl', 'rb') as f:
    birch_fwl = pickle.load(f)

scaler = StandardScaler()

def load_data(filename):
    data = pd.read_csv(filename)
    return data

# Load csv datasets
df_prod_copy = load_data('df_prod_copy.csv')
df_birch_wl_birch = load_data('df_birch_wl_birch.csv')
fwl_transformed = load_data('fwl_transformed.csv')

clusters_list_birch_foodprod = df_prod_copy[['Item', 'Cluster_Class']].sort_values(by='Cluster_Class').reset_index(drop=True)
clusters_list_birch_foodwl = df_birch_wl_birch[['Item', 'Cluster_Class']].sort_values(by='Cluster_Class').reset_index(drop=True)

def food_security_prediction(user_input):
    df_temp = df_prod_copy.copy()
    df_temp.loc[df_temp.shape[0]] = user_input
    scaled_data = scaler.fit_transform(df_temp[['Area harvested', 'Production']])
    prediction = birch.predict(scaled_data)
    cluster = prediction[-1]  # taking the prediction for the last row which is our input
    efficiency = {0: 'High production efficiency', 1: 'Low production efficiency', 2: 'Consistent production efficiency'}
    return f"a predicted <u>**{efficiency[cluster]}**</u>"

def food_waste_prediction(user_input, crop_name):
    df_temp = fwl_transformed.copy()
    df_temp.loc[df_temp.shape[0]] = user_input
    selected_columns = df_temp.iloc[:, [2, 3, 4, 5, 6, 8, 9]]
    scaled_data = StandardScaler().fit_transform(selected_columns)
    pca = PCA(n_components=2)
    transformed_data = pca.fit_transform(scaled_data)
    prediction = birch_fwl.predict(transformed_data)
    cluster = prediction[-1]  # taking the prediction for the last row which is our input
    emission = {0: 'high GHG Emission level', 1: 'moderate Level GHG Emission level', 2: 'low Level GHG Emission level'}
    
    # Add cluster class to the dataframe
    df_temp['Cluster_Class'] = prediction
    cluster_class = df_temp[df_temp['Item'] == crop_name]['Cluster_Class'].values[0]

    return f"a predicted **<u>{emission[cluster_class]}</u>**"
# Min-max values for sliders
slider_limits = {
    column: (fwl_transformed[column].min(), fwl_transformed[column].max())
    for column in ['Feed', 'Import Quantity', 'Loss', 'Other uses (non-food)', 'Processed', 'Residuals', 'Stock Variation']
}

# Streamlit UI
st.title('Crop Cluster Prediction and Analysis')

st.header('Crop Analysis')
selected_crop = st.selectbox('Choose a crop:', df_birch_wl_birch['Item'].unique())

# Display clustering info based on selected crop
prod_cluster = clusters_list_birch_foodprod[clusters_list_birch_foodprod['Item'] == selected_crop]['Cluster_Class'].values[0]
prod_efficiency = {0: 'High production efficiency', 1: 'Low production efficiency', 2: 'Consistent Production Efficiency'}
st.write(f"Production efficiency for ({selected_crop}) : {prod_efficiency[prod_cluster]}")

wl_cluster = clusters_list_birch_foodwl[clusters_list_birch_foodwl['Item'] == selected_crop]['Cluster_Class'].values[0]
emission = {0: 'High GHG level Emission', 1: 'Moderate level GHG Emission', 2: 'Low level GHG Emission'}
st.write(f"GHG emission level for ({selected_crop}) : {emission[wl_cluster]}")

st.header('Custom Crop Analysis')

# Custom Crop Name
crop_name = st.text_input('Enter a Custom Crop Name', placeholder='e.g. Apple, Wheat...')

# Food Security Sliders
st.subheader('Food Production Parameters')
user_input_fs = {
    'Area harvested (ha)': st.slider('Area harvested', int(df_prod_copy['Area harvested ()'].min()), int(df_prod_copy['Area harvested'].max())),
    'Production (tonnes)': st.slider('Production', int(df_prod_copy['Production'].min()), int(df_prod_copy['Production'].max()))
}

# Food Waste/Loss Sliders
st.subheader('Food Waste/Loss Parameters (tonnes)')
user_input_fwl = {
    'Item': crop_name,
    'Export Quantity': 0,
    'Production': 0
}

for col, limits in slider_limits.items():
    user_input_fwl[col] = st.slider(col, int(limits[0]), int(limits[1]))

# Button to Predict for Custom Crop
if st.button('Predict for Custom Crop'):
    fs_result = food_security_prediction(user_input_fs)
    fwl_result = food_waste_prediction(user_input_fwl, crop_name)
    result = f"{crop_name} has {fs_result} and {fwl_result}"
    st.markdown(result, unsafe_allow_html=True)

