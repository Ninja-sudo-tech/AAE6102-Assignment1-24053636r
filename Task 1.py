import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate
from scipy.fftpack import fft, fftfreq

def read_iq_data(filename, data_format=np.int8):

    raw_data = np.fromfile(filename, dtype=data_format)
    I = raw_data[0::2]
    Q = raw_data[1::2]
    return I + 1j * Q

def generate_ca_code(prn):

    np.random.seed(prn)
    return np.random.choice([1, -1], size=1023)


def resample_ca_code(ca_code, fs, ca_chip_rate=1.023e6):

    samples_per_chip = fs / ca_chip_rate
    resampled_code = np.repeat(ca_code, np.round(samples_per_chip).astype(int))
    return resampled_code[:int(fs)]


def acquisition(iq_data, prn, fs, if_freq):

    ca_code = generate_ca_code(prn)
    ca_code_resampled = resample_ca_code(ca_code, fs)

    correlation = correlate(iq_data[:int(fs)], ca_code_resampled, mode='valid')
    code_phase = np.argmax(np.abs(correlation))

    fft_result = fft(correlation)
    freq_bins = fftfreq(len(fft_result), 1 / fs)
    doppler_shift = freq_bins[np.argmax(np.abs(fft_result))] + if_freq

    return code_phase, doppler_shift

def process_dataset(filename, fs, if_freq):
    iq_data = read_iq_data(filename)

    visible_satellites = {}
    for prn in range(1, 33):
        code_phase, doppler_shift = acquisition(iq_data, prn, fs, if_freq)
        if abs(doppler_shift) < 5000:
            visible_satellites[prn] = (code_phase, doppler_shift)

    return visible_satellites


open_sky_results = process_dataset("/media/user/Server2Disk1/Tengda LOU/Python Projects/AAE6102-Assignment1-24053636r/Opensky.bin", fs=58e6, if_freq=4.58e6)
urban_results = process_dataset("/media/user/Server2Disk1/Tengda LOU/Python Projects/AAE6102-Assignment1-24053636r/Urban.dat", fs=26e6, if_freq=0)

print("Open-Sky Environment - Visible Satellites:")
for prn, (code_phase, doppler) in open_sky_results.items():
    print(f"PRN {prn}: Code Phase = {code_phase}, Doppler Shift = {doppler:.2f} Hz")

print("\nUrban Environment - Visible Satellites:")
for prn, (code_phase, doppler) in urban_results.items():
    print(f"PRN {prn}: Code Phase = {code_phase}, Doppler Shift = {doppler:.2f} Hz")
