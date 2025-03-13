import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate

# 定义一个简化的 C/A 码生成函数（用于 GNSS L1 C/A 码）
def generate_ca_code():
    # 生成 C/A 码（长度为 1023 bit）
    ca_code = np.zeros(1023, dtype=int)
    ca_code[0] = 1
    for i in range(1, 1023):
        ca_code[i] = ca_code[i-1]  # 这里为简化，实际应为多项式反馈
    return ca_code * 2 - 1  # 输出 +1/-1 的符号序列

# 定义一个函数进行采样、上变频、下变频等操作
def process_iq_data(file_path, fs, if_freq):
    iq_data = np.fromfile(file_path, dtype=np.complex64)  # 读取 I/Q 数据
    iq_data = iq_data[:len(iq_data) // 2]  # 假设 I/Q 数据是交替排列的
    return iq_data

# 检查并清理数据中的 NaN 或 Inf 值
def clean_data(data):
    data = np.nan_to_num(data)  # 将 NaN 和 Inf 替换为 0
    return data

# 定义 DLL（延迟锁定环）算法
def dll_tracking(iq_data, ca_code, fs, early_lag=0.5e-6, late_lag=1.5e-6):
    # 将 C/A 码进行采样（简化处理）
    code_length = len(ca_code)
    early_code = np.roll(ca_code, int(early_lag * fs))  # 早期码
    late_code = np.roll(ca_code, int(late_lag * fs))  # 晚期码

    # 清理数据中的 NaN 或 Inf
    iq_data = clean_data(iq_data)
    early_code = clean_data(early_code)
    late_code = clean_data(late_code)

    # 计算相关性
    early_corr = correlate(iq_data, early_code, mode='valid')
    prompt_corr = correlate(iq_data, ca_code, mode='valid')
    late_corr = correlate(iq_data, late_code, mode='valid')

    # 返回相关数据（用于分析）
    return early_corr, prompt_corr, late_corr

# 可视化相关图
def plot_correlation(early_corr, prompt_corr, late_corr, environment):
    plt.figure(figsize=(10, 6))
    plt.plot(np.real(early_corr), label='Early Correlation', color='blue', alpha=0.6)
    plt.plot(np.real(prompt_corr), label='Prompt Correlation', color='green', alpha=0.6)
    plt.plot(np.real(late_corr), label='Late Correlation', color='red', alpha=0.6)
    plt.title(f'Correlation Function - {environment}')
    plt.xlabel('Sample Index')
    plt.ylabel('Correlation Amplitude')
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()

# 主函数 - 处理数据集
def track_and_analyze(file_path, fs, if_freq, environment):
    # 生成 C/A 码
    ca_code = generate_ca_code()

    # 处理数据
    iq_data = process_iq_data(file_path, fs, if_freq)

    # 执行 DLL 跟踪
    early_corr, prompt_corr, late_corr = dll_tracking(iq_data, ca_code, fs)

    # 可视化相关函数
    plot_correlation(early_corr, prompt_corr, late_corr, environment)

# 跟踪开阔天空数据集
track_and_analyze("/media/user/Server2Disk1/Tengda LOU/Python Projects/AAE6102-Assignment1-24053636r/Opensky.bin", fs=58e6, if_freq=4.58e6, environment='Open-Sky')

# 跟踪城市环境数据集
track_and_analyze("/media/user/Server2Disk1/Tengda LOU/Python Projects/AAE6102-Assignment1-24053636r/Urban.dat", fs=26e6, if_freq=0, environment='Urban')
