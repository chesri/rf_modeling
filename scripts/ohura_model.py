import math

# input parameters
frequency = 800e6  # UHF frequency in Hz
power = 1  # transmitter power in watts
tx_ant_gain = 0  # transmitter antenna gain in dBi
rx_ant_gain = 0  # receiver antenna gain in dBi
distance = 5.379  # distance in km
terrain_height = 50  # average terrain height in meters
building_height = 20  # average building height in meters

# constants
h_e = 1.5  # effective height of the transmitter antenna in meters
h_r = 1.5  # effective height of the receiver antenna in meters
h_m = (terrain_height + building_height) / 2  # average height of the irregular terrain in meters

# free space loss
lambda_ = 3e8 / frequency  # wavelength in meters
fsl = (4 * math.pi * distance * 1000 / lambda_) ** 2

# diffraction loss
d = distance * 1000  # distance in meters
d_1 = 1.5 * (h_e + h_r) * math.sqrt(h_m / 1000)  # first Fresnel zone distance in meters
d_2 = d - d_1  # second Fresnel zone distance in meters
f_1 = (1.0 + (20 * math.log10(math.sqrt(d_1 * h_e)) / 1000) + (20 * math.log10(math.sqrt(d_1 * h_r)) / 1000))  # first Fresnel zone attenuation in dB
f_2 = (1.0 + (20 * math.log10(math.sqrt(d_2 * h_e)) / 1000) + (20 * math.log10(math.sqrt(d_2 * h_r)) / 1000))  # second Fresnel zone attenuation in dB
dl = 10 * math.log10((d_1 * d_2) / d ** 2) + f_1 + f_2

# attenuation due to reflection
A = 20  # ground reflection attenuation in dB
d_l = 0.1 * math.sqrt(h_e * h_r) * ((d_1 / 1000) ** 2) / lambda_  # distance to first reflection point in km
if d_l <= 3:
    R = (-10 * math.log10(d_l)) ** 2 / 10  # reflection attenuation in dB
else:
    R = (-20 * math.log10(d_l) - 7.7) * math.log10(h_e / 2) - (10 * math.log10(d_l)) * (math.log10(h_r / 2) - 1.5) + 83  # reflection attenuation in dB
ar = A + R

# total path loss
path_loss = fsl + dl + ar

# received power
rx_power = power + tx_ant_gain + rx_ant_gain - path_loss

# print the results
print("UHF frequency: {} Hz".format(frequency))
print("Transmitter power: {} watts".format(power))
print("Transmitter antenna gain: {} dBi".format(tx_ant_gain))
print("Receiver antenna gain: {} dBi".format(rx_ant_gain))
print("Distance: {} km".format(distance))
print("Recv Power: {}".format(rx_power))
