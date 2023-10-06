import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Food Security", page_icon="🐨")
# Streamlit UI
st.title('Data Visualization')

st.header('Crop Analysis')



df_MlsAreaCrop = pd.read_csv('df_MlsAreaCrop.csv')
df_MlsMerge = pd.read_csv('df_MlsMerge.csv')
df_MlsProd = pd.read_csv('df_MlsProd.csv')

# ==============================Pairplot of Area Harvested and Production==============================
# Create a subplot with 1 row and 2 columns
fig = make_subplots(rows=1, cols=2)

# Add density plot for 'Total_Area' to the first column
fig.add_trace(
    go.Histogram(x=df_MlsMerge['Total_Area'], histnorm='probability density', name='Area Harvested'),
    row=1, col=1
)

# Add density plot for 'Total_Prod' to the second column
fig.add_trace(
    go.Histogram(x=df_MlsMerge['Total_Prod'], histnorm='probability density', name='Production'),
    row=1, col=2
)

# Update the layout
fig.update_layout(
    title_text="Density Plots of Area Harvested and Production (Pre-Clustering)",
    bargap=0.01
)

# Update x-axis titles
fig.update_xaxes(title_text="Area Harvested", row=1, col=1)
fig.update_xaxes(title_text="Production", row=1, col=2)

st.plotly_chart(fig)

# ==============================Top 10 Crops by Total Area Harvested in Malaysia==============================
fig = px.bar(df_MlsAreaCrop.head(10), 
             x='Total', 
             y='Item',
             orientation='h',  
             color='Total',
             color_continuous_scale='greens',  
             labels={'Total': 'Total Area Harvested (ha)', 'Item': 'Crop'},
             title='Top 10 Crops by Total Area Harvested in Malaysia')

st.plotly_chart(fig)
st.divider()


# ==============================Top 10 Crops by Total Production in Malaysia==============================
fig = px.bar(df_MlsProd.head(10), 
             x='Total', 
             y='Item',
             orientation='h',  
             color='Total',
             color_continuous_scale='greens',  
             labels={'Total': 'Total Production (tonnes)', 'Item': 'Crop'},
             title='Top 10 Crops by Total Production in Malaysia')

st.plotly_chart(fig)
st.divider()






# ==============================Parallel Coordinates Plot for Top 20 Crops by Area Harvested==============================
#Parallel Coordinates Plot
top_20_area_crops = df_MlsMerge.nlargest(20, 'Total_Area')

# Normalize the 'Total_Area' and 'Total_Prod' columns for better visualization
top_20_area_crops['Total_Area'] = (top_20_area_crops['Total_Area'] - top_20_area_crops['Total_Area'].min()) / \
                                  (top_20_area_crops['Total_Area'].max() - top_20_area_crops['Total_Area'].min())
top_20_area_crops['Total_Prod'] = (top_20_area_crops['Total_Prod'] - top_20_area_crops['Total_Prod'].min()) / \
                                  (top_20_area_crops['Total_Prod'].max() - top_20_area_crops['Total_Prod'].min())

# plotting
# Assign a unique color ID to each crop. This will ensure that each crop gets a different color.
top_20_area_crops['color_id'] = top_20_area_crops['Item'].astype('category').cat.codes

# Create a color map (mapping from color_id to crop name)
color_map = dict(enumerate(top_20_area_crops['Item'].astype('category').cat.categories))

# Plotting
fig = px.parallel_coordinates(top_20_area_crops, dimensions=['Total_Area', 'Total_Prod'], 
                              color='color_id',
                              labels={'Total_Area': 'Area Harvested', 'Total_Prod': 'Production'},
                              color_continuous_scale=px.colors.sequential.Jet)

# Update layout and axis titles
fig.update_layout(title='Parallel Coordinates Plot for Top 20 Crops by Area Harvested')

# Update the color axis to display crop names instead of color IDs
fig.update_layout(coloraxis_colorbar=dict(tickvals=list(color_map.keys()),
                                          ticktext=list(color_map.values())))

# Display the figure in Streamlit
st.plotly_chart(fig)

#========================================================================#
st.subheader('Transformed Dataset')
main_df = pd.read_csv("df_fs.csv")
st.dataframe(main_df)