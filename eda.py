import pandas as pd
# Load datasets
providers = pd.read_csv('providers_data.csv')
receivers = pd.read_csv('receivers_data.csv')
food_listings = pd.read_csv('food_listings_data.csv')
claims = pd.read_csv('claims_data.csv')

# Preview the first 5 rows of each dataset
print("Providers Dataset:")
print(providers.head())
print("\nReceivers Dataset:")
print(receivers.head())
print("\nFood Listings Dataset:")
print(food_listings.head())
print("\nClaims Dataset:")
print(claims.head())
print("\nProviders Dataset Info:")
providers.info()

print("\nProviders Missing Values:")
print(providers.isnull().sum())

print("\nReceivers Dataset Info:")
receivers.info()

print("\nReceivers Missing Values:")
print(receivers.isnull().sum())

print("\nFood Listings Dataset Info:")
food_listings.info()

print("\nFood Listings Missing Values:")
print(food_listings.isnull().sum())

print("\nClaims Dataset Info:")
claims.info()

print("\nClaims Missing Values:")
print(claims.isnull().sum())

# Summary statistics for numerical columns in food_listings
print("\nFood Listings Summary Statistics:")
print(food_listings.describe())
import pandas as pd

# Load datasets
providers = pd.read_csv('providers_data.csv')
receivers = pd.read_csv('receivers_data.csv')
food_listings = pd.read_csv('food_listings_data.csv')
claims = pd.read_csv('claims_data.csv')

# Preview the first 5 rows of each dataset
print("Providers Dataset:")
print(providers.head())
print("\nReceivers Dataset:")
print(receivers.head())
print("\nFood Listings Dataset:")
print(food_listings.head())
print("\nClaims Dataset:")
print(claims.head())
# Check for missing values in providers dataset
print("Providers Missing Values:")
print(providers.isnull().sum())

# Clean whitespace and standardize casing in 'City' and 'Type' columns
providers['City'] = providers['City'].str.strip().str.title()
providers['Type'] = providers['Type'].str.strip().str.title()

# Show first 5 rows to confirm changes
print("\nProviders Dataset sample after cleaning:")
print(providers[['City', 'Type']].head())
# Check for missing values in receivers dataset
print("Receivers Missing Values:")
print(receivers.isnull().sum())

# Clean whitespace and standardize casing in 'City' and 'Type' columns
receivers['City'] = receivers['City'].str.strip().str.title()
receivers['Type'] = receivers['Type'].str.strip().str.title()

# Show first 5 rows to confirm changes
print("\nReceivers Dataset sample after cleaning:")
print(receivers[['City', 'Type']].head())
# Fix "Ngo" to "NGO" in the Type column
receivers['Type'] = receivers['Type'].replace({'Ngo': 'NGO'})

# Confirm the change
print("\nUpdated Receivers Types:")
print(receivers['Type'].value_counts())
# Check for missing values in food_listings dataset
print("Food Listings Missing Values:")
print(food_listings.isnull().sum())

# Clean whitespace and standardize casing in relevant columns
food_listings['Location'] = food_listings['Location'].str.strip().str.title()
food_listings['Food_Type'] = food_listings['Food_Type'].str.strip().str.title()
food_listings['Meal_Type'] = food_listings['Meal_Type'].str.strip().str.title()

# Show sample rows to confirm changes
print("\nFood Listings sample after cleaning:")
print(food_listings[['Location', 'Food_Type', 'Meal_Type']].head())
# Check for missing values in claims dataset
print("Claims Missing Values:")
print(claims.isnull().sum())

# Clean whitespace and standardize casing in 'Status' column
claims['Status'] = claims['Status'].str.strip().str.title()

# Show sample rows to confirm changes
print("\nClaims Dataset sample after cleaning:")
print(claims[['Status']].head())
# Check duplicates in Providers
print("Duplicate rows in providers dataset:", providers.duplicated().sum())
print("Unique provider types:")
print(providers['Type'].value_counts())
# Check duplicates in receivers dataset
print("Duplicate rows in receivers dataset:", receivers.duplicated().sum())

# Unique receiver types
print("Unique receiver types:")
print(receivers['Type'].value_counts())
# Check duplicates in food_listings dataset
print("Duplicate rows in food_listings dataset:", food_listings.duplicated().sum())

# Unique Provider_Type values
print("Unique provider types in food_listings:")
print(food_listings['Provider_Type'].value_counts())
# Check duplicates in claims dataset
print("Duplicate rows in claims dataset:", claims.duplicated().sum())

# Unique Status values
print("Unique Status values:")
print(claims['Status'].value_counts())
# Define a list of known non-vegetarian food keywords (you can add more if needed)
non_veg_keywords = ['Chicken', 'Fish', 'Meat', 'Egg', 'Prawn', 'Beef', 'Pork', 'Lamb', 'Turkey', 'Seafood', 'Shrimp']

# Filter rows where Food_Name contains non-vegetarian keywords but Food_Type is 'Vegetarian'
mismatched_non_veg = food_listings[
    (food_listings['Food_Name'].str.contains('|'.join(non_veg_keywords), case=False)) & 
    (food_listings['Food_Type'].str.lower() == 'vegetarian')
]

print("Possible mismatches where non-veg foods are marked as Vegetarian:")
print(mismatched_non_veg[['Food_Name', 'Food_Type', 'Quantity', 'Provider_ID']])
# Keywords to identify non-vegetarian food
non_veg_keywords = ['Chicken', 'Fish']

# Update Food_Type to 'Non-Vegetarian' where Food_Name is in non_veg_keywords and Food_Type is 'Vegetarian'
food_listings.loc[
    (food_listings['Food_Name'].str.lower().isin([x.lower() for x in non_veg_keywords])) & 
    (food_listings['Food_Type'].str.lower() == 'vegetarian'),
    'Food_Type'
] = 'Non-Vegetarian'

# Verify the corrections
corrected_rows = food_listings[
    (food_listings['Food_Name'].str.lower().isin([x.lower() for x in non_veg_keywords])) & 
    (food_listings['Food_Type'].str.lower() == 'non-vegetarian')
]

print(f"Corrected entries count: {len(corrected_rows)}")
print(corrected_rows[['Food_Name', 'Food_Type', 'Quantity', 'Provider_ID']].head())
# List of keywords indicating non-vegetarian food
non_veg_keywords = ['chicken', 'fish']

# Update Food_Type to 'Non-Vegetarian' where Food_Name matches keywords but Food_Type is 'Vegetarian'
food_listings.loc[
    (food_listings['Food_Name'].str.lower().isin(non_veg_keywords)) & (food_listings['Food_Type'].str.lower() == 'vegetarian'),
    'Food_Type'
] = 'Non-Vegetarian'

# Verify corrections
corrected = food_listings[
    (food_listings['Food_Name'].str.lower().isin(non_veg_keywords)) & (food_listings['Food_Type'].str.lower() == 'non-vegetarian')
]

print(f"Number of corrected records: {len(corrected)}")
print(corrected[['Food_Name', 'Food_Type', 'Quantity', 'Provider_ID']].head())
# Get unique combinations of Food_Name and Food_Type in food_listings
food_type_combinations = food_listings[['Food_Name', 'Food_Type']].drop_duplicates().sort_values(by='Food_Name')
print(food_type_combinations)
# Define a mapping from Food_Name to correct Food_Type
food_type_mapping = {
    'bread': 'Vegetarian',
    'chicken': 'Non-Vegetarian',
    'dairy': 'Vegetarian',  # usually dairy is vegetarian, but not vegan
    'fish': 'Non-Vegetarian',
    'fruits': 'Vegan',
    'pasta': 'Vegetarian',
    'rice': 'Vegan',
    'salad': 'Vegan',
    'soup': 'Vegetarian',  # adjust if needed
    'vegetables': 'Vegan'
}

# Function to correct the Food_Type based on Food_Name (case insensitive)
def correct_food_type(row):
    name = row['Food_Name'].lower()
    if name in food_type_mapping:
        return food_type_mapping[name]
    else:
        return row['Food_Type']  # default to existing value if no mapping

# Apply the correction
food_listings['Food_Type'] = food_listings.apply(correct_food_type, axis=1)

# Verify changes (print unique food types per food name after correction)
print(food_listings.groupby(['Food_Name', 'Food_Type']).size())
# Convert Expiry_Date in food_listings to datetime
food_listings['Expiry_Date'] = pd.to_datetime(food_listings['Expiry_Date'], errors='coerce')

# Convert Timestamp in claims to datetime
claims['Timestamp'] = pd.to_datetime(claims['Timestamp'], errors='coerce')

# Verify conversion by printing data types
print("Data types after datetime conversion:")
print(food_listings.dtypes[['Expiry_Date']])
print(claims.dtypes[['Timestamp']])
print(providers.isnull().sum())
print(receivers.isnull().sum())
print(food_listings.isnull().sum())
print(claims.isnull().sum())
print(set(food_listings['Provider_ID']) - set(providers['Provider_ID']))
print(set(claims['Food_ID']) - set(food_listings['Food_ID']))
print(set(claims['Receiver_ID']) - set(receivers['Receiver_ID']))
# Number of food providers per city
providers_per_city = providers.groupby('City')['Provider_ID'].nunique().reset_index(name='Providers_Count')
print("Food Providers count per city:")
print(providers_per_city)

# Number of receivers per city
receivers_per_city = receivers.groupby('City')['Receiver_ID'].nunique().reset_index(name='Receivers_Count')
print("\nReceivers count per city:")
print(receivers_per_city)
# Total quantity of food available by provider type, sorted descending
quantity_by_provider_type = food_listings.groupby('Provider_Type')['Quantity'].sum().reset_index().sort_values(by='Quantity', ascending=False)

print("Total quantity of food available by provider type:")
print(quantity_by_provider_type)
unique_cities = providers['City'].unique()
print(unique_cities[:20])  # print first 20 cities as sample
city_name = 'New Jessica'

providers_in_city = providers[providers['City'].str.lower() == city_name.lower()][['Name', 'Contact', 'City']]

print(f"Food providers and their contact details in {city_name}:")
print(providers_in_city)
city_provider_counts = providers['City'].value_counts()
print(city_provider_counts.head(10))  # top 10 cities by provider count
city_name = 'New Carol'

providers_in_city = providers[providers['City'].str.lower() == city_name.lower()][['Name', 'Contact', 'City']]

print(f"Food providers and their contact details in {city_name}:")
print(providers_in_city)
# Join claims with food_listings to get quantity per claim
claims_with_qty = claims.merge(food_listings[['Food_ID', 'Quantity']], on='Food_ID', how='left')

# Aggregate total quantity claimed per receiver
quantity_claimed_per_receiver = claims_with_qty.groupby('Receiver_ID')['Quantity'].sum().reset_index()

# Join with receivers dataset to get receiver names
receiver_claims = quantity_claimed_per_receiver.merge(receivers[['Receiver_ID', 'Name']], on='Receiver_ID')

# Sort descending by quantity claimed
receiver_claims_sorted = receiver_claims.sort_values(by='Quantity', ascending=False)

print("Receivers who have claimed the most food:")
print(receiver_claims_sorted)
total_quantity = food_listings['Quantity'].sum()
print(f"Total quantity of food available from all providers: {total_quantity}")
# Count the number of food listings per city
food_listings_per_city = food_listings['Location'].value_counts().reset_index()
food_listings_per_city.columns = ['City', 'Listings_Count']

# Display the city with the highest number of listings
top_city = food_listings_per_city.iloc[0]
print(f"City with the highest number of food listings: {top_city['City']} with {top_city['Listings_Count']} listings")
food_type_counts = food_listings['Food_Type'].value_counts().reset_index()
food_type_counts.columns = ['Food_Type', 'Count']

print("Most commonly available food types:")
print(food_type_counts)
claims_per_food = claims['Food_ID'].value_counts().reset_index()
claims_per_food.columns = ['Food_ID', 'Claims_Count']

# Join with food listings to get food names
claims_per_food_named = claims_per_food.merge(food_listings[['Food_ID', 'Food_Name']], on='Food_ID', how='left')

print("Number of food claims made per food item:")
print(claims_per_food_named)
# Filter claims with status Completed (successful)
completed_claims = claims[claims['Status'].str.lower() == 'completed']

# Join completed claims with food listings to get Provider_ID
completed_claims_with_provider = completed_claims.merge(food_listings[['Food_ID', 'Provider_ID']], on='Food_ID', how='left')

# Count successful claims per provider
provider_successful_claims = completed_claims_with_provider['Provider_ID'].value_counts().reset_index()
provider_successful_claims.columns = ['Provider_ID', 'Successful_Claims_Count']

# Join with providers dataset to get provider names
provider_successful_claims_named = provider_successful_claims.merge(providers[['Provider_ID', 'Name']], on='Provider_ID', how='left')

# Sort descending to get highest
provider_successful_claims_named = provider_successful_claims_named.sort_values(by='Successful_Claims_Count', ascending=False)

print("Providers with the highest number of successful food claims:")
print(provider_successful_claims_named)
# Count claims by status
claims_status_counts = claims['Status'].value_counts(normalize=True) * 100

print("Percentage of food claims by status:")
print(claims_status_counts)
# Merge claims with food_listings to get quantity per claim
claims_with_qty = claims.merge(food_listings[['Food_ID', 'Quantity']], on='Food_ID', how='left')

# Calculate average quantity claimed per receiver
average_claimed_per_receiver = claims_with_qty.groupby('Receiver_ID')['Quantity'].mean().reset_index()

# Join to get receiver names
average_claimed_per_receiver_named = average_claimed_per_receiver.merge(receivers[['Receiver_ID', 'Name']], on='Receiver_ID')

print("Average quantity of food claimed per receiver:")
print(average_claimed_per_receiver_named)
# Merge claims with food_listings to get meal types
claims_with_meal_type = claims.merge(food_listings[['Food_ID', 'Meal_Type']], on='Food_ID', how='left')

# Count claims by meal type
claims_meal_type_counts = claims_with_meal_type['Meal_Type'].value_counts().reset_index()
claims_meal_type_counts.columns = ['Meal_Type', 'Claims_Count']

print("Number of food claims by meal type:")
print(claims_meal_type_counts)
# Group total quantity by Provider_ID
total_quantity_by_provider = food_listings.groupby('Provider_ID')['Quantity'].sum().reset_index()

# Merge with providers to get provider names
total_quantity_by_provider_named = total_quantity_by_provider.merge(providers[['Provider_ID', 'Name']], on='Provider_ID')

# Sort descending by total quantity
total_quantity_by_provider_named = total_quantity_by_provider_named.sort_values(by='Quantity', ascending=False)

print("Total quantity of food donated by each provider:")
print(total_quantity_by_provider_named)

# Save Providers DataFrame
providers.to_csv('providers_data.csv', index=False)

# Save Receivers DataFrame
receivers.to_csv('receivers_data.csv', index=False)

# Save Food Listings DataFrame
food_listings.to_csv('food_listings_data.csv', index=False)

# Save Claims DataFrame
claims.to_csv('claims_data.csv', index=False)

# If you have any summary or EDA results DataFrame, you can also save it:
# eda_results.to_csv('eda_results.csv', index=False)