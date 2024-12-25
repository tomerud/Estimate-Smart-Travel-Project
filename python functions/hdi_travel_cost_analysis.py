import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# Database connection information
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "112145"
DB_PORT = 3306
DB_NAME = "cities"

# Create an SQLAlchemy engine
engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Query to get city names, HDI, and travel costs from the table
query = """
    SELECT city,
           human_development_index, 
           (budget_price_usd + midrange_price_usd + luxury_price_usd) / 3 AS average_travel_cost
    FROM top_touristic_cities
    WHERE human_development_index IS NOT NULL
      AND budget_price_usd IS NOT NULL
      AND midrange_price_usd IS NOT NULL
      AND luxury_price_usd IS NOT NULL
"""

# Load data into a pandas DataFrame
df = pd.read_sql(query, engine)

# Calculate correlation coefficient
correlation = df['human_development_index'].corr(df['average_travel_cost'])
print(f"Correlation between HDI and average travel cost: {correlation:.2f}")

# Create an interactive scatter plot with Plotly
fig = px.scatter(
    df,
    x="human_development_index",
    y="average_travel_cost",
    labels={
        "human_development_index": "Human Development Index (HDI)",
        "average_travel_cost": "Average Travel Cost (USD)"
    },
    title="Human Development Index vs. Average Travel Cost"
)

# Configure hover information to show only on hover
fig.update_traces(
    marker=dict(size=10),
    hovertemplate='<b>City:</b> %{text}<br><b>HDI:</b> %{x}<br><b>Cost:</b> %{y:.2f} USD',
    text=df['city']
)

# Show the plot
fig.show()
