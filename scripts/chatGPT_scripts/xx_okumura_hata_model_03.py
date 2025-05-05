from math import log10, log
import math

def okumura_hata(freq_mhz, power_watts, tx_gain_dbi, rx_gain_dbi, tx_height_m, rx_height_m, distance_m):
    # Constants for the Okumura-Hata model
    a_hm = lambda d: (1.1 * log10(freq_mhz) - 0.7) * rx_height_m - (1.56 * log10(freq_mhz) - 0.8)
    L_b = lambda d: (69.55 + 26.16 * log10(freq_mhz) - 13.82 * log10(tx_height_m) -
                     a_hm(d) + (44.9 - 6.55 * log10(tx_height_m)) * log10(distance_m / 1000))
    L_u = lambda d: (42.57 + 13.7 * log10(freq_mhz) - 13.82 * log10(tx_height_m) -
                     a_hm(d) + (0.8 + (1.54 * log10(freq_mhz))) * log10(distance_m / 1000))
    # Calculate signal loss in dB
    loss = 32.44 + 20 * log10(freq_mhz) + 20 * log10(distance_m / 1000) + L_b(distance_m) - tx_gain_dbi - rx_gain_dbi - L_u(distance_m)
    # Calculate received power in dBm
    received_power_dbm = 10 * log10(power_watts) + tx_gain_dbi - loss
    return received_power_dbm

# Example usage
freq_mhz = 800.0
power_watts = 5.0
tx_gain_dbi = 0.0
rx_gain_dbi = 0.0
tx_height_m = 10.0
rx_height_m = 10.0
lat1 = 35.1173620            #  79.1306856°W 35.1173620°N
lon1 = -79.1306856
lat2 = 35.1505534               # 79.0876685°W 35.1505534°N
lon2 = -79.0876685
distance = math.sqrt((lat2-lat1)**2 + (lon2-lon1)**2) * 111.139 # Convert from degrees to kilometers
distance_m = 5378
    
if distance <= 8:
    # frequency = 300 # MHz
    # power = 3 # watts
    rf_loss_dbm = okumura_hata(freq_mhz, power_watts, tx_gain_dbi, rx_gain_dbi, tx_height_m, rx_height_m, distance_m)
    print(f"RF signal loss in dBm: {rf_loss_dbm:.2f} (at distance {distance_m})")
