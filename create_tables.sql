CREATE TABLE IF NOT EXISTS providers (
    Provider_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Type TEXT,
    Address TEXT,
    City TEXT,
    Contact TEXT
);

CREATE TABLE IF NOT EXISTS receivers (
    Receiver_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Type TEXT,
    City TEXT,
    Contact TEXT
);

CREATE TABLE IF NOT EXISTS food_listings (
    Food_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Food_Name TEXT NOT NULL,
    Quantity INTEGER NOT NULL,
    Expiry_Date DATE NOT NULL,
    Provider_ID INTEGER NOT NULL,
    Provider_Type TEXT,
    Location TEXT,
    Food_Type TEXT,
    Meal_Type TEXT,
    FOREIGN KEY (Provider_ID) REFERENCES providers(Provider_ID)
);

CREATE TABLE IF NOT EXISTS claims (
    Claim_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Food_ID INTEGER NOT NULL,
    Receiver_ID INTEGER NOT NULL,
    Status TEXT,
    Timestamp DATETIME,
    FOREIGN KEY (Food_ID) REFERENCES food_listings(Food_ID),
    FOREIGN KEY (Receiver_ID) REFERENCES receivers(Receiver_ID)
);
