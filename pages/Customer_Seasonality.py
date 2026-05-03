import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import duckdb


st.set_page_config(layout="wide")

st.title("👥 Customer & Seasonality Insights")
st.subheader("Overview of the dataframe")
# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data(data):
    df = pd.read_csv(data)
    return df
df = load_data("data/data_season.csv")
# -----------------------------
# CREATE RANDOM MONTHS
# -----------------------------
np.random.seed(42)

df["Month"] = np.random.randint(1, 13, size=len(df))
# Nom des mois
month_map = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}

df["Month_Name"] = df["Month"].map(month_map)
cols = ["Year", "Month", "Month_Name"] + [col for col in df.columns if col not in ["Year", "Month", "Month_Name"]]
df = df[cols]
df.rename(columns={"yeilds": "yields"}, inplace=True)
st.dataframe(df.head())
# -----------------------------
# SQL CONNECTION
# -----------------------------
con = duckdb.connect()

# Register dataframe as SQL table
con.register("agriculture_table", df)

#1. KPI ANALYSIS
#SQL Query
kpi_query = """
SELECT
    AVG(yields) AS avg_yield,
    MAX(yields) AS max_yield,
    MIN(yields) AS min_yield
FROM agriculture_table
"""
kpi_df = con.execute(kpi_query).fetchdf()

#Streamlit KPIs
col1, col2, col3 = st.columns(3)

col1.metric(
    "🌾 Average Yield",
    round(kpi_df["avg_yield"][0], 2)
)

col2.metric(
    "🏆 Maximum Yield",
    round(kpi_df["max_yield"][0], 2)
)

col3.metric(
    "📉 Minimum Yield",
    round(kpi_df["min_yield"][0], 2)
)

#2.Yield Trend by Year
#SQL Query
year_query = """
SELECT
    Year,
    AVG(yields) AS avg_yield
FROM agriculture_table
GROUP BY Year
ORDER BY Year
"""
year_df = con.execute(year_query).fetchdf()

#Graphique
fig1 = px.line(
    year_df,
    x="Year",
    y="avg_yield",
    markers=True,
    title="🌱 Yield Trend Over Time"
)

st.plotly_chart(fig1, use_container_width=True)

#3. Best Performing Crops
#SQL Query
crops_query='''
SELECT
    Crops,
    AVG(yields) AS avg_yield
FROM agriculture_table
GROUP BY Crops
ORDER BY avg_yield DESC
'''
crops_df = con.execute(crops_query).fetchdf()
#Visualisation
fig2 = px.bar(
    crops_df,
    x="Crops",
    y="avg_yield",
    color_discrete_sequence=["darkgreen"],
    title="🌾 Average Yield by Crop"
)
st.plotly_chart(fig2, use_container_width=True)

#4.Impact of Rainfall on Yields
rain_query = '''
SELECT
    Rainfall,
    yields
FROM agriculture_table
'''
rain_df = con.execute(rain_query).fetchdf()

#Scatter Plot
fig3 = px.scatter(
    rain_df,
    x="Rainfall",
    y="yields",
    title="🌧️ Rainfall vs Yield",
    trendline="ols")
st.plotly_chart(fig3, use_container_width=True)

#5.Monthly Yields
#SQL Yields
month_query = """
SELECT
    Month_Name,
    AVG(yields) AS avg_yield
FROM agriculture_table
GROUP BY Month_Name
"""
#Execution
month_df = con.execute(month_query).fetchdf()

fig4 = px.bar(
    month_df,
    x="Month_Name",
    y="avg_yield",
    color_discrete_sequence=["purple"],
    title="📅 Average Yield by Month"
)
#Visualization
st.plotly_chart(fig4, use_container_width=True)




