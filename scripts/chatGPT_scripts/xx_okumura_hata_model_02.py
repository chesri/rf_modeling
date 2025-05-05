import math

def okumura_hata(freq, tx_height, rx_height, dist_km, tx_gain, rx_gain):
    """
    Calculates signal strength loss in dBm using Okumura-Hata model.
    
    freq: UHF radio frequency in MHz
    tx_height: height of transmitter in meters
    rx_height: height of receiver in meters
    dist_km: distance between transmitter and receiver in kilometers
    """
    # Set constants based on frequency
    if freq < 200:
        C1, C2 = 69.55, 26.16
    elif freq < 400:
        C1, C2 = 46.3, 33.9
    elif freq < 1500:
        C1, C2 = 33.9, 44.9
    else:
        raise ValueError("Frequency must be less than 1500 MHz")
    
    # Calculate path loss
    L = C1 + C2 * math.log10(freq) - 13.83 * math.log10(tx_height) - \
        (1.1 * math.log10(freq) - 0.7) * rx_height - \
        ((1.56 * math.log10(freq) - 0.8) + (44.9 - 6.55 * math.log10(tx_height))) * math.log10(dist_km)
    
    # Calculate signal strength in dBm at receiver
    pt = 1  # Transmitter power in watts
    gt = 10**(tx_gain / 10)  # Transmitter antenna gain
    gr = 10**(rx_gain / 10)  # Receiver antenna gain
    pr = 10 * math.log10(pt * gt * gr / 0.001) - L
    
    return pr


freq = 800  # MHz
tx_height = 10  # meters
rx_height = 10  # meters
dist_km = 5.379  # kilometers
tx_gain = 0  # dBi
rx_gain = 0  # dBi

pr = okumura_hata(freq, tx_height, rx_height, dist_km, tx_gain, rx_gain)
print(f"Predicted signal strength loss: {pr:.2f} dBm")
