# -*- coding: utf-8 -*-
"""
Script Name: uhf_signal_strength.py
Description: uses industry accepted RF signal strength calculation model(s) to populate
#              a signal strength value to LOS lines for TSMO communications "link" network
#
# Parameters:
#   Link Layer - existing line feature class where lines between two points represent RF 
#           comminication link.
#       Required fields in line layer: 
#           signal_db: double, stores the signal loss estimate in dBi
#           signal_db_params: text (255), stores the parameters used to determine the signal_db
#   Frequency (MHz) - Double number representing the anticipate radio frequency in megahertz
#   Power (Watts) - Long number representing the power setting on transmitter
#   Transmitter antenna gain (dBi) - Double number with measurement of Antenna gain from transmitter
#   Receiver antenna gain (dBi) - Double number with measurement of Antenna gain from receiver
#
# Description:
#   The tool takes the selected set, or all features if none selected, from Link Layer and
#   processes each record seperately. The model calculates signal loss due to distance
#   using the "Friis transmission formula" and then writes the result to the console and
#   to Link Layer fields (signal_db, signal_db_params).
#
# Author:      chrism
# Created:     02/23/2023
# Copyright:   (c) Esri 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
"""
import math
import arcpy, json, os, sys

# Constants for UHF frequencies -> Replaced with Arctoolbox input parameters. 
# FREQUENCY_MIN = 300 # MHz
# FREQUENCY_MAX = 3000 # MHz
# WAVELENGTH_MIN = 1000 / FREQUENCY_MAX
# WAVELENGTH_MAX = 1000 / FREQUENCY_MIN

def sendMessage(message, indent=0):

    if indent == 0:
        string = message
    if indent > 0 :
        string = "{} {}".format(R" " * indent,message)

    arcpy.AddMessage(string)
    #print(string)

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # radius of the Earth in kilometers

    # convert latitudes and longitudes to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # calculate the differences between latitudes and longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # calculate the haversine of the differences
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2

    # calculate the great circle distance in kilometers
    distance = 2 * R * math.asin(math.sqrt(a))

    # convert kilometers to meters
    #distance *= 1000

    # return distance in kilometers
    return distance

# Function to calculate the signal strength for a given distance, frequency, and transmitter power
def calculate_signal_strength(distance, frequency, power):
    '''the calculate_signal_strength function takes three arguments: 
    the distance between the two locations in kilometers, the frequency 
    of the signal in MHz, and the transmitter power in watts. It calculates 
    the signal strength in decibels relative to one milliwatt (dBm) using 
    the Friis transmission formula with the assumptions of a transmitter 
    antenna gain of 0 dBi and a receiver antenna gain of 0 dBi.'''
    # Assume transmitter antenna gain of 0 dBi
    gt = arcpy.GetParameter(3) if arcpy.GetParameter(3) else 0
    # Assume receiver antenna gain of 0 dBi
    gr = arcpy.GetParameter(4) if arcpy.GetParameter(4) else 0
    # Calculate the free space path loss
    fspl = 20 * math.log10(distance) + 20 * math.log10(frequency) + 32.44
    # Calculate the signal strength using the Friis transmission formula
    signal_strength = 10 * math.log10(power) + gt + gr - fspl
    return signal_strength

# Connect to the ArcGIS Pro project
if os.path.basename(sys.executable) in ['ArcGISPro.exe', 'ArcSOC.exe']:
    aprx = arcpy.mp.ArcGISProject("CURRENT")
else:   # for testing
    aprx = arcpy.mp.ArcGISProject(R"C:\Users\chrism\OneDrive - Esri\ArcGIS_Pro_Projects\TFGP_data_model\TFGP_data_model_31.aprx")

# Get the feature layer
if arcpy.GetParameter(0):                            
    layer = arcpy.GetParameter(0)                    
else:                                                
    layer = aprx.listMaps("tsmo-dev1")[0].listLayers("links")[0]
    
# desc = arcpy.Describe(layer)
# arcpy.env.workspace = 'C:\\Users\\chrism\\OneDrive - Esri\\ArcGIS_Pro_Projects\\TFGP_mock_up_data_3\\PostgreSQL-tsmo-dev3-tsmotfgp(tsmodataowner).sde'
# arcpy.AddMessage(f"Layer:{layer}")
features_dict = {}     
features_dict_params = {}                          
frequency = arcpy.GetParameter(1) # MHz
power = arcpy.GetParameter(2) # watts
max_distance = 50

for row in arcpy.da.SearchCursor(layer, ['SHAPE@','OID@']):
    distance = row[0].getLength("GEODESIC","Meters") / 1000
    
    if distance <= max_distance:
        # frequency = 300 # MHz
        # power = 3 # watts
        signal_strength = calculate_signal_strength(distance, frequency, power)
        features_dict[row[1]] = signal_strength                  #cmac added
        calc_params = f"distance (k): {round(distance,3)}; freq (MHz): {frequency}; power (W): {power}; txgain (dB): {arcpy.GetParameter(3)}; rxgain (dB): {arcpy.GetParameter(4)}"
        features_dict_params[row[1]] = calc_params 
    else:
        arcpy.AddMessage(f"The distance between the two locations is greater than {max_distance} kilometers. This model is only valid for distances less than {max_distance} kilometers.")
        arcpy.AddMessage(f"Distance: {distance}")
# update selected records using the record ID (rid) as the index to the results generated above

test_fields = arcpy.ListFields(layer)
test_fields = [f.name for f in arcpy.ListFields(layer)]

for rid in features_dict:
    arcpy.AddMessage(f"features_dict: {features_dict}")
    arcpy.AddMessage(f"+++ Processing: {rid}:{features_dict[rid]}")
    if 'signal_db' in test_fields:
        expression = arcpy.AddFieldDelimiters(layer, "objectid") + " = " + str(rid)
        fields = ['signal_db','signal_db_params']
        with arcpy.da.UpdateCursor(layer, fields, where_clause=expression) as cursor:
            for row in cursor:
                row[0] = round(features_dict[rid],0)
                row[1] = features_dict_params[rid]
                arcpy.AddMessage("Calculating OBJECTID {} signal_db = {}.".format(rid,row[0]))
                sendMessage(f"{features_dict_params[rid]}",2)
                cursor.updateRow(row)
    elif 'Text' in test_fields:
        expression = arcpy.AddFieldDelimiters(layer, "objectid") + " = " + str(rid)
        fields = ['Text']
        with arcpy.da.UpdateCursor(layer, fields, where_clause=expression) as cursor:
            for row in cursor:
                row[0] = round(features_dict[rid],0)
                row[1] = features_dict_params[rid]
                arcpy.AddMessage("Calculating OBJECTID {} Text = {}.".format(rid,row[0]))
                sendMessage(f"{features_dict_params[rid]}",2)
                cursor.updateRow(row)
    else:
        arcpy.AddMessage(f'Field "signal_db" doesn\'t exist so will not be updated with {round(features_dict[rid],0)}dBm')