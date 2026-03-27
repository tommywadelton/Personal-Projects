#I opted to write my own code for this project example

## Part 1 ## - Python code development and comprehension
##########################
#You have been given 4 csv files of data and 1 empty sqlite database (ibotta.db)
#Using PYTHON, write some code to load the 4 csv files into a database with their respective
#table names (offer_rewards, customer_offers, customer_offer_rewards
#customer_#offer_redemptions). As mentioned, there is provided an empty sqlite db for your
#convenience but you can use your own type of SQL database if you so choose.
#Loading the 4 csv's into my local machine

import pandas as pd
import sqlite3
import os
#I made the location of the CSV's on my machine the currect directory, so I dont have to use the entire folder path each time
os.chdir('.../Downloads/for_candidate')

#loading the csv files into dataframes
#parsing each csv's date column(s)

customer_offer_redemptions = pd.read_csv('CSV_data/customer_offer_redemptions_31025.csv', parse_dates=['CREATED_AT'])
customer_offer_rewards= pd.read_csv('CSV_data/customer_offer_rewards_144392.csv', parse_dates=['FINISHED', 'CREATED_AT'])
customer_offers = pd.read_csv('CSV_data/customer_offers_296332.csv', parse_dates=['ACTIVATED'])
offer_rewards = pd.read_csv('CSV_data/offer_rewards_168083.csv', parse_dates=['CREATED_AT', 'UPDATED_AT'])

#normalizing the date columns to all be in the YYYY-MM-DD HH:MM:SS format

def normalize_datetimes(df):
    for col in df.select_dtypes(include=["datetime64[ns]"]):
        df[col] = df[col].dt.strftime("%Y-%m-%d %H:%M:%S")
    return df

customer_offer_redemptions = normalize_datetimes(customer_offer_redemptions)
customer_offer_rewards = normalize_datetimes(customer_offer_rewards)
customer_offers = normalize_datetimes(customer_offers)
offer_rewards = normalize_datetimes(offer_rewards)

#printing the top 10 rows of the CSVs in this for loop so I can see the data in each and get familiar 

dfs = [
    ("customer_offer_redemptions", customer_offer_redemptions), 
    ("customer_offer_rewards", customer_offer_rewards), 
    ("customer_offers", customer_offers), 
    ("offer_rewards", offer_rewards)
]

# Used to not cut off if a dataframe has a lot of rows/columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#prints the name and data for each of the above dataframes
for name, df in dfs:
    print(f"\n{name}\n")
    print(df.head(10))
    
#call the path of the predefined ibotta database
    
db_path = "Database/ibotta.db"

#call the connection to the database, using the sqlite3 package installed at the top
conn = sqlite3.connect(db_path)

#write each table with their corresponding data types
print("\nTable customer_offer_redemptions was written to the ibotta database")

customer_offer_redemptions.to_sql(
    "customer_offer_redemptions",
    conn,
    if_exists="replace",
    index=False,
    dtype={
        "ID": "INTEGER",
        "CUSTOMER_OFFER_ID": "INTEGER",
        "VERIFIED_REDEMPTION_COUNT": "INTEGER",
        "SUBMITTED_REDEMPTION_COUNT": "INTEGER",
        "OFFER_AMOUNT": "REAL",
        "CREATED_AT": "TEXT"
    }
)

print("Table customer_offer_rewards was written to the ibotta database")

customer_offer_rewards.to_sql(
    "customer_offer_rewards",
    conn,
    if_exists="replace",
    index=False,
    dtype={
        "ID": "INTEGER",
        "CUSTOMER_ID": "INTEGER",
        "OFFER_REWARD_ID": "INTEGER",
        "FINISHED": "TEXT",
        "CREATED_AT": "TEXT"
    }
)

print("Table customer_offers was written to the ibotta database")

customer_offers.to_sql(
    "customer_offers",
    conn,
    if_exists="replace",
    index=False,
    dtype={
        "ID": "INTEGER",
        "CUSTOMER_ID": "INTEGER",
        "OFFER_ID": "INTEGER",
        "ACTIVATED": "TEXT",
        "VERIFIED": "TEXT"
    }
)

print("Table offer_rewards was written to the ibotta database")

offer_rewards.to_sql(
    "offer_rewards",
    conn,
    if_exists="replace",
    index=False,
    dtype={
        "ID": "INTEGER",
        "OFFER_ID": "INTEGER",
        "TYPE": "TEXT",
        "AMOUNT": "REAL",
        "CREATED_AT": "TEXT",
        "UPDATED_AT": "TEXT"
    }
)

#commit and close the connetion to sql after writing the data
conn.commit()
conn.close()