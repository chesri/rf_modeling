import math

def longley_rice(freq, power, tx_gain, rx_gain, tx_height, rx_height, distance, terrain_type, climate_conditions):
    # Constants
    k = 1.38064852e-23 # Boltzmann constant in joules per kelvin
    T0 = 290 # Reference temperature in kelvin
    c = 299792458 # Speed of light in meters per second
    pi = math.pi
    
    # Convert frequency from MHz to Hz
    freq = freq * 1e6
    
    # Calculate wavelength
    wavelength = c / freq
    
    # Convert power from watts to dBm
    power_dbm = 10 * math.log10(power * 1000)
    
    # Convert transmitter and receiver antenna gain from dBi to linear scale
    tx_gain_lin = 10 ** (tx_gain / 10)
    rx_gain_lin = 10 ** (rx_gain / 10)
    
    # Calculate effective antenna height
    heff_tx = tx_height + 0.8 * (wavelength / (2 * pi)) ** 2 / tx_height
    heff_rx = rx_height + 0.8 * (wavelength / (2 * pi)) ** 2 / rx_height
    
    # Convert distance from kilometers to meters
    distance = distance * 1000
    
    # Calculate terrain factor
    if terrain_type == "urban":
        a = 4.6
        b = 0.0075
    elif terrain_type == "suburban":
        a = 4.0
        b = 0.0065
    else:
        a = 3.6
        b = 0.005
    
    terrain_factor = a * (distance / 1000) ** b
    
    # Calculate atmospheric absorption
    if climate_conditions == "standard":
        alpha = 0.0064 * (freq / 1000000) ** 1.3
        beta = 2.1e-11 * (freq / 1000000) ** 2.4
    else:
        alpha = 0.0173 * (freq / 1000000) ** 0.5
        beta = 1.65e-9 * (freq / 1000000) ** 2
        
    attenuation = alpha * distance + beta * distance ** 2
    
    # Calculate path loss
    path_loss = 32.44 + 20 * math.log10(distance) + 20 * math.log10(freq / 1000000) + terrain_factor - attenuation
    
    # Calculate received power
    rx_power_dbm = power_dbm + tx_gain + rx_gain - path_loss
    
    # Calculate noise power density
    noise_density = 10 * math.log10(k * T0) - 174
    
    # Calculate received signal-to-noise ratio
    snr_db = rx_power_dbm - noise_density
    
    return snr_db

freq = 800 # UHF frequency in MHz
power = 5 # Power in watts
tx_gain = 0 # Transmitter antenna gain in dBi
rx_gain = 0 # Receiver antenna gain in dBi
tx_height = 10 # Height of transmitter in meters
rx_height = 10 # Height of receiver in meters
distance = 5.379 # Distance in kilometers
terrain_type = "urban" # Terrain type ("urban",
climate_conditions = "standard"

print(longley_rice(freq, power, tx_gain, rx_gain, tx_height, rx_height, distance, terrain_type, climate_conditions))