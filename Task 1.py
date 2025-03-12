
'''Task 1 – Acquisition
Process the IF data using a GNSS SDR and generate the initial acquisition results.'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate

# ==========================
# 1️⃣ 设置 GNSS 相关参数
# ==========================
f_L1 = 1575.42e6  # GPS L1 载波频率 (Hz)
f_IF = 4.58e6  # 中频 (Hz)
fs = 58e6  # 采样率 (Hz)
num_samples = int(fs * 0.001)  # 取 1ms 数据

# ==========================
# 2️⃣ 读取 Open-Sky 数据
# ==========================

# file_path = '/media/user/Server2Disk1/Tengda LOU/Python Projects/AAE6102-Assignment1-24053636r/Opensky.bin'  # 文件名
file_path = '/media/user/Server2Disk1/Tengda LOU/Python Projects/AAE6102-Assignment1-24053636r/Urban.dat'

raw_data = np.fromfile(file_path, dtype=np.int8)  # 读取 8-bit I/Q 数据

# 提取 I/Q 分量（假设 I 在偶数索引，Q 在奇数索引）
I_samples = raw_data[0::2][:num_samples]  # 取前 num_samples 个点
Q_samples = raw_data[1::2][:num_samples]
if_data = I_samples + 1j * Q_samples  # 复数信号

# ==========================
# 3️⃣ 生成 PRN 伪随机码
# ==========================
def generate_ca_code(prn):
    """ 生成 GPS C/A 码（示例代码，可替换为更完整的 PRN 码表） """
    np.random.seed(prn)
    return np.where(np.random.rand(1023) > 0.5, 1, -1)

# 码率调整（C/A 码原始速率：1.023 MHz，需要插值到 58 MHz）
def upsample_ca_code(ca_code, target_fs=fs, ca_rate=1.023e6):
    """ 将 C/A 码插值到目标采样率 """
    factor = int(target_fs / ca_rate)  # 计算插值因子
    return np.repeat(ca_code, factor)

# ==========================
# 4️⃣ 进行 Acquisition 计算
# ==========================
prn_list = range(1, 33)  # GPS PRN 号 1~32
doppler_range = np.arange(-10000, 10000, 500)  # 搜索多普勒范围（Hz）

acquisition_results = []

for prn in prn_list:
    ca_code = generate_ca_code(prn)  # 生成 PRN 码
    ca_code_upsampled = upsample_ca_code(ca_code)  # 插值到 58 MHz 采样率

    best_correlation = 0
    best_doppler = 0
    best_code_phase = 0

    for doppler in doppler_range:
        # 生成频率偏移信号
        freq_shift = np.exp(-1j * 2 * np.pi * doppler / fs * np.arange(num_samples))
        if_data_shifted = if_data * freq_shift  # 进行频率校正

        # 计算相关性
        correlation = correlate(if_data_shifted, ca_code_upsampled, mode='valid')
        peak_value = np.max(np.abs(correlation))
        peak_index = np.argmax(np.abs(correlation))

        if peak_value > best_correlation:
            best_correlation = peak_value
            best_doppler = doppler
            best_code_phase = peak_index

    if best_correlation > 0.6 * np.max(best_correlation):  # 设定门限
        acquisition_results.append((prn, best_doppler, best_code_phase))
        print(f"✅ PRN {prn}: Doppler = {best_doppler} Hz, Code Phase = {best_code_phase}")

# ==========================
# 5️⃣ 显示捕获结果
# ==========================
plt.figure(figsize=(10, 5))
plt.bar([x[0] for x in acquisition_results], [x[1] for x in acquisition_results], color='b')
plt.xlabel('PRN')
plt.ylabel('Doppler Shift (Hz)')
plt.title('GPS Acquisition Results_Urban')
plt.show()
