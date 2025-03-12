'''Task 2 – Tracking
Adapt the tracking loop (DLL) to generate correlation plots and analyze the tracking performance.
Discuss the impact of urban interference on the correlation peaks. (Multiple correlators must be implemented for plotting the correlation function.)'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate

# ==========================
# 1️⃣ 读取 GNSS 数据（Open-Sky.bin）
# ==========================
file_path = '/media/user/Server2Disk1/Tengda LOU/Python Projects/AAE6102-Assignment1-24053636r/Opensky.bin'
raw_data = np.fromfile(file_path, dtype=np.int8)  # 读取 8-bit I/Q 数据

# 假设 I 在偶数索引，Q 在奇数索引
I_samples = raw_data[0::2]  # I 分量
Q_samples = raw_data[1::2]  # Q 分量
if_data = I_samples + 1j * Q_samples  # 复数信号

# ==========================
# 2️⃣ 设置 GNSS 相关参数
# ==========================
fs = 58e6  # 采样率 (Hz)
f_IF = 4.58e6  # 中频 (Hz)
ca_rate = 1.023e6  # C/A 码速率 (Hz)
prn = 7  # 选择一个 PRN 号进行分析

# ==========================
# 3️⃣ 生成 PRN 码 & 插值到 58MHz
# ==========================
def generate_ca_code(prn):
    """ 生成 GPS PRN 码（简化版，建议使用标准 PRN 码表） """
    np.random.seed(prn)
    return np.where(np.random.rand(1023) > 0.5, 1, -1)

def upsample_ca_code(ca_code, target_fs=fs, ca_rate=ca_rate):
    """ 将 C/A 码插值到目标采样率 """
    factor = int(target_fs / ca_rate)  # 计算插值因子
    return np.repeat(ca_code, factor)

ca_code = generate_ca_code(prn)
ca_code_upsampled = upsample_ca_code(ca_code)

# ==========================
# 4️⃣ DLL 码跟踪环
# ==========================
def dll_tracking(if_data, ca_code, fs, spacing=0.5):
    """
    DLL 码跟踪环，使用 Early-Prompt-Late 计算相关性。
    spacing: Early / Late 的间隔（0.5 代表 ±0.5 chip）
    """

    num_samples = len(if_data)

    # 生成 Early, Prompt, Late 码
    ca_early = np.roll(ca_code, int(-spacing * fs / ca_rate))
    ca_late = np.roll(ca_code, int(spacing * fs / ca_rate))

    # 计算相关性
    prompt_corr = np.abs(correlate(if_data, ca_code, mode='valid'))
    early_corr = np.abs(correlate(if_data, ca_early, mode='valid'))
    late_corr = np.abs(correlate(if_data, ca_late, mode='valid'))

    return early_corr, prompt_corr, late_corr

# 运行 DLL 码跟踪
early_corr, prompt_corr, late_corr = dll_tracking(if_data, ca_code_upsampled, fs)

# ==========================
# 5️⃣ 绘制相关性曲线
# ==========================
plt.figure(figsize=(10, 5))
plt.plot(prompt_corr, label="Prompt (Correctly Aligned)")
plt.plot(early_corr, label="Early (-0.5 chip)")
plt.plot(late_corr, label="Late (+0.5 chip)")
plt.xlabel("Code Phase Offset")
plt.ylabel("Correlation Strength")
plt.title(f"PRN {prn} Code Tracking Correlation Curve")
plt.legend()
plt.show()
