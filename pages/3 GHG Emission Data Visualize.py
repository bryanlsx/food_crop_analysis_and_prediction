import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px


st.set_page_config(page_title="GHG Emission", page_icon="🐨")
# Streamlit UI
st.title('Data Visualization')

st.header('GHG Emission Analysis')


data = pd.read_csv('Malaysia_GHG_Emission.csv',encoding='ISO-8859-1')

def cleaned_process (df):
    # 1. Drop Redundant Columns
    clean = df.drop(columns=['ï»¿Domain Code','Area Code (M49)', 'Element Code', 'Item Code', 'Year Code'])

    # Drop the 'Note' column
    clean = clean.drop(columns=['Note'])

    return clean


ghg_data = cleaned_process(data)

st.dataframe(ghg_data)


st.title("Interactive Plot for analysis")

# ==============================Total GHG Emissions Over the Years===========================================
total_emissions_per_year = ghg_data.groupby('Year')['Value'].sum()


fig = px.line(total_emissions_per_year, x=total_emissions_per_year.index, y=total_emissions_per_year.values, 
              title='Total GHG Emissions Over the Years',
              labels={'y': 'Emissions (kt)', 'index': 'Year'})


st.plotly_chart(fig)

st.divider()

# ==============================Total emissions for each item/source across all years===========================================
total_emissions_by_item = ghg_data[ghg_data['Unit'] == 'kt'].groupby('Item')['Value'].sum().reset_index()
total_emissions_by_item = total_emissions_by_item.sort_values(by='Value', ascending=False)

# Create a bar chart using Plotly
fig = px.bar(total_emissions_by_item, x='Value', y='Item', 
             title='Total Greenhouse Gas Emissions by Item/Source in Malaysia',
             labels={'Item': 'Item/Source', 'Value': 'Total Emissions (kt)'},
             orientation='h',
             color='Item', color_continuous_scale='magma')

# Displaying the plot on Streamlit
st.plotly_chart(fig)

st.divider()


# ==============================Total GHG Emissions by Source for latest year===========================================
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

# ==============================Total Proportion of GHG Emissions by Element Across All Years==============================
total_emissions_by_element = ghg_data.groupby('Element')['Value'].sum().sort_values(ascending=False)

# Creating an interactive pie chart using Plotly
fig = px.pie(total_emissions_by_element, 
             values=total_emissions_by_element.values, 
             names=total_emissions_by_element.index,
             title='Total Proportion of GHG Emissions by Element Across All Years')

# Displaying the plot on Streamlit
st.plotly_chart(fig)


# ==============================Proportion of GHG Emissions by Element for latest year==============================
emissions_by_element = ghg_data[ghg_data['Year'] == latest_year].groupby('Element')['Value'].sum().sort_values(ascending=False)

# Creating an interactive pie chart using Plotly
fig = px.pie(emissions_by_element, 
             values=emissions_by_element.values, 
             names=emissions_by_element.index,
             title=f'Proportion of GHG Emissions by Element for {latest_year}')

# Displaying the plot on Streamlit
st.plotly_chart(fig)