import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Food Wastage Management", layout="wide")

st.title("🥗 Food Wastage Management Dashboard")

# ================= LOAD DATA =================
# Load CSVs
claims = pd.read_csv("claims_data.csv")
food = pd.read_csv("food_listings_data.csv")
providers = pd.read_csv("providers_data.csv")
receivers = pd.read_csv("receivers_data.csv")

# ================= SIDEBAR FILTERS =================
st.sidebar.header("🔍 Filters")

if "City" in providers.columns:
    city_options = ["All"] + sorted(providers["City"].dropna().unique().tolist())
    selected_city = st.sidebar.selectbox("Select City", city_options)
else:
    selected_city = "All"

if "Food_Type" in food.columns:
    food_type_options = ["All"] + sorted(food["Food_Type"].dropna().unique().tolist())
    selected_food_type = st.sidebar.selectbox("Select Food Type", food_type_options)
else:
    selected_food_type = "All"

# ================= APPLY FILTERS =================
filtered_food = food.copy()
if selected_city != "All" and "Location" in filtered_food.columns:
    filtered_food = filtered_food[filtered_food["Location"] == selected_city]

if selected_food_type != "All":
    filtered_food = filtered_food[filtered_food["Food_Type"] == selected_food_type]

filtered_claims = claims.copy()
if selected_city != "All" and "City" in filtered_claims.columns:
    filtered_claims = filtered_claims[filtered_claims["City"] == selected_city]

filtered_providers = providers.copy()
if selected_city != "All":
    filtered_providers = filtered_providers[filtered_providers["City"] == selected_city]

# ================= KEY METRICS =================
st.header("📊 Key Metrics")

food_listings_count = filtered_food["Food_Name"].nunique() if "Food_Name" in filtered_food.columns else 0

claims_total = claims["Claim_ID"].nunique() if "Claim_ID" in claims.columns else 0
pending_claims = claims[claims["Status"] == "Pending"]["Claim_ID"].nunique() if "Status" in claims.columns else 0
completed_claims = claims[claims["Status"] == "Completed"]["Claim_ID"].nunique() if "Status" in claims.columns else 0

providers_count = providers["Name"].nunique() if "Name" in providers.columns else 0
receivers_count = receivers["Name"].nunique() if "Name" in receivers.columns else 0

fulfillment_rate = (completed_claims / claims_total * 100) if claims_total > 0 else 0

expired_food_qty = 0
if "Expiry_Date" in food.columns and "Quantity" in food.columns:
    food["Expiry_Date"] = pd.to_datetime(food["Expiry_Date"], errors="coerce")
    expired_food_qty = food.loc[food["Expiry_Date"] < pd.Timestamp.today(), "Quantity"].sum()

# Show KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🥘 Food Listings", food_listings_count)
with col2:
    st.metric("📦 Total Claims", claims_total)
with col3:
    st.metric("🏬 Providers", providers_count)
with col4:
    st.metric("🤝 Receivers", receivers_count)

col5, col6, col7 = st.columns(3)
with col5:
    st.metric("⏳ Pending Claims", pending_claims)
with col6:
    st.metric("✅ Fulfillment Rate", f"{fulfillment_rate:.1f}%")
with col7:
    st.metric("⚠️ Expired Food Qty", expired_food_qty)

# ================= VISUAL INSIGHTS =================
st.header("📊 Visual Insights")

# Food Listings by Food Type (Pie Chart)
st.subheader("🍽️ Food Listings by Food Type")
if "Food_Type" in filtered_food.columns:
    food_type_counts = filtered_food["Food_Type"].value_counts().reset_index()
    food_type_counts.columns = ["Food_Type", "Count"]
    fig = px.pie(food_type_counts, names="Food_Type", values="Count", title="Distribution of Food Listings")
    st.plotly_chart(fig, use_container_width=True)

# Claims Trend Over Time (Line Chart)
st.subheader("📈 Claims Over Time")
if "Timestamp" in filtered_claims.columns:
    filtered_claims["Timestamp"] = pd.to_datetime(filtered_claims["Timestamp"], errors="coerce")
    claims_trend = (
        filtered_claims.dropna(subset=["Timestamp"])
        .groupby(filtered_claims["Timestamp"].dt.date)["Claim_ID"]
        .nunique()
        .reset_index()
    )
    claims_trend.columns = ["Date", "Total Claims"]
    fig2 = px.line(claims_trend, x="Date", y="Total Claims", markers=True, title="Claims Over Time")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No 'Timestamp' column found in claims dataset.")

# Expired vs Valid Food Quantity (Bar Chart)
st.subheader("⚠️ Expired vs Valid Food")
if {"Expiry_Date", "Quantity"}.issubset(filtered_food.columns):
    filtered_food["Expiry_Date"] = pd.to_datetime(filtered_food["Expiry_Date"], errors="coerce")
    expired_qty = filtered_food.loc[filtered_food["Expiry_Date"] < pd.Timestamp.today(), "Quantity"].sum()
    valid_qty = filtered_food.loc[filtered_food["Expiry_Date"] >= pd.Timestamp.today(), "Quantity"].sum()
    exp_df = pd.DataFrame({"Status": ["Expired", "Valid"], "Quantity": [expired_qty, valid_qty]})
    fig3 = px.bar(exp_df, x="Status", y="Quantity", color="Status", title="Expired vs Valid Food Quantity", text="Quantity")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Expiry date or quantity column missing in food dataset.")

# ================= DETAILED DATA =================
st.header("📋 Detailed Data")

st.subheader("Food Listings")
st.dataframe(filtered_food)

st.subheader("Claims")
st.dataframe(filtered_claims)

st.subheader("Providers")
st.dataframe(filtered_providers)

st.subheader("Receivers")
st.dataframe(receivers)