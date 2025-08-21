import streamlit as st
import pandas as pd
import altair as alt

# --- Styling ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f6ff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 1rem 2rem;
    }
    .css-1pc5uxm {
        background-color: #003366 !important;
        color: white !important;
    }
    h1, h2, h3 {
        color: #003366;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Load datasets ---
providers = pd.read_csv('providers_data.csv')
receivers = pd.read_csv('receivers_data.csv')
food_listings = pd.read_csv('food_listings_data.csv')
claims = pd.read_csv('claims_data.csv')

# --- Dashboard Header ---
st.title("Local Food Wastage Dashboard")

# --- 1. Filter food donations (interactive filters) ---
st.subheader("Filter Food Donations")
col1, col2, col3 = st.columns(3)

with col1:
    city_options = sorted(food_listings['Location'].dropna().unique())
    selected_city = st.selectbox("Select City", ["All"] + city_options)

with col2:
    provider_options = sorted(providers['Name'].dropna().unique())
    selected_provider = st.selectbox("Select Provider", ["All"] + provider_options)

with col3:
    food_type_options = sorted(food_listings['Food_Type'].dropna().unique())
    selected_food_type = st.selectbox("Select Food Type", ["All"] + food_type_options)

# Apply filters
filtered = food_listings.copy()
if selected_city != "All":
    filtered = filtered[filtered['Location'] == selected_city]
if selected_provider != "All":
    provider_ids = providers[providers['Name'] == selected_provider]['Provider_ID']
    filtered = filtered[filtered['Provider_ID'].isin(provider_ids)]
if selected_food_type != "All":
    filtered = filtered[filtered['Food_Type'] == selected_food_type]

st.write(f"Showing {len(filtered)} food donation records.")
st.dataframe(filtered)

st.markdown("---")

# --- 2. Contact providers or receivers ---
st.subheader("Contact Information")
contact_type = st.radio("Show contact info for:", ("Providers", "Receivers"))

if contact_type == "Providers":
    st.dataframe(providers[['Name', 'Contact', 'City', 'Address']])
else:
    st.dataframe(receivers[['Name', 'Contact', 'City']])

st.markdown("---")

# --- 3. Most frequent providers (Top 10) ---
st.subheader("Most Frequent Providers by Quantity Donated")
prov_qty = (
    food_listings.groupby('Provider_ID')['Quantity']
    .sum()
    .reset_index()
    .merge(providers[['Provider_ID', 'Name']], on='Provider_ID')
    .sort_values(by='Quantity', ascending=False)
    .head(10)
)
prov_chart = alt.Chart(prov_qty).mark_bar(color="#1f77b4").encode(
    x=alt.X('Quantity', title='Total Quantity'),
    y=alt.Y('Name', sort='-x', title='Provider Name'),
)
st.altair_chart(prov_chart, use_container_width=True)

st.markdown("---")

# --- 4. Demand locations (Top 10 by claim count) ---
# Merge claims with food listings to get 'Location'
claims_with_location = claims.merge(food_listings[['Food_ID', 'Location']], on='Food_ID', how='left')

# Replace missing locations with a placeholder string
claims_with_location['Location'] = claims_with_location['Location'].fillna('Unknown').astype(str)

# Calculate claim counts per location
location_claim_counts = claims_with_location['Location'].value_counts().reset_index()
location_claim_counts.columns = ['Location', 'Claims']

# Filter out any empty or unknown locations if you prefer
location_claim_counts = location_claim_counts[location_claim_counts['Location'] != '']

# Plot top 10 locations with highest claim counts
top_locations = location_claim_counts.head(10)

import altair as alt

chart = alt.Chart(top_locations).mark_bar(color='#d62728').encode(
    x=alt.X('Claims', title='Number of Claims'),
    y=alt.Y('Location', sort='-x', title='Location')
).properties(width=700, height=350)

st.altair_chart(chart)

st.markdown("---")

st.markdown(
    """
    <style>
    /* Change app background */
    .stApp {
        background-color: #f0f2f6;
    }

    /* Customize sidebar */
    .css-1d391kg {
        background-color: #003366;
        color: white;
    }

    /* Style headers */
    h1, h2, h3 {
        color: #003366;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load datasets (ensure your CSV files are in the same directory or provide full paths)
providers = pd.read_csv('providers_data.csv')
receivers = pd.read_csv('receivers_data.csv')
food_listings = pd.read_csv('food_listings_data.csv')
claims = pd.read_csv('claims_data.csv')

# 1. Number of food providers and receivers in each city
def query1_providers_receivers_per_city():
    providers_per_city = providers.groupby('City')['Provider_ID'].nunique().reset_index(name='Providers_Count')
    receivers_per_city = receivers.groupby('City')['Receiver_ID'].nunique().reset_index(name='Receivers_Count')
    return pd.merge(providers_per_city, receivers_per_city, on='City', how='outer').fillna(0)

# 2. Total quantity of food available by provider type
def query2_quantity_by_provider_type():
    return food_listings.groupby('Provider_Type')['Quantity'].sum().reset_index().sort_values(by='Quantity', ascending=False)

# 3. Contact information of food providers in a specific city
def query3_providers_contact_in_city(city_name):
    return providers[providers['City'].str.lower() == city_name.lower()][['Name', 'Contact', 'City']]

# 4. Receivers who have claimed the most food
def query4_receivers_most_claimed():
    claims_with_qty = claims.merge(food_listings[['Food_ID', 'Quantity']], on='Food_ID', how='left')
    qty_per_receiver = claims_with_qty.groupby('Receiver_ID')['Quantity'].sum().reset_index()
    receiver_claims = qty_per_receiver.merge(receivers[['Receiver_ID', 'Name']], on='Receiver_ID')
    return receiver_claims.sort_values(by='Quantity', ascending=False)

# 5. Total quantity of food available from all providers
def query5_total_food_quantity():
    return int(food_listings['Quantity'].sum())

# 6. City with highest number of food listings
def query6_city_highest_food_listings():
    count_per_city = food_listings['Location'].value_counts().reset_index()
    count_per_city.columns = ['City', 'Listings_Count']
    return count_per_city.head()

# 7. Most commonly available food types
def query7_most_common_food_types():
    food_type_counts = food_listings['Food_Type'].value_counts().reset_index()
    food_type_counts.columns = ['Food_Type', 'Count']
    return food_type_counts

# 8. Number of food claims made for each food item
def query8_food_claim_counts():
    claims_count = claims.groupby('Food_ID').size().reset_index(name='Claims_Count')
    # Join with food_listings to get food names
    claims_with_names = claims_count.merge(food_listings[['Food_ID', 'Food_Name']], on='Food_ID', how='left')
    # Group by food name to aggregate counts if duplicates exist
    result = claims_with_names.groupby('Food_Name')['Claims_Count'].sum().reset_index().sort_values(by='Claims_Count', ascending=False)
    return result

# 9. Provider with highest number of successful food claims
def query9_provider_highest_successful_claims():
    completed_claims = claims[claims['Status'].str.lower() == 'completed']
    completed_claims_with_provider = completed_claims.merge(food_listings[['Food_ID', 'Provider_ID']], on='Food_ID', how='left')
    successful_claim_counts = completed_claims_with_provider['Provider_ID'].value_counts().reset_index()
    successful_claim_counts.columns = ['Provider_ID', 'Successful_Claims_Count']
    return successful_claim_counts.merge(providers[['Provider_ID', 'Name']], on='Provider_ID').sort_values(by='Successful_Claims_Count', ascending=False)

# 10. Percentage of food claims by status (Completed, Pending, Cancelled)
def query10_claims_status_percentage():
    return claims['Status'].value_counts(normalize=True).mul(100).reset_index().rename(columns={'index': 'Status', 'Status': 'Percentage'})

# 11. Average quantity of food claimed per receiver
def query11_avg_quantity_claimed_per_receiver():
    claims_with_qty = claims.merge(food_listings[['Food_ID', 'Quantity']], on='Food_ID', how='left')
    avg_qty = claims_with_qty.groupby('Receiver_ID')['Quantity'].mean().reset_index()
    return avg_qty.merge(receivers[['Receiver_ID', 'Name']], on='Receiver_ID')

# 12. Number of food claims by meal type
def query12_claims_by_meal_type():
    claims_with_meal_type = claims.merge(food_listings[['Food_ID', 'Meal_Type']], on='Food_ID', how='left')
    meal_type_counts = claims_with_meal_type['Meal_Type'].value_counts().reset_index()
    meal_type_counts.columns = ['Meal_Type', 'Claims_Count']
    return meal_type_counts

# 13. Total quantity of food donated by each provider
def query13_total_quantity_by_provider():
    total_qty = food_listings.groupby('Provider_ID')['Quantity'].sum().reset_index()
    return total_qty.merge(providers[['Provider_ID', 'Name']], on='Provider_ID').sort_values(by='Quantity', ascending=False)

# --------------------------------------------------------------------------------------------
# Display all queries and their results using Streamlit
# --------------------------------------------------------------------------------------------

st.title("Food Wastage Management - Queries and Results")

st.subheader("1. How many food providers and receivers are there in each city?")
st.dataframe(query1_providers_receivers_per_city())

st.subheader("2. Which type of food provider (restaurant, grocery store, etc.) contributes the most food?")
st.dataframe(query2_quantity_by_provider_type())

st.subheader("3. Contact information of food providers in a specific city")

# You can use a dropdown with available cities for better UX:
city_list = sorted(providers['City'].dropna().unique())
selected_city = st.selectbox("Select a city:", ["-- Select City --"] + city_list)

if selected_city != "-- Select City --":
    df = query3_providers_contact_in_city(selected_city)
    if df.empty:
        st.warning(f"No providers found in city: {selected_city}")
    else:
        st.dataframe(df)
else:
    st.info("Please select a city to see contact information of providers.")

st.subheader("4. Which receivers have claimed the most food?")
st.dataframe(query4_receivers_most_claimed())

st.subheader("5. What is the total quantity of food available from all providers?")
st.write(f"Total Quantity: {query5_total_food_quantity()}")

st.subheader("6. City with the highest number of food listings")
st.dataframe(query6_city_highest_food_listings())

st.subheader("7. Most commonly available food types")
st.dataframe(query7_most_common_food_types())

st.subheader("8. Number of food claims made for each food item")
st.dataframe(query8_food_claim_counts())

st.subheader("9. Provider with the highest number of successful food claims")
st.dataframe(query9_provider_highest_successful_claims())

st.subheader("10. Percentage of food claims by status")
st.dataframe(query10_claims_status_percentage())

st.subheader("11. Average quantity of food claimed per receiver")
st.dataframe(query11_avg_quantity_claimed_per_receiver())

st.subheader("12. Number of food claims by meal type")
st.dataframe(query12_claims_by_meal_type())

st.subheader("13. Total quantity of food donated by each provider")
st.dataframe(query13_total_quantity_by_provider())
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        right: 10px;
        bottom: 10px;
        font-size: 20px;
        color: red;
        opacity: 0.6;
        z-index: 9999;
    }
    </style>
    <div class="footer">
        Developed by Manvi Jain
    </div>
    """,
    unsafe_allow_html=True
)