import math

def calculate_signal_strength_loss(frequency, power, tx_gain, rx_gain, distance):
    # Convert frequency from MHz to Hz
    frequency_hz = frequency * 1000000
    
    # Calculate free space path loss
    free_space_path_loss = 20 * math.log10(distance) + 20 * math.log10(frequency_hz) - 27.55
    
    # Calculate effective isotropic radiated power (EIRP)
    eirp = 10 ** ((tx_gain + 10 * math.log10(power)) / 10)
    
    # Calculate received power
    received_power = eirp - free_space_path_loss + rx_gain
    
    # Convert received power to dBm
    received_power_dbm = 10 * math.log10(abs(received_power) * 1000)
    if received_power < 0:
        received_power_dbm = -1.0 * received_power_dbm
    
    return received_power_dbm

# Example inputs
frequency = 800.0 # MHz
power = 5.0 # watts
tx_gain = 0.0 # dBi
rx_gain = 0.0 # dBi
distance = 5378.0 # meters

# Calculate signal strength loss
signal_strength_loss = calculate_signal_strength_loss(frequency, power, tx_gain, rx_gain, distance)

# Print the result
print("Signal strength loss: {:.2f} dBm".format(signal_strength_loss))