import numpy as np
from scipy.signal import correlate
from scipy.fftpack import fft, fftfreq

# 模拟早-晚捕获跟踪的核心函数
def code_tracking(iq_data, ca_code, fs, doppler_shift, code_phase, early_late_spacing=2, max_shift=20):
    """
    Perform early-late code tracking.

    Parameters:
    - iq_data: I/Q data samples
    - ca_code: C/A code
    - fs: Sampling frequency (Hz)
    - doppler_shift: Estimated doppler shift
    - code_phase: Initial code phase
    - early_late_spacing: Early-late spacing (samples)
    - max_shift: Maximum code phase search range (samples)

    Returns:
    - Best code phase after tracking
    """
    iq_data = np.nan_to_num(iq_data)
    ca_code = np.nan_to_num(ca_code)

    # Generate early and late code signals based on the given code phase
    early_code = np.roll(ca_code, -early_late_spacing)
    late_code = np.roll(ca_code, early_late_spacing)

    # Mix IQ data with Doppler shift
    freq_shift = np.exp(1j * 2 * np.pi * doppler_shift * np.arange(len(iq_data)) / fs)
    iq_shifted = iq_data * freq_shift

    # Find correlation with early and late code
    early_corr = correlate(iq_shifted, early_code, mode='same')
    late_corr = correlate(iq_shifted, late_code, mode='same')

    # Compute error in code phase and apply early-late tracking
    early_peak = np.argmax(np.abs(early_corr))
    late_peak = np.argmax(np.abs(late_corr))

    code_phase_error = early_peak - late_peak  # Difference between early and late code phase
    new_code_phase = code_phase + code_phase_error

    # Adjust code phase to stay within bounds
    if new_code_phase < 0:
        new_code_phase += len(ca_code)
    elif new_code_phase >= len(ca_code):
        new_code_phase -= len(ca_code)

    return new_code_phase


# 模拟载波同步函数
def carrier_tracking(iq_data, fs, doppler_shift, max_iterations=100):
    """
    Perform carrier synchronization using a Phase Lock Loop (PLL).

    Parameters:
    - iq_data: I/Q data samples
    - fs: Sampling frequency (Hz)
    - doppler_shift: Initial estimated doppler shift
    - max_iterations: Maximum number of PLL iterations

    Returns:
    - Synchronized IQ data after PLL
    """
    phase = 0  # Initial phase
    frequency_offset = doppler_shift  # Initial frequency offset

    for _ in range(max_iterations):
        # Mix IQ data with current estimated doppler shift
        freq_shift = np.exp(1j * 2 * np.pi * frequency_offset * np.arange(len(iq_data)) / fs)
        iq_shifted = iq_data * freq_shift

        # Estimate phase error by correlating the data with a reference signal
        pll_error = np.angle(np.mean(iq_shifted))  # Phase error estimation
        frequency_offset -= pll_error / (2 * np.pi)

    return iq_shifted


# 解码导航消息
def decode_navigation_message(iq_data, fs, ca_code, doppler_shift, code_phase):
    """
    Decode navigation message from GPS signal.

    Parameters:
    - iq_data: I/Q data samples
    - fs: Sampling frequency (Hz)
    - ca_code: C/A code
    - doppler_shift: Estimated doppler shift
    - code_phase: Initial code phase

    Returns:
    - Decoded navigation message
    """
    # Perform code tracking
    final_code_phase = code_tracking(iq_data, ca_code, fs, doppler_shift, code_phase)

    # Perform carrier tracking
    iq_synced = carrier_tracking(iq_data, fs, doppler_shift)

    # Extract the navigation message bits (this is a simplified version)
    nav_message = iq_synced[int(final_code_phase):int(final_code_phase + 1023)]  # Just an example
    return nav_message


def generate_ca_code(prn):
    """
    Generate the GPS C/A code for a given PRN number (1-32).

    Parameters:
    - prn: PRN number (1 to 32).

    Returns:
    - ca_code: The C/A code for the given PRN.
    """
    # GPS C/A code generator for PRN from 1 to 32 (based on 1023-bit length)

    # Define the lengths of the C/A code sequence and the initial states of the LFSRs
    ca_code_length = 1023

    # Initializing two shift registers based on PRN
    # Each PRN has a unique initial state for the two shift registers (G1 and G2)
    g1 = [1, 0, 1, 1, 0, 1, 1, 0, 1, 1]  # example G1 for PRN 1
    g2 = [1, 0, 0, 1, 1, 1, 1, 1, 1, 0]  # example G2 for PRN 1

    # Create a generator for PRN's C/A code (simplified version)
    ca_code = []
    for _ in range(ca_code_length):
        # Generate the new bit for the C/A code sequence
        output_bit = g1[9] ^ g2[9]  # XOR operation to generate the C/A code
        ca_code.append(output_bit)

        # Update shift registers
        feedback_g1 = g1[2] ^ g1[9]  # G1 feedback
        feedback_g2 = g2[1] ^ g2[2]  # G2 feedback

        # Shift G1 and G2 registers
        g1 = [feedback_g1] + g1[:-1]
        g2 = [feedback_g2] + g2[:-1]

    return np.array(ca_code)

# Read the I/Q data from the file
def load_iq_data(file_path):
    with open(file_path, 'rb') as f:
        iq_data = np.fromfile(f, dtype=np.complex64)
    return iq_data

opensky_path = '/media/user/Server2Disk1/Tengda LOU/Python Projects/AAE6102-Assignment1-24053636r/Opensky.bin'
fs_open_sky = 58e6

# Load the Open-Sky data
iq_open_sky = load_iq_data(opensky_path)

# Example usage (assuming we already have the I/Q data and PRN results)
prn = 1  # Example PRN
ca_code = generate_ca_code(prn)  # Generate C/A code for PRN
doppler_shift = -4286.22  # Example doppler shift from acquisition
code_phase = 22799938  # Example initial code phase

# Decode navigation message for PRN 1
nav_msg = decode_navigation_message(iq_open_sky, fs_open_sky, ca_code, doppler_shift, code_phase)

# Show the decoded navigation message
print(f"Decoded Navigation Message for PRN {prn}: {nav_msg}")


