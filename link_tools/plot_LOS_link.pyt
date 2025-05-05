# -*- coding: utf-8 -*-
"""
Script Name: plot_LOS_link.pyt
Description: tool allows user to draw a line on the map and calculates 
            the expected RF signal loss/strength using
            the Okumura-Hata Model and Friis transmission formula. 
Author: Cmac
Date: 05-16-2023
"""
import arcpy
import math


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Plot Line of Site"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Link",
            name="in_feature_set",
            datatype="GPFeatureRecordSetLayer",
            parameterType="Required",
            direction="Input")
        
        param1 = arcpy.Parameter(
            displayName="Frequency (MHz)",
            name='frequency',
            datatype='GPDouble',
            parameterType="Required",
            direction="Input")
        param1.value=800
        
        param2 = arcpy.Parameter(
            displayName="Power (Watts)",
            name='power',
            datatype='GPDouble',
            parameterType="Required",
            direction="Input")
        param2.value = 5

        param3 = arcpy.Parameter(
            displayName="Transmitter antenna gain (dBi)",
            name='txgain',
            datatype='GPDouble',
            parameterType="Required",
            direction="Input")
        param3.value = 0
        
        param4 = arcpy.Parameter(
            displayName="Receiver antenna gain (dBi)",
            name='rxgain',
            datatype='GPDouble',
            parameterType="Required",
            direction="Input")
        param4.value = 0
        
        param5 = arcpy.Parameter(
            displayName="Messages",
            name='result',
            datatype='GPString',
            parameterType="Derived",
            direction="Output")
        param5.value = 'no info'

        param6 = arcpy.Parameter(
            displayName="Transmitter antenna height (m)",
            name='txheight',
            datatype='GPDouble',
            parameterType="Required",
            direction="Input")
        param6.value = 10

        param7 = arcpy.Parameter(
            displayName="Receiver antenna height (m)",
            name='rxheight',
            datatype='GPDouble',
            parameterType="Required",
            direction="Input")
        param7.value = 10
        
        param8 = arcpy.Parameter(
            displayName="Irregular Terrain?",
            name='irterrain',
            datatype='GPBoolean',
            parameterType="Required",
            direction="Input")
        param8.value = True
        
        
        params = [param0, param1, param2, param3, param4, param5, param6, param7, param8]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        
        lyr_links = parameters[0].value
        freq = parameters[1].value
        power = parameters[2].value
        txgain = parameters[3].value
        rxgain = parameters[4].value
        parameters[5].value = f'reading line(s) from "{lyr_links.name}"'
        txheight = parameters[6].value
        rxheight = parameters[7].value  
        irterrain = parameters[8].value
              
        arcpy.AddMessage(f'reading line(s) from "{lyr_links.name}"')
        result_message = []

        sr = arcpy.SpatialReference(4326) # WGS 1984       

        los_features = [row for row in arcpy.da.SearchCursor(lyr_links, ['SHAPE@','OID@'])]
        
        for los_feature in los_features:
            result_message.append(f"\nCalculating signal strength for OBJECTID = {los_feature[1]}")
            ssid = los_feature[1]
            distance = round(los_feature[0].getLength("GEODESIC","Meters") / 1000,2)
                       
            friis = calculate_signal_strength(distance, freq, power, txgain, rxgain )
            okumura = okumura_hata(freq, power, txgain, rxgain, txheight, rxheight, distance)

            
            result_message.append(f'Method: FSPL + Friis transmission formula')
            result_message.append(f'Signal: {friis}; distance: {distance}; freq: {freq}; power: {power}; txgain: {txgain}; rxgain: {rxgain}')
            result_message.append(f'Method: Okumura')
            result_message.append(f'Signal: {okumura}; distance: {distance}; freq: {freq}; power: {power}; txgain: {txgain}; rxgain: {rxgain}')
                       
            calc_params = f"distance (k): {distance}; freq (MHz): {freq}; power (W): {power}; txgain (dB): {txgain}; rxgain (dB): {rxgain}"
            
            writeResult(ssid, lyr_links,okumura,calc_params)
            
        for mess in result_message:
            arcpy.AddMessage(mess)
            parameters[5].value += "\n" + mess 
                                             
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        
        # aprx = arcpy.mp.ArcGISProject("CURRENT")
        # map = aprx.activeMap
        # #layer = map.listLayers(lyr_links)[0]
        # map.removeLayer(parameters[0].value)
        
        return

# Function to calculate the signal strength for a given distance, frequency, and transmitter power
def calculate_signal_strength(distance, frequency, power, txgain=0, rxgain=0):
    '''the calculate_signal_strength function takes three arguments: 
    the distance between the two locations in kilometers, the frequency 
    of the signal in MHz, and the transmitter power in watts. It calculates 
    the signal strength in decibels relative to one milliwatt (dBm) using 
    the Friis transmission formula with the assumptions of a transmitter 
    antenna gain of 0 dBi and a receiver antenna gain of 0 dBi.'''

    # Calculate the free space path loss
    fspl = 20 * math.log10(distance) + 20 * math.log10(frequency) + 32.44
    # Calculate the signal strength using the Friis transmission formula
    signal_strength = 10 * math.log10(power) + txgain + rxgain - fspl
    return round(signal_strength,2)



def okumura_hata(freq, power, tx_gain, rx_gain, tx_height, rx_height, distance):
    """
    Calculate the signal strength loss in dBm using the Okumura-Hata Model.
    
    Args:
    freq (float): UHF frequency in MHz.
    power (float): Transmitter power in watts.
    tx_gain (float): Transmitter antenna gain in dBi.
    rx_gain (float): Receiver antenna gain in dBi.
    tx_height (float): Height of transmitter in meters.
    rx_height (float): Height of receiver in meters.
    distance (float): Distance between transmitter and receiver in kilometers.
    
    Returns:
    float: Signal strength loss in dBm.
    """
    # Convert frequency to MHz
    f = freq / 1000000.0
    
    # Calculate mobile station antenna height h_m
    h_m = 1.5
    
    # Calculate median effective height of the terrain h_b (height of base station)
    #   73.0 * math.log10(distance): This part calculates the path loss due to distance attenuation. It uses the logarithm (base 10) of the distance and multiplies it by a constant value of 73.0. The result represents the path loss in decibels (dB) caused by the distance between the transmitter and receiver.
    #   - 3.0 * math.log10(tx_height): This part calculates the path loss due to the height of the transmitter antenna. It uses the logarithm (base 10) of the transmitter height and multiplies it by a constant value of -3.0. The negative sign indicates that as the transmitter height increases, the path loss decreases.
    #   + 2.0: This part adds a constant value of 2.0 to account for additional factors in the model, such as diffraction and scattering.
    h_b = 73.0 * math.log10(distance) - 3.0 * math.log10(tx_height) + 2.0
    
    # Calculate the path loss due to free space propagation
    L_fs = 32.44 + 20.0 * math.log10(distance) + 20.0 * math.log10(f)
    
    #   L_50: represents the median path loss. It is the path loss value that is exceeded by 50% of the cases. In other words, it represents the typical path loss experienced in the given environment for a specific set of parameters such as frequency, distance, and antenna heights. L_50 is often used as a reference value for path loss calculations.
    #   L_90: represents the path loss value exceeded by 90% of the cases. It is a higher value compared to L_50, indicating a more extreme or worse-case scenario in terms of path loss. L90 is used to account for situations where the path loss can be significantly higher due to unfavorable conditions or obstacles in the propagation environment. 
    
    # Calculate the path loss due to terrain irregularities
    if distance <= 0.1:
        L_50 = 8.29 * math.pow(math.log10(1.54*h_m), 2) - 1.1
    else:
        #   (1.1*math.log10(f)-0.7)*h_m: This part calculates a term related to the frequency (f) and the mobile station height (h_m). It takes the logarithm (base 10) of the frequency, multiplies it by 1.1, subtracts 0.7, and then multiplies the result by the mobile station height. This term represents the influence of the frequency and mobile station height on the path loss.
        #   math.pow((1.1*math.log10(f)-0.7)*h_m, 2) + 1.56*math.pow(math.log10(f), 2): This part calculates the sum of two terms. 
        # #           The first term is the square of the previously calculated term. The second term is the square of the logarithm 
        # #           (base 10) of the frequency, multiplied by a constant value of 1.56. This sum represents the combined effect of the 
        # #           frequency and mobile station height on the path loss.
        #   10.0 * math.log10(...) and - 10.0*math.log10(math.pow(h_m,2)): These parts involve taking the logarithm (base 10) of certain terms and multiplying them by 10.0. They adjust the values to the decibel (dB) scale.
        #   - 3.0: This part subtracts a constant value of 3.0 from the previous calculations.
        L_50 = 10.0 * math.log10(math.pow((1.1*math.log10(f)-0.7)*h_m,2) + 1.56*math.pow(math.log10(f),2)) - 10.0*math.log10(math.pow(h_m,2)) - 3.0
    
    # Calculate the path loss due to buildings and other obstacles
    if distance <= 0.1:
        L_90 = 3.2 * math.pow(math.log10(11.75*h_m), 2) - 4.97
    else:
        L_90 = 10.0 * math.log10(math.pow((1.1*math.log10(f)-0.7)*h_m,2) + 1.56*math.pow(math.log10(f),2)) + 2.5*math.log10(math.pow(h_m/200.0,2)) - 10.0*math.log10(math.pow(h_m,2)) - 0.5
    
    # Calculate the total path loss
    L = L_fs + L_50 + L_90
    
    # Calculate the received power in dBm
    signal_strength = 10.0 * math.log10(power) + tx_gain - L - rx_gain - 107.0
    
    return round(signal_strength,2)


def writeResult(fid, layer,signal_strength,cparams):

    test_fields = arcpy.ListFields(layer)
    test_fields = [f.name for f in arcpy.ListFields(layer)]
    
    expression = f'OBJECTID = {fid}'

    if 'signal_db' in test_fields:

        fields = ['signal_db','signal_db_params']
        
        with arcpy.da.UpdateCursor(layer, fields,expression) as cursor:
            for row in cursor:
                cursor.updateRow([signal_strength] + [cparams])
                
    elif 'Text' in test_fields:

        fields = ['DoubleValue', 'Text']
        
        with arcpy.da.UpdateCursor(layer, fields, expression) as cursor:
            for row in cursor:
                cursor.updateRow([signal_strength]+ [cparams])
                
def setLOS():
    pass
#   arcpy.defense.LinearLineOfSight(input_points, input_points, elevation, linesofsight, sightlines, observers, targets, None, 10, 10, "ADD_PROFILE_GRAPH")
#   https://pro.arcgis.com/en/pro-app/latest/tool-reference/defense/linear-line-of-sight.htm