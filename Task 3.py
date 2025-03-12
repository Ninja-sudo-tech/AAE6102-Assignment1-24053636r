'''Task 3 – Navigation data decoding
Decode the navigation message and extract key parameters, such as ephemeris data, for at least one satellite.
'''

import numpy as np

# ==========================
# 1️⃣ 读取已跟踪的 PRN 号的导航数据
# ==========================
file_path = '/media/user/Server2Disk1/Tengda LOU/Python Projects/AAE6102-Assignment1-24053636r/Opensky.bin'
raw_data = np.fromfile(file_path, dtype=np.int8)
fs=58e6

# 这里假设 raw_data 是 Prompt 相关结果
I_samples = raw_data[0::2]  # I 分量
Q_samples = raw_data[1::2]  # Q 分量
if_data = I_samples + 1j * Q_samples  # 复数信号

# ==========================
# 2️⃣ 导航数据解码
# ==========================
def extract_navigation_bits(if_data, fs, bit_rate=50):
    """
    从 IF 数据中提取 50 bps 导航数据
    """
    samples_per_bit = int(fs / bit_rate)  # 每比特采样点数
    bits = []

    for i in range(0, len(if_data), samples_per_bit):
        bit_value = np.sign(np.sum(if_data[i:i+samples_per_bit]))  # 通过符号决定是 0 还是 1
        bits.append(1 if bit_value > 0 else 0)

    return np.array(bits)

# 50 bps 导航比特流
nav_bits = extract_navigation_bits(if_data, fs)

# ==========================
# 3️⃣ 找到导航电文起始（TLM 字头同步）
# ==========================
def find_tlm_header(nav_bits):
    """
    在 50bps 数据流中寻找 GPS TLM 头（8B in hex -> 10001011 in binary）
    """
    tlm_pattern = np.array([1, 0, 0, 0, 1, 0, 1, 1])  # GPS TLM 头
    for i in range(len(nav_bits) - len(tlm_pattern)):
        if np.array_equal(nav_bits[i:i+len(tlm_pattern)], tlm_pattern):
            return i
    return -1

start_idx = find_tlm_header(nav_bits)
if start_idx == -1:
    print("❌ 未找到 TLM 头，数据可能损坏！")
else:
    print(f"✅ 找到 TLM 头，起始索引: {start_idx}")

# ==========================
# 4️⃣ 解析星历数据（子帧 2 & 3）
# ==========================
def parse_ephemeris(nav_bits, start_idx):
    """
    解析 GPS 星历数据（子帧 2 和 3）
    """
    subframe_2_start = start_idx + 300  # 子帧 2 起始
    subframe_3_start = start_idx + 600  # 子帧 3 起始

    ephemeris_data = {
        "Week Number": int("".join(map(str, nav_bits[subframe_2_start+30:subframe_2_start+40])), 2),
        "SV Accuracy": int("".join(map(str, nav_bits[subframe_2_start+40:subframe_2_start+44])), 2),
        "SV Health": int("".join(map(str, nav_bits[subframe_2_start+44:subframe_2_start+50])), 2),
        "Eccentricity": int("".join(map(str, nav_bits[subframe_2_start+60:subframe_2_start+76])), 2) * 2**-33,
        "Inclination Angle": int("".join(map(str, nav_bits[subframe_3_start+60:subframe_3_start+76])), 2) * 2**-31,
        "Semi-Major Axis": int("".join(map(str, nav_bits[subframe_3_start+76:subframe_3_start+96])), 2) * 2**-19
    }
    return ephemeris_data

if start_idx != -1:
    ephemeris = parse_ephemeris(nav_bits, start_idx)
    print("✅ 解析到星历数据:")
    for key, value in ephemeris.items():
        print(f"{key}: {value}")
