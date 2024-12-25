import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA  # Add this import
from sqlalchemy import create_engine

# Create the connection engine using SQLAlchemy
engine = create_engine("mysql+mysqlconnector://root:112145@localhost:3306/cities")

# Query to retrieve city data
query = "SELECT city, human_development_index, religion, language, latitude, longitude FROM top_touristic_cities LIMIT 100"
cities_df = pd.read_sql(query, engine)

# Encode categorical variables (Religion and Language)
encoder = LabelEncoder()
cities_df['religion_encoded'] = encoder.fit_transform(cities_df['religion'])
cities_df['language_encoded'] = encoder.fit_transform(cities_df['language'])

# Standardize data for PCA
features = ['human_development_index', 'latitude', 'longitude', 'religion_encoded', 'language_encoded']
scaler = StandardScaler()
scaled_features = scaler.fit_transform(cities_df[features])

# Dimensionality Reduction with PCA for only latitude, longitude, religion, and language
pca = PCA(n_components=1)
cities_df['PCA1'] = pca.fit_transform(scaled_features[:, 1:])  # Exclude HDI from PCA

# Interactive Plotting with Plotly, with HDI on the x-axis and PCA1 on the y-axis
fig = px.scatter(
    cities_df,
    x='human_development_index',
    y='PCA1',
    color='human_development_index',
    text='city',  # Display city names on each point
    title="Interactive Visualization of Cities by Development Ranking (HDI) and PCA Components",
    labels={'human_development_index': 'Development Ranking (HDI)', 'PCA1': 'PCA Component'},
    color_continuous_scale=px.colors.sequential.Viridis
)

# Update the layout to display text near the markers
fig.update_traces(textposition='top center', marker=dict(size=12, opacity=0.7))
fig.update_layout(coloraxis_colorbar=dict(title="Development Ranking (HDI)"))

# Save the plot as an HTML file
fig.write_html("city_visualization.html")

# Provide instructions to manually open the file
print("The interactive plot with city names has been saved as 'city_visualization.html'. You can open this file in your browser.")
