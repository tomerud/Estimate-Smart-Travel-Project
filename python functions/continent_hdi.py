import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

# Create a connection string for SQLAlchemy
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# SQLAlchemy connection string
connection_string = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(connection_string)

# Fetch data using SQLAlchemy connection
query = """
SELECT continent, human_development_index, city, country, language, religion
FROM top_touristic_cities
"""
data = pd.read_sql(query, engine)

# Plot interactive scatter plot using Plotly
fig = px.scatter(data, x="continent", y="human_development_index",
                 hover_data=["city", "country", "language", "religion"],
                 title="Human Development Index by Continent",
                 labels={"continent": "Continent", "human_development_index": "Human Development Index"})

# Specify the output path
output_dir = "C:/Estimate/visual outputs"  # Directory to save outputs
html_path = os.path.join(output_dir, "continent_hdi_plot.html")
png_path = os.path.join(output_dir, "continent_hdi_plot.png")

# Save the interactive plot as an HTML file
fig.write_html(html_path)

# Save the plot as a static PNG image
fig.write_image(png_path)

print(f"Plot saved as HTML at {html_path} and PNG at {png_path}")
