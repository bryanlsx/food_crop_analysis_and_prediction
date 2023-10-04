import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pickle

def load_data(filename):
    data = pd.read_csv(filename)
    return data

# Load csv datasets
df_prod_copy = load_data('df_prod_copy.csv')
df_birch_wl_birch = load_data('df_birch_wl_birch.csv')
fwl_transformed = load_data('fwl_transformed.csv')

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

def food_security_prediction(user_input):
    df_temp = df_prod_copy.copy()
    df_temp.loc[df_temp.shape[0]] = user_input
    scaled_data = scaler.fit_transform(df_temp[['Area harvested', 'Production']])
    prediction = birch.predict(scaled_data)
    cluster = prediction[-1]  # taking the prediction for the last row which is our input
    return cluster

def food_waste_prediction(user_input, crop_name):
    df_temp = fwl_transformed.copy()
    df_temp.loc[df_temp.shape[0]] = user_input
    selected_columns = df_temp.iloc[:, [2, 3, 4, 5, 6, 8, 9]]
    scaled_data = StandardScaler().fit_transform(selected_columns)
    pca = PCA(n_components=2)
    transformed_data = pca.fit_transform(scaled_data)
    prediction = birch_fwl.predict(transformed_data)
    cluster = prediction[-1]  # taking the prediction for the last row which is our input
    return cluster

# Color-coding functions
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
        return '#F39C12'  # red
    elif cluster_num == 1:
        return '#E74C3C'  # yellow
    else:
        return '#2ECC71'  # green
    
# Min-max values for sliders
slider_limits = {
    column: ((fwl_transformed[column].min()), fwl_transformed[column].max())
    for column in ['Feed', 'Import Quantity', 'Loss', 'Other uses (non-food)', 'Processed', 'Residuals', 'Stock Variation']
}

# Streamlit UI
st.title('Custom Crop Prediction')

# Custom Crop Name
st.subheader('Enter your Crop\'s Name')
crop_name = st.text_input('Enter a Custom Crop Name', placeholder='e.g. Apple, Wheat...')

# Food Security Sliders
st.subheader('Food Production Parameters')
user_input_fs = {
    'Area harvested': st.slider('Area harvested (ha)', int(df_prod_copy['Area harvested'].min()), int(df_prod_copy['Area harvested'].max())),
    'Production': st.slider('Production (tonnes)', int(df_prod_copy['Production'].min()), int(df_prod_copy['Production'].max()))
}

# Food Waste/Loss Sliders
st.subheader('Food Waste/Loss Parameters')
user_input_fwl = {
    'Item': crop_name,
    'Export Quantity': 0,
    'Production': 0
}

for col, limits in slider_limits.items():
    user_input_fwl[col] = st.slider(col + " (tonnes)", int(limits[0]), int(limits[1]))

if crop_name == '':
    crop_name = 'Unknown Plant'

# Button to Predict for Custom Crop
if st.button('See how your crop performs!'):
    fs_cluster = food_security_prediction(user_input_fs)
    fwl_cluster = food_waste_prediction(user_input_fwl, crop_name)
    efficiency = {0: 'High production efficiency', 1: 'Low production efficiency', 2: 'Consistent production efficiency'}
    emission = {0: 'High GHG Emission level', 1: 'Low Level GHG Emission level', 2: 'Moderate Level GHG Emission level'}
    utilisation = {0: 'Moderate Utilisation', 1: 'High utilisation', 2: 'Low utilisation'}

    st.markdown(f"""
    <style>
        .info-card {{
            padding: 10px 20px;
            margin: 10px 0px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
    </style>

    <div class="info-card" style="background-color: {get_color_pe(fs_cluster)};">
        <h4>Production Efficiency for {crop_name}</h4>
        <p>{efficiency[fs_cluster]}</p>
    </div>

    <div class="info-card" style="background-color: {get_color_fwl(fwl_cluster)};">
        <h4>GHG Emission Level for {crop_name}</h4>
        <p>{emission[fwl_cluster]}</p>
    </div>

    <div class="info-card" style="background-color: {get_color_util(fwl_cluster)};">
        <h4>GHG Emission Level for {crop_name}</h4>
        <p>{utilisation[fwl_cluster]}</p>
    </div>
    """, unsafe_allow_html=True)
