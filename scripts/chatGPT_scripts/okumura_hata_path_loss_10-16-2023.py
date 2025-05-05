import math

def okumura_hata_path_loss(frequency_MHz, power_W, tx_gain_dBi, rx_gain_dBi, tx_height_m, rx_height_m, distance_km, terrain_type):
    # Constants for Okumura-Hata model
    if terrain_type == "urban":
        A = 69.55
        B = 26.16
    elif terrain_type == "suburban":
        A = 69.55
        B = 20.0
    elif terrain_type == "rural":
        A = 69.55
        B = 11.0
    else:
        raise ValueError("Invalid terrain type. Choose from 'urban', 'suburban', or 'rural'.")

    # Calculate path loss
    L = A + B * math.log10(frequency_MHz) - 13.83 * math.log10(tx_height_m) - (44.9 - 6.55 * math.log10(tx_height_m)) * math.log10(distance_km)
    
    # Adjust for antenna gains
    L -= (tx_gain_dBi + rx_gain_dBi)
    
    # Calculate received power in dBm
    received_power_dBm = 10 * math.log10(power_W * 1000) - L

    return received_power_dBm

# Input parameters
frequency_MHz = 900  # UHF frequency in MHz
power_W = 1.0       # Transmitter power in watts
tx_gain_dBi = 3.0   # Transmitter antenna gain in dBi
rx_gain_dBi = 5.0   # Receiver antenna gain in dBi
tx_height_m = 30.0  # Height of transmitter in meters
rx_height_m = 3.0   # Height of receiver in meters
distance_km = 2.0   # Distance between transmitter and receiver in kilometers
terrain_type = "rural"  # Terrain type (urban, suburban, rural)

# Calculate signal strength loss
signal_strength_loss_dBm = okumura_hata_path_loss(frequency_MHz, power_W, tx_gain_dBi, rx_gain_dBi, tx_height_m, rx_height_m, distance_km, terrain_type)

# Print the result
print(f"Signal Strength Loss: {signal_strength_loss_dBm:.2f} dBm")
