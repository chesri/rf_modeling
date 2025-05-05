import math

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
    
    # Calculate median effective height of the terrain h_b
    h_b = 73.0 * math.log10(distance) - 3.0 * math.log10(tx_height) + 2.0
    
    # Calculate the path loss due to free space propagation
    L_fs = 32.44 + 20.0 * math.log10(distance) + 20.0 * math.log10(f)
    
    # Calculate the path loss due to terrain irregularities
    if distance <= 0.1:
        L_50 = 8.29 * math.pow(math.log10(1.54*h_m), 2) - 1.1
    else:
        L_50 = 10.0 * math.log10(math.pow((1.1*math.log10(f)-0.7)*h_m,2) + 1.56*math.pow(math.log10(f),2)) - 10.0*math.log10(math.pow(h_m,2)) - 3.0
    
    # Calculate the path loss due to buildings and other obstacles
    if distance <= 0.1:
        L_90 = 3.2 * math.pow(math.log10(11.75*h_m), 2) - 4.97
    else:
        L_90 = 10.0 * math.log10(math.pow((1.1*math.log10(f)-0.7)*h_m,2) + 1.56*math.pow(math.log10(f),2)) + 2.5*math.log10(math.pow(h_m/200.0,2)) - 10.0*math.log10(math.pow(h_m,2)) - 0.5
    
    # Calculate the total path loss
    L = L_fs + L_50 + L_90
    
    # Calculate the received power in dBm
    p_rx = 10.0 * math.log10(power) + tx_gain - L - rx_gain - 107.0
    
    return p_rx

# Example usage
freq = 800.0 # MHz
power = 5.0 # watts
tx_gain = 0.0 # dBi
rx_gain = 0.0 # dBi
tx_height = 10.0 # meters
rx_height = 10.0 # meters
distance = 5.379 # kilometers

loss = okumura_hata(freq, power, tx_gain, rx_gain, tx_height, rx_height, distance)
print("Signal strength loss:", round(loss,3), "dBm")

