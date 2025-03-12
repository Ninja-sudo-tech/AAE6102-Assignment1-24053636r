'''Task 4 – Position and velocity estimation
Using the pseudorange measurements obtained from tracking, implement the Weighted Least Squares (WLS) algorithm to compute user’s position and velocity. Plot the user position and velocity, compare it to the provided ground truth values, and comment on the impact of multipath effects on the WLS solution.
'''

import numpy as np
import matplotlib.pyplot as plt

# ==========================
# 1️⃣ 读取数据：卫星星历 & 伪距
# ==========================
# 示例星历数据（假设已解码）
ephemeris = {
    'sv_positions': np.array([[15600e3, 7540e3, 20140e3],  # 假设 4 颗卫星 ECEF 坐标
                              [18760e3, 2750e3, 18610e3],
                              [17610e3, 14630e3, 13480e3],
                              [19170e3, 610e3, 18390e3]]),
    'transmission_times': np.array([0.07, 0.09, 0.10, 0.12])  # 传播时间（s）
}

# 伪距观测值（单位：米）
pseudoranges = np.array([2.407e7, 2.412e7, 2.423e7, 2.425e7])


# ==========================
# 2️⃣ WLS 位置解算
# ==========================
def wls_position(ephemeris, pseudoranges):
    """
    使用加权最小二乘法（WLS）解算用户位置
    """
    sv_positions = ephemeris['sv_positions']
    num_sats = sv_positions.shape[0]

    # 初始猜测用户位置
    x_u, y_u, z_u, clock_bias = 0, 0, 0, 0

    for _ in range(5):  # 迭代 5 次
        h_matrix = np.zeros((num_sats, 4))
        delta_p = np.zeros((num_sats, 1))

        for i in range(num_sats):
            dx = sv_positions[i, 0] - x_u
            dy = sv_positions[i, 1] - y_u
            dz = sv_positions[i, 2] - z_u
            r = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

            h_matrix[i, :] = [-dx / r, -dy / r, -dz / r, 1]
            delta_p[i, 0] = pseudoranges[i] - (r + clock_bias)

        # 权重矩阵（对角权重矩阵，可根据 SNR 计算）
        W = np.eye(num_sats)

        # 计算 WLS 解
        x_delta = np.linalg.inv(h_matrix.T @ W @ h_matrix) @ (h_matrix.T @ W @ delta_p)

        # 更新用户位置
        x_u += x_delta[0, 0]
        y_u += x_delta[1, 0]
        z_u += x_delta[2, 0]
        clock_bias += x_delta[3, 0]

    return np.array([x_u, y_u, z_u]), clock_bias


# 计算用户位置
user_position, clock_bias = wls_position(ephemeris, pseudoranges)
print(f"用户 ECEF 位置：{user_position} (m), 时钟偏差: {clock_bias} (m)")


# ==========================
# 3️⃣ 速度解算
# ==========================
def wls_velocity(sv_positions, sv_velocities, pseudorange_rates):
    """
    使用 WLS 计算用户速度
    """
    num_sats = sv_positions.shape[0]
    h_matrix = np.zeros((num_sats, 4))
    delta_r = np.zeros((num_sats, 1))

    for i in range(num_sats):
        dx = sv_positions[i, 0] - user_position[0]
        dy = sv_positions[i, 1] - user_position[1]
        dz = sv_positions[i, 2] - user_position[2]
        r = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

        h_matrix[i, :] = [-dx / r, -dy / r, -dz / r, 1]
        delta_r[i, 0] = pseudorange_rates[i]

    W = np.eye(num_sats)
    x_delta = np.linalg.inv(h_matrix.T @ W @ h_matrix) @ (h_matrix.T @ W @ delta_r)

    return np.array([x_delta[0, 0], x_delta[1, 0], x_delta[2, 0]]), x_delta[3, 0]


# 假设卫星速度（单位 m/s）
sv_velocities = np.array([[1000, 2000, 1500],
                          [1200, 2500, 1300],
                          [900, 1600, 1700],
                          [1100, 1400, 1600]])

# 伪距变化率（单位 m/s）
pseudorange_rates = np.array([500, 600, 550, 580])

# 计算用户速度
user_velocity, clock_drift = wls_velocity(ephemeris['sv_positions'], sv_velocities, pseudorange_rates)
print(f"用户速度（ECEF）：{user_velocity} (m/s), 时钟漂移: {clock_drift} (m/s)")

# ==========================
# 4️⃣ 结果可视化
# ==========================
# 真实坐标（经纬度）
ground_truth = np.array([22.328444770087565, 114.1713630049711])

plt.figure(figsize=(6, 6))
plt.scatter(ground_truth[1], ground_truth[0], color='red', label="Ground Truth", marker="x")
plt.scatter(user_position[0] / 1e6, user_position[1] / 1e6, color='blue', label="WLS Position", marker="o")
plt.xlabel("Longitude (°)")
plt.ylabel("Latitude (°)")
plt.legend()
plt.title("User Position (WLS vs. Ground Truth)")
plt.grid()
plt.show()
