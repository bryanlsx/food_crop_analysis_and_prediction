import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px


st.set_page_config(page_title="Food Waste & Loss", page_icon="🐨")
# Streamlit UI
st.title('Data Visualization')

st.header('Crop Analysis')

fwl_transformed = pd.read_csv("fwl_transformed.csv")
st.dataframe(fwl_transformed)



st.title("Interactive Plot for analysis")

# ==============================Top 10 Items with Highest Total Loss===========================================
top_loss_items = fwl_transformed.groupby('Item')['Loss'].sum().sort_values(ascending=False).head(10)

fig = px.bar(top_loss_items, x=top_loss_items.index, y=top_loss_items.values, 
                labels={'y': 'Total Loss', 'index': 'Item'}, 
                title='Top 10 Items with Highest Total Loss',
                color=top_loss_items.values, color_continuous_scale='viridis')

st.plotly_chart(fig)


st.divider()

# ==============================Top 10 Items Contributing to Feed===========================================
top_feed_items = fwl_transformed.groupby('Item')['Feed'].sum().sort_values(ascending=False).head(10)

fig = px.bar(top_feed_items, x=top_feed_items.index, y=top_feed_items.values, 
                labels={'y': 'Total Loss', 'index': 'Item'}, 
                title='Top 10 Items Contributing to Feed',
                color=top_loss_items.values, color_continuous_scale='magma')

st.plotly_chart(fig)
st.divider()

# ==============================Heatmap===========================================
cols_of_interest = ['Feed', 'Import Quantity', 'Loss', 'Other uses (non-food)', 'Processed', 'Residuals', 'Stock Variation']
correlation_matrix = fwl_transformed[cols_of_interest].corr()

# Using Plotly to create the heatmap
fig = ff.create_annotated_heatmap(
    z=correlation_matrix.values,
    x=list(correlation_matrix.columns),
    y=list(correlation_matrix.index),
    annotation_text=correlation_matrix.round(2).values,
    colorscale='balance',
    showscale=True
)

fig.update_layout(title='Correlation Heatmap')

st.plotly_chart(fig)
st.divider()

# ==============================Heatmap===========================================
# Using Plotly to create the 2D Density Plot

# Create the 2D density plot using plotly.figure_factory
fig = ff.create_2d_density(
        x=fwl_transformed['Feed'], 
        y=fwl_transformed['Loss'], 
    )
fig.update_layout(title='2D Density Plot of Feed vs Loss')
st.plotly_chart(fig)
