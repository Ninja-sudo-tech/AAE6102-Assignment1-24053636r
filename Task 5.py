'''Task 5 – Kalman filter-based positioning
Develop an Extended Kalman Filter (EKF) using pseudorange and Doppler measurements to estimate user position and velocity.
'''

import numpy as np
import matplotlib.pyplot as plt

# ==========================
# 1️⃣ 初始化 EKF
# ==========================
def initialize_ekf():
    """
    初始化状态向量 X 和协方差矩阵 P
    """
    X = np.zeros((8, 1))  # [x, y, z, vx, vy, vz, b, bd]
    P = np.eye(8) * 100  # 初始不确定性
    return X, P

# ==========================
# 2️⃣ 状态转移模型（时间更新）
# ==========================
def predict_state(X, P, dt):
    """
    使用状态转移矩阵 F 预测状态和协方差矩阵
    """
    F = np.eye(8)
    F[0, 3] = dt  # x = x + vx * dt
    F[1, 4] = dt  # y = y + vy * dt
    F[2, 5] = dt  # z = z + vz * dt
    F[6, 7] = dt  # b = b + bd * dt

    Q = np.eye(8) * 0.01  # 过程噪声

    X = F @ X
    P = F @ P @ F.T + Q
    return X, P


# ==========================
# 3️⃣ 观测更新（伪距 & 多普勒）
# ==========================
def update_state(X, P, sat_pos, sat_vel, pseudoranges, dopplers):
    """
    使用伪距和多普勒测量更新状态
    """
    num_sats = sat_pos.shape[0]
    H = np.zeros((2 * num_sats, 8))
    Y = np.zeros((2 * num_sats, 1))

    for i in range(num_sats):
        dx = sat_pos[i, 0] - X[0]
        dy = sat_pos[i, 1] - X[1]
        dz = sat_pos[i, 2] - X[2]
        r = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

        # 伪距测量方程
        H[i, :3] = [-dx / r, -dy / r, -dz / r]
        H[i, 6] = 1  # 时钟偏移
        Y[i, 0] = pseudoranges[i] - (r + X[6])

        # 多普勒测量方程
        rel_velocity = (dx * X[3] + dy * X[4] + dz * X[5]) / r
        H[num_sats + i, 3:6] = [-dx / r, -dy / r, -dz / r]
        H[num_sats + i, 7] = 1  # 时钟漂移
        Y[num_sats + i, 0] = dopplers[i] - (rel_velocity + X[7])

    R = np.eye(2 * num_sats) * 10  # 观测噪声

    # 计算 Kalman 增益
    S = H @ P @ H.T + R
    K = P @ H.T @ np.linalg.inv(S)

    # 更新状态
    X = X + K @ Y
    P = (np.eye(8) - K @ H) @ P

    return X, P


# ==========================
# 4️⃣ 运行 EKF
# ==========================
def run_ekf(sat_pos, sat_vel, pseudoranges, dopplers, dt=1.0, num_steps=20):
    """
    运行 EKF 进行用户位置和速度估计
    """
    X, P = initialize_ekf()
    positions = []

    for _ in range(num_steps):
        X, P = predict_state(X, P, dt)
        X, P = update_state(X, P, sat_pos, sat_vel, pseudoranges, dopplers)
        positions.append(X[:3].flatten())

    return np.array(positions)


# ==========================
# 5️⃣ 测试 EKF
# ==========================
# 假设 4 颗卫星的 ECEF 坐标（单位：m）
sat_positions = np.array([[15600e3, 7540e3, 20140e3],
                          [18760e3, 2750e3, 18610e3],
                          [17610e3, 14630e3, 13480e3],
                          [19170e3, 610e3, 18390e3]])

# 假设 4 颗卫星的速度（单位：m/s）
sat_velocities = np.array([[1000, 2000, 1500],
                           [1200, 2500, 1300],
                           [900, 1600, 1700],
                           [1100, 1400, 1600]])

# 伪距测量（单位：m）
pseudoranges = np.array([2.407e7, 2.412e7, 2.423e7, 2.425e7])

# 多普勒测量（单位：m/s）
doppler_measurements = np.array([500, 600, 550, 580])

# 运行 EKF
ekf_positions = run_ekf(sat_positions, sat_velocities, pseudoranges, doppler_measurements)

# 真实坐标（经纬度）
ground_truth = np.array([22.328444770087565, 114.1713630049711])

# ==========================
# 6️⃣ 结果可视化
# ==========================
plt.figure(figsize=(6, 6))
plt.plot(ekf_positions[:, 0] / 1e6, ekf_positions[:, 1] / 1e6, label="EKF Trajectory", marker="o")
plt.scatter(ground_truth[1], ground_truth[0], color='red', label="Ground Truth", marker="x")
plt.xlabel("Longitude (°)")
plt.ylabel("Latitude (°)")
plt.legend()
plt.title("User Position (EKF vs. Ground Truth)")
plt.grid()
plt.show()
