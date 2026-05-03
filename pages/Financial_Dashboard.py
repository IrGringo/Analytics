import streamlit as st
import pandas as pd
import plotly.express as px



st.set_page_config(page_title="Financial Dashboard",page_icon="📊",layout="wide")
st.title("📊 Financial Analysis & Profitability Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data(data):
    df = pd.read_excel(data)
    return df
df=load_data("data/Customer_Profit_Analysis.xlsx")
# -----------------------------
# SIDEBAR (FILTRES)
# -----------------------------
st.sidebar.header("Filters")

country = st.sidebar.multiselect(
    "Select Country",
    df["Country"].unique(),
    default=df["Country"].unique()
)

segment = st.sidebar.multiselect(
    "Select Segment",
    df["Segment"].unique(),
    default=df["Segment"].unique()
)

df_filtered = df[
    (df["Country"].isin(country)) &
    (df["Segment"].isin(segment))
]

# -----------------------------
# KPIs
# -----------------------------
total_sales = df_filtered["Sales"].sum()
total_profit = df_filtered["Profit"].sum()
profit_margin = total_profit / total_sales

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("📊 Profit Margin", f"{profit_margin:.2%}")

st.markdown("---")

# -----------------------------
# SALES OVER TIME
# -----------------------------
sales_time = df_filtered.groupby("Date")["Sales"].sum().reset_index()

fig1 = px.line(
    sales_time,
    x="Date",
    y="Sales",
    title="📅 Sales Over Time"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# SALES BY COUNTRY
# -----------------------------
col1, col2 = st.columns(2)

country_sales = df_filtered.groupby("Country")["Sales"].sum().reset_index()

fig2 = px.bar(
    country_sales,
    x="Country",
    y="Sales",
    title="🌍 Sales by Country"
)

col1.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# PROFIT BY SEGMENT
# -----------------------------
segment_profit = df_filtered.groupby("Segment")["Profit"].sum().reset_index()

fig3 = px.pie(
    segment_profit,
    names="Segment",
    values="Profit",
    title="🧩 Profit Distribution by Segment"
)

col2.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# PRODUCT PERFORMANCE
# -----------------------------
product_perf = df_filtered.groupby("Product")["Profit"].sum().reset_index()

fig4 = px.bar(
    product_perf,
    x="Product",
    y="Profit",
    title="📦 Profit by Product"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# TABLE DETAIL
# -----------------------------
st.markdown("### 🔎 Detailed Data")
st.dataframe(df_filtered)