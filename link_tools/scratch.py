import math
import time

# Start time
start_time = time.time()

for l in range(10):

    # End time
    end_time = time.time()
 
    # Calculate elapsed time
    elapsed_time = end_time - start_time

    # Print elapsed time
    print(f"Elapsed time: {round(elapsed_time,3)} seconds")
    time.sleep(4)





# latitude = 35  # North latitude

# resolution = 111320 * math.cos(math.radians(latitude)) / 3600
# print("1/3 Arc Second resolution at latitude 35: ", resolution, " meters")


# def okumura_hata_model(freq, power, tx_gain, rx_gain, tx_height, rx_height, distance, terrain_irregularity, obstacle_loss):
#     # Convert frequency from MHz to MHz
#     freq = freq * 1e6
    
#     # Calculate height factor (h_f)
#     h_f = (1.1 * math.log10(freq) - 0.7) * rx_height - (1.56 * math.log10(freq) - 0.8)
    
#     # Calculate median path loss (L_50) in dB
#     L_50 = 69.55 + 26.16 * math.log10(freq) - 13.82 * math.log10(tx_height) - h_f + (44.9 - 6.55 * math.log10(tx_height)) * math.log10(distance)
    
#     # Calculate path loss due to terrain irregularities (L_ti) in dB
#     L_ti = 0
#     if terrain_irregularity:
#         L_ti = 3.2 * math.pow(math.log10(11.75 * rx_height), 2) - 4.97
    
#     # Calculate path loss due to obstacles (L_o) in dB
#     L_o = 0
#     if obstacle_loss:
#         L_o = obstacle_loss
    
#     # Calculate total path loss (L) in dB
#     L = L_50 + L_ti + L_o
    
#     # Calculate received power (P_rx) in dBm
#     P_rx = power + tx_gain + rx_gain - L
    
#     return P_rx


# # Example usage
# freq = 147.23  # UHF frequency in MHz
# power = 5  # Transmitter power in watts
# tx_gain = 0  # Transmitter antenna gain in dBi
# rx_gain = 1  # Receiver antenna gain in dBi
# tx_height = 10  # Height of transmitter in meters
# rx_height = 10  # Height of receiver in meters
# distance = 5.379  # Distance between transmitter and receiver in kilometers
# terrain_irregularity = True  # Set to True to include path loss due to terrain irregularities
# obstacle_loss = 3  # Path loss due to obstacles in dB

# # Calculate signal loss
# signal_loss = okumura_hata_model(freq, power, tx_gain, rx_gain, tx_height, rx_height, distance, terrain_irregularity, obstacle_loss)
# print("Signal Loss (dBm):", signal_loss)
