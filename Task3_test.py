import numpy as np
import matplotlib.pyplot as plt


def load_iq_data(filename, max_samples=None):
    """ Load 8-bit I/Q data with an optional limit on sample count """
    data = np.fromfile(filename, dtype=np.int8)

    if max_samples is not None:
        data = data[: max_samples * 2]  # Ensure I/Q pairing

    iq_data = data[::2] + 1j * data[1::2]  # Combine I and Q data
    return iq_data


def plot_gps_l1_spectrum(iq_data, fs, title, center_freq=1575.42e6, span=4e6, nfft=2 ** 20):
    """
    Plot GPS L1 power spectrum (around 1575.42 MHz)

    Parameters:
    - iq_data: Complex I/Q samples
    - fs: Sampling frequency (Hz)
    - title: Plot title
    - center_freq: Center frequency of interest (default 1575.42 MHz)
    - span: Frequency span around center (default ±2 MHz)
    - nfft: FFT size for resolution
    """
    num_samples = len(iq_data)
    if num_samples > nfft:
        iq_data = iq_data[:nfft]  # Limit samples to avoid memory issues

    fft_data = np.fft.fftshift(np.fft.fft(iq_data, n=nfft))
    freqs = np.fft.fftshift(np.fft.fftfreq(nfft, 1 / fs)) + center_freq  # Adjust frequency axis

    # Only keep the range of interest
    mask = (freqs >= center_freq - span / 2) & (freqs <= center_freq + span / 2)

    plt.figure(figsize=(10, 5))
    plt.plot(freqs[mask], 20 * np.log10(np.abs(fft_data[mask])))
    plt.title(f"GPS L1 Power Spectrum: {title}")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power (dB)")
    plt.grid()
    plt.show()


# Dataset paths
opensky_path = '/media/user/Server2Disk1/Tengda LOU/Python Projects/AAE6102-Assignment1-24053636r/Opensky.bin'
urban_path = '/media/user/Server2Disk1/Tengda LOU/Python Projects/AAE6102-Assignment1-24053636r/Urban.dat'

# Sampling rates
fs_open_sky = 58e6  # 58 MHz
fs_urban = 26e6  # 26 MHz

# Load data (limit to 10M samples to save memory)
iq_open_sky = load_iq_data(opensky_path, max_samples=10_000_000)
iq_urban = load_iq_data(urban_path, max_samples=10_000_000)

# Plot GPS L1 spectrum
plot_gps_l1_spectrum(iq_open_sky, fs_open_sky, "Open-Sky")
plot_gps_l1_spectrum(iq_urban, fs_urban, "Urban")
