import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate
from scipy.fftpack import fft, fftfreq

# ==== 1. 读取 I/Q 采样数据 ====
def read_iq_data(filename, data_format=np.int8):
    """读取二进制 I/Q 采样数据"""
    raw_data = np.fromfile(filename, dtype=data_format)
    I = raw_data[0::2]  # 奇数索引为 I 分量
    Q = raw_data[1::2]  # 偶数索引为 Q 分量
    return I + 1j * Q  # 复数形式的 I/Q 信号


# ==== 2. 生成伪随机码 C/A 码 ====
def generate_ca_code(prn):
    """生成 GPS C/A 码 (简化版)"""
    np.random.seed(prn)  # PRN 码种子（这里只是占位，实际 GPS C/A 码需用 LFSR 生成）
    return np.random.choice([1, -1], size=1023)


def resample_ca_code(ca_code, fs, ca_chip_rate=1.023e6):
    """重采样 C/A 码以匹配采样频率"""
    samples_per_chip = fs / ca_chip_rate
    resampled_code = np.repeat(ca_code, np.round(samples_per_chip).astype(int))
    return resampled_code[:int(fs)]  # 取 1ms 长度的 C/A 码

# ==== 3. Acquisition (捕获) ====
def acquisition(iq_data, prn, fs, if_freq):
    """捕获 GPS 信号，估算载波多普勒频率 & 码相位"""
    ca_code = generate_ca_code(prn)
    ca_code_resampled = resample_ca_code(ca_code, fs)

    # 计算相关性（找到最佳码相位）
    correlation = correlate(iq_data[:int(fs)], ca_code_resampled, mode='valid')
    code_phase = np.argmax(np.abs(correlation))

    # 计算频谱（找到多普勒频移）
    fft_result = fft(correlation)
    freq_bins = fftfreq(len(fft_result), 1 / fs)
    doppler_shift = freq_bins[np.argmax(np.abs(fft_result))] + if_freq

    return code_phase, doppler_shift

# ==== 4. 处理数据集 ====
def process_dataset(filename, fs, if_freq):
    iq_data = read_iq_data(filename)

    visible_satellites = {}
    for prn in range(1, 33):  # GPS PRN 1-32
        code_phase, doppler_shift = acquisition(iq_data, prn, fs, if_freq)
        if abs(doppler_shift) < 5000:  # 设定阈值，通常 GPS 信号的多普勒范围在 ±5kHz
            visible_satellites[prn] = (code_phase, doppler_shift)

    return visible_satellites

# ==== 5. 运行 Acquisition ====
open_sky_results = process_dataset("/media/user/Server2Disk1/Tengda LOU/Python Projects/AAE6102-Assignment1-24053636r/Opensky.bin", fs=58e6, if_freq=4.58e6)
urban_results = process_dataset("/media/user/Server2Disk1/Tengda LOU/Python Projects/AAE6102-Assignment1-24053636r/Urban.dat", fs=26e6, if_freq=0)

# ==== 6. 打印结果 ====
print("Open-Sky Environment - Visible Satellites:")
for prn, (code_phase, doppler) in open_sky_results.items():
    print(f"PRN {prn}: Code Phase = {code_phase}, Doppler Shift = {doppler:.2f} Hz")

print("\nUrban Environment - Visible Satellites:")
for prn, (code_phase, doppler) in urban_results.items():
    print(f"PRN {prn}: Code Phase = {code_phase}, Doppler Shift = {doppler:.2f} Hz")