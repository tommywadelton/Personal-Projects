#I wrote this code to calculate the estimated carbon footprint of a flight and how much I need to donate to offset that amount
#I am an avid traveler, but also am big on trying to find ways to fight climate change
#I like practical scripts like this that give me an actionable answer to a question I have
#import packages

import pandas as pd
from math import radians, sin, cos, sqrt, atan2

#the excel sheet contains information on trips I have taken (starting/ending location, date, and the lat/long of each corresponding airport)
#Sample data in the excel sheet is in this format:
#Trip	Date	 Starting Location City Name	Starting Location Code	Layover	Ending Location City Name	Ending Location Code	Roundtrip	Starting_Lat	Starting_Long	Layover_Lat	Layover_Long	Ending_Lat	Ending_Long
#1	  08/25/2023	      Denver	                   DEN	                  N	           Indianapolis	         IND	               Y	     39.86166667	-104.6731667	      0	        0	        39.71730556	-86.29463889

df = pd.read_excel('C:\\Users\\twadel816\\Downloads\\US_Airport_Data.xlsx', sheet_name='Travel_to_Date')

df['Date'] = pd.to_datetime(df['Date'])


distances_2023 = []  # List to store distances
distances_2024 = []  # List to store distances

df_2023 = df.where(df['Year'] == 2023).dropna()
df_2024 = df.where(df['Year'] == 2024).dropna()


for trip in df['Trip']:
    if df.iloc[int(trip) - 1]['Roundtrip'] == 'Y' and df.iloc[int(trip) - 1]['Year'] == 2023:
        #calculate the distance between the two airports in km's
        #This takes the lat/long of the starting and ending location, turns them into radians, and then calculates the distance between those 2 locations
        #It is an approximation, because the calculation takes the straight line distance between the two
        #It does not take into account the actual flight path taken
        #Distance is in KM's, converted to miles later
        
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
        distances_2023.append(distance)
    
    elif df.iloc[int(trip) - 1]['Roundtrip'] == 'N' and df.iloc[int(trip) - 1]['Year'] == 2023:
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
        distances_2023.append(distance)
        
    elif df.iloc[int(trip) - 1]['Roundtrip'] == 'Y' and df.iloc[int(trip) - 1]['Year'] == 2024:
        #calculate the distance between the two airports in km's
        #This takes the lat/long of the starting and ending location, turns them into radians, and then calculates the distance between those 2 locations
        #It is an approximation, because the calculation takes the straight line distance between the two
        #It does not take into account the actual flight path taken
        
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
        distances_2024.append(distance)
    
    elif df.iloc[int(trip) - 1]['Roundtrip'] == 'N' and df.iloc[int(trip) - 1]['Year'] == 2024:
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
        distances_2024.append(distance)

# Now you can use the distances list outside of the loop
for trip, (distance, start, end, date, trip) in enumerate(zip(distances_2023, df_2023['Starting Location City Name'], df_2023['Ending Location City Name'], df_2023['Date'], df_2023['Trip']), start=1):
    carbon_calc = distance * .115
    distance_miles = distance * .62
    carbon_calc = int(carbon_calc)
    #Based on my online resarch, this is an estimate of the C02 offset between trees planted and distance traveled 
    trees = (carbon_calc/ 454) * 5
    #teamtrees.org donates a tree per dollar
    #I currently donate with Wren as they are a little more well known for their environmental impacts
    #Turns the calculation into a dollar format
    
    trip = int(trip)
    trees_dollars = "${:,.2f}".format(trees)
    formatted_date = date.strftime("%m/%d/%Y")
 
    print(f"Trip #{trip}: {start} to {end} on {formatted_date}, {distance_miles} miles, produced {carbon_calc}kg of C02. I need to donate {trees_dollars} to offset this amount")

for trip, (distance, start, end, date, trip) in enumerate(zip(distances_2024, df_2024['Starting Location City Name'], df_2024['Ending Location City Name'], df_2024['Date'], df_2024['Trip']), start=1):
    carbon_calc = distance * .115
    distance_miles = distance * .62
    carbon_calc = int(carbon_calc)
    #Based on my online resarch, this is an estimate of the C02 offset between trees planted and distance traveled 
    trees = (carbon_calc/ 454) * 5
    #teamtrees.org donates a tree per dollar
    #I currently donate with Wren as they are a little more well known for their environmental impacts
    #Turns the calculation into a dollar format
    
    trees_dollars = "${:,.2f}".format(trees)
    formatted_date = date.strftime("%m/%d/%Y")
    trip = int(trip)
 
    print(f"Trip #{trip}: {start} to {end} on {formatted_date}, {distance_miles} miles, produced {carbon_calc}kg of C02. I need to donate {trees_dollars} to offset this amount")


total_distance_2023 = sum(distances_2023)
distance_miles = total_distance_2023 * .62
distance_miles = int(distance_miles)
carbon_calc = total_distance_2023 * .115
carbon_calc = int(carbon_calc)
trees = (carbon_calc/ 454) * 5
trees_dollars = "${:,.2f}".format(trees)
trip_number = int(max(df['Trip'].where(df['Year'] == 2023)))

print("\n2023 Stats:")
print(f"My total Carbin Footprint from air travel in 2023 is approximately {carbon_calc} kg of C02")
print("To offset my total C02 contribution, I need to donate " + str(trees_dollars))
print(f"In 2023, I have traveleled {distance_miles} miles during {trip_number} trip(s)")

total_distance_2024 = sum(distances_2024)
distance_miles = total_distance_2024 * .62
distance_miles = int(distance_miles)
carbon_calc = total_distance_2024 * .115
carbon_calc = int(carbon_calc)
trees = (carbon_calc/ 454) * 5
trees_dollars = "${:,.2f}".format(trees)
trip_number = int(max(df['Trip'])) - int(max(df['Trip'].where(df['Year'] == 2023)))

print("\n2024 Stats:")
print(f"My total Carbin Footprint from air travel in 2024 is approximately {carbon_calc} kg of C02")
print("I need to donate " + str(trees_dollars) + " to offset my 2023 total C02 contribution.")
print(f"In 2024, I have traveleled {distance_miles} miles during {trip_number} trip(s)")

print("\nAll Time Stats:")

total_distance_all_Time = sum(distances_2023) + sum(distances_2024)
distance_miles = total_distance_all_Time * .62
distance_miles = int(distance_miles)
carbon_calc = total_distance_all_Time * .115
carbon_calc = int(carbon_calc)
trees = (carbon_calc/ 454) * 5
trees_dollars = "${:,.2f}".format(trees)
trip_number = int(max(df['Trip']))

print(f"My total Carbin Footprint from air travel is approximately {carbon_calc} kg of C02")
print("I need to donate " + str(trees_dollars) + " to offset my 2024 total C02 contribution.")
print(f"In Total, I have traveleled {distance_miles} miles during {trip_number} trips") 
