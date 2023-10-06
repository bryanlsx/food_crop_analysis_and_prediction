import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots   


st.set_page_config(page_title="Food Waste & Loss", page_icon="🐨")
# Streamlit UI
st.title('Data Visualization')

st.header('Crop Analysis')

fwl_transformed = pd.read_csv("fwl_transformed.csv")
st.dataframe(fwl_transformed)



st.title("Interactive Plot for analysis")

# ==============================Pairplot of Area Harvested and Production==============================
# Create a subplot with 1 row and 2 columns
fig = make_subplots(rows=3, cols=3)

# Add density plot for 'Total_Area' to the first column
fig.add_trace(
    go.Histogram(x=fwl_transformed['Feed'], histnorm='probability density', name='Feed'),
    row=1, col=1
)

# Add density plot for 'Total_Prod' to the second column
fig.add_trace(
    go.Histogram(x=fwl_transformed['Import Quantity'], histnorm='probability density', name='Import Quantity'),
    row=1, col=2
)

fig.add_trace(
    go.Histogram(x=fwl_transformed['Loss'], histnorm='probability density', name='Loss'),
    row=1, col=3
)

fig.add_trace(
    go.Histogram(x=fwl_transformed['Other uses (non-food)'], histnorm='probability density', name='Other uses (non-food)'),
    row=2, col=1
)

fig.add_trace(
    go.Histogram(x=fwl_transformed['Processed'], histnorm='probability density', name='Processed'),
    row=2, col=2
)

fig.add_trace(
    go.Histogram(x=fwl_transformed['Residuals'], histnorm='probability density', name='Residuals'),
    row=2, col=3
)

fig.add_trace(
    go.Histogram(x=fwl_transformed['Stock Variation'], histnorm='probability density', name='Stock Variation'),
    row=3, col=1
)

# Update the layout
fig.update_layout(
    title_text="Density Plots of Area Harvested and Production (Pre-Clustering)",
    bargap=0.01
)

# Update x-axis titles
fig.update_xaxes(title_text="Feed", row=1, col=1)
fig.update_xaxes(title_text="Import Quantity", row=1, col=2)
fig.update_xaxes(title_text="Loss", row=1, col=3)
fig.update_xaxes(title_text="Other uses (non-food)", row=2, col=1)
fig.update_xaxes(title_text="Processed", row=2, col=2)
fig.update_xaxes(title_text="Residuals", row=2, col=3)
fig.update_xaxes(title_text="Stock Variation", row=3, col=1)

st.plotly_chart(fig)

top_feed_items = fwl_transformed.groupby('Item')['Feed'].sum().sort_values(ascending=False).head(10)

fig = px.bar(top_feed_items, x=top_feed_items.index, y=top_feed_items.values, 
                labels={'y': 'Feed', 'index': 'Item'}, 
                title='Top 10 Items Contributing to Feed',
                color=top_feed_items.values, color_continuous_scale='magma')

st.plotly_chart(fig)
st.divider()

import_qty = fwl_transformed.groupby('Item')['Import Quantity'].sum().sort_values(ascending=False).head(10)

fig = px.bar(import_qty, x=import_qty.index, y=import_qty.values, 
                labels={'y': 'Import Quantity', 'index': 'Item'}, 
                title='Top 10 Items with Import Quantity',
                color=import_qty.values, color_continuous_scale='magma')

st.plotly_chart(fig)


st.divider()

top_loss_items = fwl_transformed.groupby('Item')['Loss'].sum().sort_values(ascending=False).head(10)

fig = px.bar(top_loss_items, x=top_loss_items.index, y=top_loss_items.values, 
                labels={'y': 'Total Loss', 'index': 'Item'}, 
                title='Top 10 Items with Highest Total Loss',
                color=top_loss_items.values, color_continuous_scale='viridis')

st.plotly_chart(fig)


st.divider()

otheruses = fwl_transformed.groupby('Item')['Other uses (non-food)'].sum().sort_values(ascending=False).head(10)

fig = px.bar(otheruses, x=otheruses.index, y=otheruses.values, 
                labels={'y': 'Other uses (non-food)', 'index': 'Item'}, 
                title='Top 10 Items with Other uses (non-food)',
                color=otheruses.values, color_continuous_scale='viridis')

st.plotly_chart(fig)


st.divider()

pros = fwl_transformed.groupby('Item')['Processed'].sum().sort_values(ascending=False).head(10)

fig = px.bar(pros, x=pros.index, y=pros.values, 
                labels={'y': 'Processed', 'index': 'Item'}, 
                title='Top 10 Items with Processed',
                color=pros.values, color_continuous_scale='magma')

st.plotly_chart(fig)


st.divider()

# 
residuals = fwl_transformed.groupby('Item')['Residuals'].sum().sort_values(ascending=False).head(10)

fig = px.bar(residuals, x=residuals.index, y=residuals.values, 
                labels={'y': 'Residuals', 'index': 'Item'}, 
                title='Top 10 Items with residuals',
                color=residuals.values, color_continuous_scale='magma')

st.plotly_chart(fig)


st.divider()

stockvar = fwl_transformed.groupby('Item')['Stock Variation'].sum().sort_values(ascending=False).head(10)

fig = px.bar(stockvar, x=stockvar.index, y=stockvar.values, 
                labels={'y': 'Stock Variation', 'index': 'Item'}, 
                title='Top 10 Items with Stock Variation',
                color=stockvar.values, color_continuous_scale='magma')

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

st.image("fwl.png", use_column_width=True)

# # ==============================Top 10 Items with Highest Total Loss===========================================
# top_loss_items = fwl_transformed.groupby('Item')['Loss'].sum().sort_values(ascending=False).head(10)

# fig = px.bar(top_loss_items, x=top_loss_items.index, y=top_loss_items.values, 
#                 labels={'y': 'Total Loss', 'index': 'Item'}, 
#                 title='Top 10 Items with Highest Total Loss',
#                 color=top_loss_items.values, color_continuous_scale='viridis')

# st.plotly_chart(fig)


# st.divider()

# # ==============================Top 10 Items Contributing to Feed===========================================
# top_feed_items = fwl_transformed.groupby('Item')['Feed'].sum().sort_values(ascending=False).head(10)

# fig = px.bar(top_feed_items, x=top_feed_items.index, y=top_feed_items.values, 
#                 labels={'y': 'Total Loss', 'index': 'Item'}, 
#                 title='Top 10 Items Contributing to Feed',
#                 color=top_loss_items.values, color_continuous_scale='magma')

# st.plotly_chart(fig)
# st.divider()



# # ==============================Heatmap===========================================
# # Using Plotly to create the 2D Density Plot

# # Create the 2D density plot using plotly.figure_factory
# fig = ff.create_2d_density(
#         x=fwl_transformed['Feed'], 
#         y=fwl_transformed['Loss'], 
#     )
# fig.update_layout(title='2D Density Plot of Feed vs Loss')
# st.plotly_chart(fig)


# ========================================================================
# st.image("cluster_results_fwl.png", caption="Result of Clustering on FWL Dataset", use_column_width=True)
