import math

def longley_rice(freq_mhz, power_watts, tx_ant_gain, rx_ant_gain, tx_ant_height, rx_ant_height, distance_km, terrain_type, climate_condition):
    # Convert input values to appropriate units
    freq = freq_mhz * 1e6
    power = 10 * math.log10(power_watts * 1000)
    tx_gain = tx_ant_gain
    rx_gain = rx_ant_gain
    tx_height = tx_ant_height
    rx_height = rx_ant_height
    distance = distance_km * 1000

    # Calculate effective Earth radius
    if terrain_type == 'rural':
        Re = 8500
    elif terrain_type == 'suburban':
        Re = 8200
    else:
        Re = 7600

    # Calculate delta h and theta_e
    delta_h = rx_height - tx_height
    theta_e = math.atan(delta_h / distance)

    # Calculate the radio horizon
    d1 = 2 * math.sqrt(tx_height) * math.sqrt(Re)
    d2 = 2 * math.sqrt(rx_height) * math.sqrt(Re)
    d = d1 + d2
    radio_horizon = math.sqrt(d * distance)

    # Calculate the path distance factor
    if distance > radio_horizon:
        d0 = 1.607 * radio_horizon * math.log10(distance / radio_horizon) + 0.477 * (distance / radio_horizon) - 1.82
    else:
        d0 = 0

    # Calculate the terrain factor
    if terrain_type == 'rural':
        terrain_factor = -0.1 * (tx_height - 200) + 8.56 * (math.log10(distance))**2 - 1.3
    elif terrain_type == 'suburban':
        terrain_factor = -0.15 * (tx_height - 200) + 7.81 * math.log10(distance) - 1.1
    else:
        terrain_factor = -0.17 * (tx_height - 200) + 7.44 * math.log10(distance) - 1.5

    # Calculate the atmospheric absorption factor
    if climate_condition == 'standard':
        atmospheric_factor = (math.pow(freq/1000, 2) * (1.607*math.log10(freq/1000) - 0.8))
    else:
        atmospheric_factor = 0

    # Calculate the total path loss
    path_loss = 32.44 + 20*math.log10(freq/1000000) + 20*math.log10(distance/1000) + terrain_factor - tx_gain - rx_gain + atmospheric_factor + d0

    # Calculate the signal strength at the receiver
    rx_signal_strength = power - path_loss

    return rx_signal_strength

# Example usage
signal_loss = longley_rice(freq_mhz=800, power_watts=5, tx_ant_gain=0, rx_ant_gain=1, tx_ant_height=10, rx_ant_height=10, distance_km=5.379, terrain_type='rural', climate_condition='standard')
print(f'Signal loss: {signal_loss:.2f} dBm')
