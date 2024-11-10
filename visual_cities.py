import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
from sqlalchemy import create_engine

# Create the connection engine using SQLAlchemy
engine = create_engine("mysql+mysqlconnector://root:112145@localhost:3306/cities")
query = "SELECT City, `Development Ranking (HDI)`, Religion, Language, Location FROM cities LIMIT 51"
cities_df = pd.read_sql(query, engine)

# Data Preprocessing
# Split latitude and longitude
cities_df[['Latitude', 'Longitude']] = cities_df['Location'].str.split(',', expand=True).astype(float)
cities_df = cities_df.drop(columns='Location')

# Encode categorical variables (Religion and Language)
encoder = LabelEncoder()
cities_df['Religion_encoded'] = encoder.fit_transform(cities_df['Religion'])
cities_df['Language_encoded'] = encoder.fit_transform(cities_df['Language'])

# Standardize data for PCA
features = ['Development Ranking (HDI)', 'Latitude', 'Longitude', 'Religion_encoded', 'Language_encoded']
scaler = StandardScaler()
scaled_features = scaler.fit_transform(cities_df[features])

# Dimensionality Reduction with PCA
pca = PCA(n_components=2)
cities_df[['PCA1', 'PCA2']] = pca.fit_transform(scaled_features)

# Interactive Plotting with Plotly, with permanent city names displayed
fig = px.scatter(
    cities_df,
    x='PCA1',
    y='PCA2',
    color='Development Ranking (HDI)',
    text='City',  # Display city names on each point
    title="Interactive Visualization of Cities by PCA Components",
    labels={'PCA1': 'PCA Component 1', 'PCA2': 'PCA Component 2'},
    color_continuous_scale=px.colors.sequential.Viridis
)

# Update the layout to display text near the markers
fig.update_traces(textposition='top center', marker=dict(size=12, opacity=0.7))
fig.update_layout(coloraxis_colorbar=dict(title="Development Ranking (HDI)"))

# Save the plot as an HTML file
fig.write_html("city_visualization.html")

# Provide instructions to manually open the file
print("The interactive plot with city names has been saved as 'city_visualization.html'. You can open this file in your browser.")
