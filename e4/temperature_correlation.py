# Exercise 4
# Author: Md Rownak Abtahee Diganta 
# Student ID: 301539632 
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import cos, asin, sqrt, pi

# Taken from exercise 3 
# Source: https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
# Haversine formula to calculate the distance between two lat/lon points
def haversine_formula(lat1, lon1, lat2, lon2):
    r = 6371 * 1000  # Earth radius in meters
    p = pi / 180

    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 2 * r * asin(sqrt(a))

# Function to calculate distance between a city and all stations
def distance(city, stations):
    city_lat = city['latitude']
    city_lon = city['longitude']
    # ref: https://www.geeksforgeeks.org/apply-function-to-every-row-in-a-pandas-dataframe/ (Gained knowledge from this site )
    distances = stations.apply(lambda station: haversine_formula(city_lat, city_lon, station['latitude'], station['longitude']), axis=1)
    return distances


def best_tmax(city, stations):
    distances = distance(city, stations)
    
    # Followed the given hint 
    closest_station = np.argmin(distances)
    return stations.at[closest_station,'avg_tmax']
def main():
    
    # The last command line argument should be the filename for the plot you'll output (described below).
    # python3 temperature_correlation.py stations.json.gz city_data.csv output.svg
    # There are 3 arguments hence there should be 3 variables to take these arguments 
    
    #stations_argument = sys.argv[1]
    stations_file = sys.argv[1]
    city_argument = sys.argv[2]
    output_argument = sys.argv[3]
    
    stations = pd.read_json(stations_file, lines=True)
    stations['avg_tmax'] = stations['avg_tmax']/10
    #print(stations)
    cities = pd.read_csv(city_argument)
    cities = cities.dropna()                               # Dropping all the NaN values 
    
    # The city area is given in m², which is hard to reason about: convert to km²
    cities['area'] = cities['area']/ 1000000
    cities = cities[cities['area'] <= 10000]
    cities['density'] = cities['population']/cities['area']
    cities['avg_tmax'] = cities.apply(best_tmax, stations=stations, axis=1)
    #print(cities)
    
    plt.scatter(cities['avg_tmax'], cities['density'], alpha=0.4)
    plt.ylabel('Population Density (people/km\u00b2)')
    plt.xlabel('Avg Max Temperature (\u00b0C)')
    plt.title('Temperature vs Population Density')
    plt.savefig(output_argument)
    #plt.show()
    
if __name__ == '__main__':
    main()