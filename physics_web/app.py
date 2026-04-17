import numpy as np
import matplotlib.pyplot as plt

# --- 1. 在这里填入你的实验测量数据 ---
# 表1：马吕斯定律 (7个数据点)
i_measured_1 = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]) 

# 表2：1/2 波片 (25个数据点，0°到360°)
i_measured_2 = np.array([0.0] * 25) 

# 表3：1/4 波片 (各13个数据点，0°到360°)
i_30 = np.array([0.0] * 13) 
i_45 = np.array([0.0] * 13) 
i_90 = np.array([0.0] * 13) 

# --- 2. 坐标与理论值计算 ---
theta_1_deg = np.array([0, 15, 30, 45, 60, 75, 90])
# 理论值：I_theory = I_max * cos^2(theta)
i_theory_1 = i_measured_1[0] * np.cos(np.radians(theta_1_deg))**2

theta_2_rad = np.radians(np.arange(0, 361, 15))
theta_3_rad = np.radians(np.arange(0, 361, 30))

# --- 3. 纯净版绘图 (无任何文字标签) ---
fig = plt.figure(figsize=(15, 5))

# 图1：马吕斯定律 (直角坐标系)
ax1 = fig.add_subplot(131)
ax1.plot(theta_1_deg, i_measured_1, 'ro-')  # 测量值 (红实线)
ax1.plot(theta_1_deg, i_theory_1, 'b^--')   # 理论值 (蓝虚线)
ax1.set_xticks(theta_1_deg)
ax1.grid(True, linestyle='--', alpha=0.6)

# 图2：1/2 波片 (极坐标系)
ax2 = fig.add_subplot(132, projection='polar')
ax2.plot(theta_2_rad, i_measured_2, 'bo-', linewidth=1.5)
ax2.set_theta_zero_location("E") # 0度在右侧

# 图3：1/4 波片 (极坐标系)
ax3 = fig.add_subplot(133, projection='polar')
ax3.plot(theta_3_rad, i_30, 'ro-')
ax3.plot(theta_3_rad, i_45, 'go-')
ax3.plot(theta_3_rad, i_90, 'bo-')
ax3.set_theta_zero_location("E")

plt.tight_layout()
plt.show()
