import math
import arcpy, json, os, sys

# Constants for UHF frequencies
FREQUENCY_MIN = 300 # MHz
FREQUENCY_MAX = 3000 # MHz
WAVELENGTH_MIN = 1000 / FREQUENCY_MAX
WAVELENGTH_MAX = 1000 / FREQUENCY_MIN

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
else:
    aprx = arcpy.mp.ArcGISProject(R"C:\Users\chrism\OneDrive - Esri\ArcGIS_Pro_Projects\TFGP_mock_up_data_3\TFGP_mock_up_data_3.aprx")

# Get the feature layer
if arcpy.GetParameter(0):                            
    layer = arcpy.GetParameter(0)                    
else:                                                
    layer = aprx.listMaps("DEV TFGP database")[0].listLayers("links")[0]
features_dict = {}     
features_dict_params = {}                          
frequency = arcpy.GetParameter(1) # MHz
power = arcpy.GetParameter(2) # watts

# Loop through the selected features
for row in arcpy.da.SearchCursor(layer, ["SHAPE@JSON","OBJECTID"]):
    # Parse the JSON representation of the feature's geometry
    feature_json = row[0]
    feature_dict = json.loads(feature_json)
    geometry = feature_dict["paths"][0]

    # Get the beginning and end coordinates of the line
    start_coord = geometry[0]
    end_coord = geometry[-1]

    # Example usage   79.0491424°W 35.1470829°N  79.0775205°W 35.1363622°N
    lat1 = start_coord[1] # Latitude of location 1
    lon1 = start_coord[0] # Longitude of location 1
    lat2 = end_coord[1] # Latitude of location 2
    lon2 = end_coord[0] # Longitude of location 2
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    
    if distance <= 10:
        # frequency = 300 # MHz
        # power = 3 # watts
        signal_strength = calculate_signal_strength(distance, frequency, power)
        features_dict[row[1]] = signal_strength                  #cmac added
        features_dict_params[row[1]] = (f"{frequency} MHz , {power} W, {arcpy.GetParameter(3)} Tx Gain (dBi), {arcpy.GetParameter(4)} Rx Gain (dBi), distance={round(distance,3)}K")
    else:
        arcpy.AddMessage("The distance between the two locations is greater than 10 kilometers. This model is only valid for distances less than 8 kilometers.")

# update selected records using the record ID (rid) as the index to the results generated above
for rid in features_dict:
    expression = arcpy.AddFieldDelimiters(layer, "objectid") + " = " + str(rid)
    fields = ['signal_db']
    with arcpy.da.UpdateCursor(layer, fields, where_clause=expression) as cursor:
        for row in cursor:
            row[0] = round(features_dict[rid],0)
            arcpy.AddMessage("Calculating OBJECTID {} signal_db = {}.".format(rid,row[0]))
            sendMessage(f"{features_dict_params[rid]}",2)
            cursor.updateRow(row)