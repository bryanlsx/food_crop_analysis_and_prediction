import streamlit as st



# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox(
    'Choose a page',
    ('Food Security Data Visualize', 'Food Waste and Loss Data Visualize', 'GHG Emission Data Visualize', 'Crop Analysis', 'Custom Crop Prediction')
)


