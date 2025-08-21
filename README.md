# Local Food Wastage Management System

## Project by Manvi

---

## Overview

This Streamlit-powered application helps connect surplus food providers (restaurants, grocery stores, individuals) with NGOs and communities in need. The goal is to reduce local food wastage by redistributing excess food efficiently using a structured database, analysis, and an interactive dashboard.

---

## Features

- List and claim surplus food items
- Filtering by city, provider, food type, and meal type
- Display outputs of 15+ SQL queries for analysis
- Contact food providers and receivers directly
- CRUD operations for food listings and claims (Add, Update, Delete)
- Visualize food wastage patterns using Plotly charts
- SQL-powered data storage and query engine
- Easy, user-friendly interface built with Streamlit

---

## Folder Structure
Food-Wastage-Project/
│
├── app.py # Main Streamlit app
├── requirements.txt # Python packages
├── README.md # This documentation file
├── .gitignore # For Git version control
│
├── data/
│ ├── providers_data.csv
│ ├── receivers_data.csv
│ ├── food_listings_data.csv
│ └── claims_data.csv
│
├── sql/
│ ├── create_tables.sql
│ ├── insert_data.sql
│ └── queries.sql
│
├── src/
│ ├── data_cleaning.py
│ ├── db_utils.py
│ └── analysis.py
│
└── notebooks/
└── food_eda.ipynb
## How to Run

1. *Install dependencies*
    
    pip install -r requirements.txt
    

2. *Set up the SQL database*
    - Use create_tables.sql and insert_data.sql in the sql/ folder to create the database and insert sample data.
    - Set your database connection path/settings in src/db_utils.py.

3. *Start the Streamlit app*
    
    streamlit run app.py
    
    - The app interface will open in your browser (default: http://localhost:8502/).

---

## Data Files

- *providers_data.csv*: All food providers and their details
- *receivers_data.csv*: All NGOs/individuals who claim food
- *food_listings_data.csv*: List of food items available for donation
- *claims_data.csv*: All food claims, statuses, timestamps

---

## Key SQL Analyses

- Providers/receivers grouped by city
- Top contributing provider types
- Contacts by city
- Most claimed receivers
- Total available food quantity
- Food listing counts by city
- Most common food types
- Claims per food item
- Providers with most successful claims
- Claim status percentages (completed/pending/canceled)
- Average claim quantity per receiver
- Most claimed meal type
- Total quantity donated per provider

---

## Deployment

For sharing with mentors and users:
- Deploy on [Streamlit Cloud](https://share.streamlit.io/) to get a public link
- Share your GitHub repository with all code and data files

---

## Contact

Created by: *Manvi*  
If you have questions, reach out or check project files for guidance.

---

## Additional Notes

- All code, data, and queries are version-controlled using Git.
- This project uses Python, SQL, Plotly, and Streamlit.
- For Exploratory Data Analysis, see notebooks/food_eda.ipynb.
