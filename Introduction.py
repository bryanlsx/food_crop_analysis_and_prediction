import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px

st.title('Introduction')
st.image("pg1.png", use_column_width=True)
st.image("pg2.png", use_column_width=True)

# ========Visualise Part===============
st.header('GHG Emission Data Visualisations')

data = pd.read_csv('Malaysia_GHG_Emission.csv',encoding='ISO-8859-1')

def cleaned_process (df):
    # 1. Drop Redundant Columns
    clean = df.drop(columns=['ï»¿Domain Code','Area Code (M49)', 'Element Code', 'Item Code', 'Year Code'])

    # Drop the 'Note' column
    clean = clean.drop(columns=['Note'])

    return clean

ghg_data = cleaned_process(data)

# ==============================Total GHG Emissions Over the Years===========================================
st.header('GHG Emission Pattern Across the Years')
total_emissions_per_year = ghg_data.groupby('Year')['Value'].sum()


fig = px.line(total_emissions_per_year, x=total_emissions_per_year.index, y=total_emissions_per_year.values, 
              title='Total GHG Emissions Over the Years',
              labels={'y': 'Emissions (kt)', 'index': 'Year'})


st.plotly_chart(fig)

st.divider()

# ==============================Total GHG Emissions by Source for latest year===========================================
st.header('Source of GHG Emissions Year 2020')
latest_year = ghg_data['Year'].max()
emissions_by_source = ghg_data[ghg_data['Year'] == latest_year].groupby('Item')['Value'].sum().sort_values(ascending=False)

# Create a horizontal bar chart using Plotly
fig = px.bar(emissions_by_source, x=emissions_by_source.index, y=emissions_by_source.values, 
             title=f'Total GHG Emissions by Source for {latest_year}',
             labels={'y': 'Emission (kt)', 'x': 'Emission Source'},
             color='Value')
fig.update_layout(xaxis_tickangle=-45)
# Displaying the plot on Streamlit
st.plotly_chart(fig)

st.divider()

# =======================================
st.image("pg3.png", use_column_width=True)
st.image("pg4.png", use_column_width=True)
st.image("pg5.png", use_column_width=True)
st.image("pg6.png", use_column_width=True)