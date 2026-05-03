import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide")

st.title("🛍️ Customer Behavior & Revenue Drivers")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data(data):
    df = pd.read_csv(data)
    return df
df=load_data("data/shopping_behavior_updated.csv")
st.dataframe(df.head())


# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Filtres")

gender = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

category = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

df_filtered = df[
    (df["Gender"].isin(gender)) &
    (df["Category"].isin(category))
]

# -----------------------------
# KPIs
# -----------------------------
total_revenue = df_filtered["Purchase Amount (USD)"].sum()
avg_purchase = df_filtered["Purchase Amount (USD)"].mean()

col1, col2 = st.columns(2)

col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
col2.metric("🧾 Avg Purchase", f"${avg_purchase:,.0f}")

st.markdown("---")

# -----------------------------
# CATEGORY PERFORMANCE
# -----------------------------
cat_sales = df_filtered.groupby("Category")["Purchase Amount (USD)"].sum().reset_index()

fig1 = px.bar(cat_sales, x="Category", y="Purchase Amount (USD)",
              title="📦 Revenue by Category")

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# PAYMENT METHOD
# -----------------------------
pay = df_filtered.groupby("Payment Method")["Purchase Amount (USD)"].sum().reset_index()

fig2 = px.pie(pay, names="Payment Method", values="Purchase Amount (USD)",
              title="💳 Payment Method Distribution")

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# CUSTOMER DEMOGRAPHICS
# -----------------------------
age_dist = px.histogram(df_filtered, x="Age",nbins=20,
                        title="👥 Age Distribution")
age_dist.update_layout(bargap=0.1)

st.plotly_chart(age_dist, use_container_width=True)

# -----------------------------
# TOP INSIGHT
# -----------------------------
top_category = cat_sales.sort_values(by="Purchase Amount (USD)", ascending=False).iloc[0]["Category"]

st.success(f"🏆 Top Revenue Category: {top_category}")

