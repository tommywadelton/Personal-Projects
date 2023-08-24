# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 16:38:19 2023

@author: twadel816
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:28:44 2023

@author: twadel816
"""
#import packages
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

#the excel sheet contains information on trips I have taken (starting/ending location, date, and the lat/long of each corresponding airport)

df = pd.read_excel('C:\\Users\\twadel816\\Downloads\\US_Airport_Data.xlsx', sheet_name='Travel_to_Date_2')
distances = []  # List to store distances

for trip in df['Trip']:
    if df.iloc[int(trip) - 1]['Roundtrip'] == 'Y':
        #calculate the distance between the two airports in km's
        
        R = 6373.0
        lat1 = radians(df.iloc[int(trip) - 1]['Starting_Lat'])
        lon1 = radians(df.iloc[int(trip) - 1]['Starting_Long'])
        lat2 = radians(df.iloc[int(trip) - 1]['Ending_Lat'])
        lon2 = radians(df.iloc[int(trip) - 1]['Ending_Long'])
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c
        #multiplied by 2 for roundtrip
        
        distance = round(distance, 0) * 2
        distances.append(distance)
    
    elif df.iloc[int(trip) - 1]['Roundtrip'] == 'N':
        R = 6373.0
        lat1 = radians(df.iloc[int(trip) - 1]['Starting_Lat'])
        lon1 = radians(df.iloc[int(trip) - 1]['Starting_Long'])
        lat2 = radians(df.iloc[int(trip) - 1]['Ending_Lat'])
        lon2 = radians(df.iloc[int(trip) - 1]['Ending_Long'])
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c
        distance = round(distance, 0) * 1
        distances.append(distance)

# Now you can use the distances list outside of the loop
for trip, (distance, start, end, date) in enumerate(zip(distances, df['Starting Location City Name'], df['Ending Location City Name'], df['Date']), start=1):
    carbon_calc = distance * .115
    distance_miles = distance * .62
    carbon_calc = int(carbon_calc)
    trees = (carbon_calc/ 454) * 5
    trees_dollars = "${:,.2f}".format(trees)
    
    formatted_date = date.strftime("%m/%d/%Y")

    #prints the trip details, from where to where, on what date, totalling how many miles and the amount of trees/money it will take to donate to offset my carbon footprint based on this flight
    
    print(f"My trip from {start} to {end} on {formatted_date}, {distance_miles} miles, produced {carbon_calc}kg of C02. I need to donate {trees_dollars} to offset this amount")


#Total amount so far

total_distance = sum(distances)
carbon_calc = total_distance * .115
carbon_calc = int(carbon_calc)
trees = (carbon_calc/ 454) * 5
trees_dollars = "${:,.2f}".format(trees)
print("\nTo offset my total C02 contribution, I need to donate " + str(trees_dollars))
