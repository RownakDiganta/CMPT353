# Exercise 3
# Author: Md Rownak Abtahee Diganta 
# Student ID: 301539632 

import sys 
import pandas as pd 
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess # From the slides
from pykalman import KalmanFilter                             # From slides 
import numpy as np
from xml.dom.minidom import parse, parseString
from xml.dom.minidom import getDOMImplementation
from math import cos, asin, sqrt, pi

def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """

    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.7f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.7f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')

def get_data(input_gpx):
    #print(input_gpx)
    file = parse(input_gpx)
    #print(file)
    # ref : https://www.geeksforgeeks.org/parse-xml-using-minidom-in-python/ (Gained knowledge of this library from this site)
    trkpt_tag = file.getElementsByTagName('trkpt')
    #print(trkpt_tag)
    
    # Creating empty lists
    lat_list = []
    lon_list = []
    time_list = []
    for i in trkpt_tag:
        lat_list.append(i.getAttribute('lat'))
        lon_list.append(i.getAttribute('lon'))
        # ref: https://www.geeksforgeeks.org/parsing-xml-with-dom-apis-in-python/?ref=ml_lbp (Gained knowledge of this library from this site)
        time_list.append(i.getElementsByTagName('time')[0].firstChild.data)
        
        
    #time_tag = file.getElementsByTagName('time')
    #print(time_tag)
    
    
    
    data_frame = pd.DataFrame({'datetime':time_list,'lat': lat_list,'lon':lon_list})
    
    # Given in the hint
    data_frame['datetime'] = pd.to_datetime(data_frame['datetime'], utc=True)
    data_frame['lat'] = data_frame['lat'].astype(float)
    data_frame['lon'] = data_frame['lon'].astype(float)
    #print(data_frame)
    return data_frame


# Source: https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
def haversine_formula(lat1, lon1, lat2, lon2):
    r = 6371 * 1000 # meter 
    p = pi / 180

    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 2 * r * asin(sqrt(a))

def distance(data_file):
    data_file['lat2'] = data_file['lat'].shift(-1)
    data_file['lon2'] = data_file['lon'].shift(-1)
    
    print("Dataframe with Shifted Columns:")
    print(data_file.head())
# ref: https://www.geeksforgeeks.org/apply-function-to-every-row-in-a-pandas-dataframe/ (Gained knowledge from this site )
    distance_meter = data_file.apply(lambda row : haversine_formula(row['lat'],row['lon'],row['lat2'],row['lon2']), axis = 1)
    print("Distances Calculated for Each Row:")
    print(distance_meter.head())# Apply the function to every row 
    sum_distance = distance_meter.sum(axis = 0)
    #print(sum_distance)
    print("Total Distance:")
    print(sum_distance)
    return sum_distance

def smooth(points) : 
    # took help from 1st question (smooth_temperature.py), which is done by me
    initial_state = points[['lat','lon']].iloc[0]
    observation_covariance = np.diag([0.71, 0.71]) ** 2 # TODO: shouldn't be zero
    transition_covariance = np.diag([0.89, 0.89]) ** 2 # TODO: shouldn't be zero
    transition = [[1,0], [0,1]] # TODO: shouldn't (all) be zero
    
    # From slide
    kf = KalmanFilter(    
    initial_state_mean=initial_state,
    initial_state_covariance=observation_covariance,
    observation_covariance=observation_covariance,
    transition_covariance=transition_covariance,
    transition_matrices=transition)

    # Taken from hint
    kalman_smoothed, _ = kf.smooth(points[['lat','lon']])
    kalman_data_frame = pd.DataFrame(kalman_smoothed, columns =['lat','lon'])
    return kalman_data_frame


def main():
    input_gpx = sys.argv[1]
    input_csv = sys.argv[2]
    
    points = get_data(input_gpx).set_index('datetime')
    #print(points['lat']) # Checking value
    
    
    sensor_data = pd.read_csv(input_csv, parse_dates=['datetime']).set_index('datetime')
    points['Bx'] = sensor_data['Bx']
    points['By'] = sensor_data['By']
    # print(points['By']) # Checking value
    


    dist = distance(points)
    
    print(f'Unfiltered distance: {dist:.2f}')

    smoothed_points = smooth(points)
    
    smoothed_dist = distance(smoothed_points)
    print(f'Filtered distance: {smoothed_dist:.2f}')

    output_gpx(smoothed_points, 'out.gpx')

if __name__ == '__main__':
    main()