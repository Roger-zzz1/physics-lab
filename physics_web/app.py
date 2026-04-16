import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. 页面配置 ---
st.set_page_config(page_title="偏振光实验数据处理", layout="wide")

# --- 2. 中文字体修正 (兼容 Linux/Windows/Mac) ---
# 云端服务器通常使用 WenQuanYi Micro Hei 字体显示中文
plt.rcParams['font.sans-serif'] = [
    'SimHei', 
    'WenQuanYi Micro Hei', 
    'Arial Unicode MS', 
    'Songti SC', 
    'sans-serif'
]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题

# --- 3. 页面标题与简介 ---
st.title("🌟 偏振光的观测与研究 - 实验作图工具")
st.markdown("""
本工具用于处理大学物理实验“偏振光的观测与研究”数据。  
**使用说明：** 1. 在下方表格中双击单元格填入你的测量数据。
2. 填写完毕后，点击底部的 **“🚀 生成图像”** 按钮。
3. 生成的图像可以右键另存为图片，用于实验报告。
""")

# --- 4. 数据输入区域 ---
st.divider()

# 表1：马吕斯定律
st.subheader("📝 表1：马吕斯定律验证 (2mW 档位)")
cols1 = [f"{i}°" for i in range(0, 91, 15)]
df1 = pd.DataFrame([[0.0] * len(cols1)], columns=cols1, index=["I_测 (mW)"])
edited_df1 = st.data_editor(df1, use_container_width=True, key="table1")

# 表2：1/2 波片调节
st.subheader("📝 表2：1/2 波片调节 (2mW 档位)")
cols2 = [f"{i}°" for i in range(0, 361, 15)]
df2 = pd.DataFrame([[0.0] * len(cols2)], columns=cols2, index=["I_测 (mW)"])
edited_df2 = st.data_editor(df2, use_container_width=True, key="table2")

# 表3：1/4 波片调节
st.subheader("📝 表3：1/4 波片调节 (2mW 档位)")
cols3 = [f"{i}°" for i in range(0, 361, 30)]
df3 = pd.DataFrame([[0.0] * len(cols3) for _ in range(3)], 
                   columns=cols3, 
                   index=["消光处+30°", "消光处+45°", "消光处+90°"])
edited_df3 = st.data_editor(df3, use_container_width=True, key="table3")

st.divider()

# --- 5. 绘图逻辑 ---
if st.button("🚀 点击生成实验图像", type="primary", use_container_width=True):
    try:
        # 数据读取与转换 
        i_measured_1 = edited_df1.iloc[0].values.astype(float)
        theta_1_deg = np.array([0, 15, 30, 45, 60, 75, 90])
        # 理论值计算过程：I_理 = I_max * cos^2(theta) [cite: 19]
        i_theory_1 = i_measured_1[0] * np.cos(np.radians(theta_1_deg))**2

        i_measured_2 = edited_df2.iloc[0].values.astype(float)
        theta_2_rad = np.radians(np.arange(0, 361, 15))

        i_30 = edited_df3.iloc[0].values.astype(float)
        i_45 = edited_df3.iloc[1].values.astype(float)
        i_90 = edited_df3.iloc[2].values.astype(float)
        theta_3_rad = np.radians(np.arange(0, 361, 30))

        # 创建布局 [cite: 20]
        col1, col2, col3 = st.columns(3)

        # 图像 1：马吕斯定律 (直角坐标)
        with col1:
            fig1, ax1 = plt.subplots(figsize=(5, 5))
            ax1.plot(theta_1_deg, i_measured_1, 'ro-', label='测量值 ($I_{测}$)')
            ax1.plot(theta_1_deg, i_theory_1, 'b^--', label='理论值 ($I_{理}$)')
            ax1.set_title('图1：马吕斯定律验证', fontsize=12)
            ax1.set_xlabel('夹角 $\\theta$ (°)')
            ax1.set_ylabel('光强 $I$ (mW)')
            ax1.set_xticks(theta_1_deg)
            ax1.legend()
            ax1.grid(True, linestyle='--', alpha=0.6)
            st.pyplot(fig1)

        # 图像 2：1/2 波片 (极坐标) 
        with col2:
            fig2 = plt.figure(figsize=(5, 5))
            ax2 = fig2.add_subplot(111, projection='polar')
            ax2.plot(theta_2_rad, i_measured_2, 'bo-', linewidth=1.5, label='1/2波片')
            ax2.set_title('图2：1/2 波片极坐标图', va='bottom', fontsize=12, pad=20)
            ax2.set_theta_zero_location("E") # 0度在右侧
            ax2.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
            st.pyplot(fig2)

        # 图像 3：1/4 波片 (极坐标)
        with col3:
            fig3 = plt.figure(figsize=(5, 5))
            ax3 = fig3.add_subplot(111, projection='polar')
            ax3.plot(theta_3_rad, i_30, 'ro-', label='+30° (椭圆)')
            ax3.plot(theta_3_rad, i_45, 'go-', label='+45° (圆)')
            ax3.plot(theta_3_rad, i_90, 'bo-', label='+90° (线)')
            ax3.set_title('图3：1/4 波片极坐标图', va='bottom', fontsize=12, pad=20)
            ax3.set_theta_zero_location("E")
            ax3.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
            st.pyplot(fig3)
            
        st.success("✅ 处理成功！请检查生成的图像。")
        
    except Exception as e:
        st.error(f"❌ 运行出错：{e}。请检查表格中是否填入了非数字内容。")
