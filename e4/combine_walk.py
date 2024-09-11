# Exercise 4
# Author: Md Rownak Abtahee Diganta 
# Student ID: 301539632 

import os
import pathlib
import sys
import numpy as np
import pandas as pd
from xml.dom.minidom import parse, parseString
from xml.dom.minidom import getDOMImplementation
from math import cos, asin, sqrt, pi


def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation, parse
    xmlns = 'http://www.topografix.com/GPX/1/0'
    
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.10f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.10f' % (pt['lon']))
        time = doc.createElement('time')
        time.appendChild(doc.createTextNode(pt['datetime'].strftime("%Y-%m-%dT%H:%M:%SZ")))
        trkpt.appendChild(time)
        trkseg.appendChild(trkpt)

    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)

    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)

    doc.documentElement.setAttribute('xmlns', xmlns)

    with open(output_filename, 'w') as fh:
        fh.write(doc.toprettyxml(indent='  '))


def get_data(input_gpx):
    # TODO: you may use your code from exercise 3 here.
        #print(input_gpx)
        # Read the GPX file and parse it
    # Ref : https://stackoverflow.com/questions/67137305/how-do-i-deploy-jupyter-to-medium-attributeerror-posixpath-object-has-no-at (Gained knowledge only as encountering errors)
    with open(input_gpx, 'r') as f:
        #f = f.read()
        file = parse(f)
    #file = parse(input_gpx)
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
    
    
    
    data_frame = pd.DataFrame({'timestamp':time_list,'lat': lat_list,'lon':lon_list})
    
    # Given in the hint
    data_frame['timestamp'] = pd.to_datetime(data_frame['timestamp'], utc=True, format= 'mixed')
    data_frame['lat'] = data_frame['lat'].astype(float)
    data_frame['lon'] = data_frame['lon'].astype(float)
    #print(data_frame)
    return data_frame
    #pass


def main():
    input_directory = pathlib.Path(sys.argv[1])
    output_directory = pathlib.Path(sys.argv[2])
    
    accl = pd.read_json(input_directory / 'accl.ndjson.gz', lines=True, convert_dates=['timestamp'])[['timestamp', 'x']]
    gps = get_data(input_directory / 'gopro.gpx')
    phone = pd.read_csv(input_directory / 'phone.csv.gz')[['time', 'gFx', 'Bx', 'By']]

    first_time = accl['timestamp'].min()
    
    # TODO: create "combined" as described in the exercise
    # Given instruction 
    # Assuming the phone data starts at exactly the same time as the accelerometer data 
    #offset = 0
    #first_time = accl['timestamp'].min()
    #phone['timestamp'] = first_time + pd.to_timedelta(phone['time'] + offset, unit='sec')
    
    # To unify the times, we will aggregate using 4 second bins (i.e. round to the nearest 4 seconds, hint 1), 
    # then group on the rounded-times, and average all of the other values (hint 2, hint 3).
    # Followed hint 1

    #phone['timestamp'] = phone['timestamp'].round('4S')
    #accl['timestamp'] = accl['timestamp'].round('4S')
    #gps['timestamp']  = gps['timestamp'].round('4S')
    
    # Followed hint 2 and hint 3
    #phone = phone.groupby(['timestamp']).mean()
    #accl = accl.groupby(['timestamp']).mean()
    #gps = gps.groupby(['timestamp']).mean()
    
    #print(phone)
    #print(accl)
    #print(gps)
    
    # Correlating Data sets 
    # Now, we have to work with real problem as the prof did not press record at the exact same time 
    
    # Initializing
    highest_cross_correlation = 0
    best_offset = 0
    for offset in np.linspace(-5.0, 5.0, 101):
        # Followig the given instruction
        phone['timestamp'] = first_time + pd.to_timedelta(phone['time'] + offset, unit='sec')
        # Followed hint 1
        phone['timestamp'] = phone['timestamp'].round('4S')
        accl['timestamp']  = accl['timestamp'].round('4S')
        gps['timestamp']   = gps['timestamp'].round('4S')

        # Followed hint 2 and hint 3
        phone_grouped = phone.groupby(['timestamp']).mean().reset_index()
        accl_grouped  = accl.groupby(['timestamp']).mean().reset_index()
        gps_grouped   = gps.groupby(['timestamp']).mean().reset_index()

        # Combining data 
        # ref: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html (Gained knowledge)
        
        combined_0 = pd.merge(accl_grouped, gps_grouped, on='timestamp',how = 'inner')
        combined = pd.merge(combined_0, phone_grouped, on='timestamp',how = 'inner')
        
        # Ref: https://www.geeksforgeeks.org/python-pandas-dataframe-series-dot/ (Gained knowledge)
        # dot_product = phone['gFx'].dot(accl['x'])  # Error
        #print(dot_product)
        dot_product = combined['gFx'].dot(combined['x'])
        cross_correlation = dot_product
        
        # Finding the best offset as per the given hints and instructions 
        if cross_correlation > highest_cross_correlation:
            highest_cross_correlation = cross_correlation
            best_offset = offset

        
  
        #print(phone)
        #print(accl)
        #print(gps)
    #   print(combined)

    
    # Using the best offset that I found 
    phone['timestamp'] = first_time + pd.to_timedelta(phone['time'] + best_offset, unit='sec')
    phone['timestamp'] = phone['timestamp'].round('4S')
    phone_grouped = phone.groupby(['timestamp']).mean().reset_index()

    combined_0 = pd.merge(accl_grouped, gps_grouped, on='timestamp',how = 'inner')
    combined = pd.merge(combined_0, phone_grouped, on='timestamp',how = 'inner')
    

    print(f'Best time offset: {best_offset:.1f}')
    #print(combined)
    # Ref: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html (Gained knowledge)
    combined.rename(columns = {"timestamp":"datetime"}, inplace = True)
    os.makedirs(output_directory, exist_ok=True)
    output_gpx(combined[['datetime', 'lat', 'lon']], output_directory / 'walk.gpx')
    combined[['datetime', 'Bx', 'By']].to_csv(output_directory / 'walk.csv', index=False)
    

main()
