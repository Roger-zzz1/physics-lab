import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. 页面配置 ---
st.set_page_config(page_title="偏振光实验数据处理", layout="wide")

st.title("🌟 偏振光实验作图工具")
st.markdown("""
**使用说明：** 1. 双击表格填入测量数据。
2. 点击底部按钮生成图像。
*(注：为避免云端字体报错，图像内已全部替换为国际通用物理符号)*
""")

st.divider()

# --- 2. 数据输入区域 ---
# 表1：马吕斯定律
st.subheader("📝 表1：马吕斯定律验证")
cols1 = [f"{i}°" for i in range(0, 91, 15)]
df1 = pd.DataFrame([[0.0] * len(cols1)], columns=cols1, index=["I (mW)"])
edited_df1 = st.data_editor(df1, use_container_width=True, key="table1")

# 表2：1/2 波片
st.subheader("📝 表2：1/2 波片调节")
cols2 = [f"{i}°" for i in range(0, 361, 15)]
df2 = pd.DataFrame([[0.0] * len(cols2)], columns=cols2, index=["I (mW)"])
edited_df2 = st.data_editor(df2, use_container_width=True, key="table2")

# 表3：1/4 波片
st.subheader("📝 表3：1/4 波片调节")
cols3 = [f"{i}°" for i in range(0, 361, 30)]
df3 = pd.DataFrame([[0.0] * len(cols3) for _ in range(3)], 
                   columns=cols3, 
                   index=["+30°", "+45°", "+90°"])
edited_df3 = st.data_editor(df3, use_container_width=True, key="table3")

st.divider()

# --- 3. 绘图逻辑 ---
if st.button("🚀 生成实验图像", type="primary", use_container_width=True):
    try:
        # 读取数据
        i_measured_1 = edited_df1.iloc[0].values.astype(float)
        theta_1_deg = np.array([0, 15, 30, 45, 60, 75, 90])
        i_theory_1 = i_measured_1[0] * np.cos(np.radians(theta_1_deg))**2

        i_measured_2 = edited_df2.iloc[0].values.astype(float)
        theta_2_rad = np.radians(np.arange(0, 361, 15))

        i_30 = edited_df3.iloc[0].values.astype(float)
        i_45 = edited_df3.iloc[1].values.astype(float)
        i_90 = edited_df3.iloc[2].values.astype(float)
        theta_3_rad = np.radians(np.arange(0, 361, 30))

        # 布局分为三列
        col1, col2, col3 = st.columns(3)

        # 图像 1：马吕斯定律
        with col1:
            st.markdown("##### 图1：马吕斯定律") # 用网页显示中文标题
            fig1, ax1 = plt.subplots(figsize=(5, 5))
            ax1.plot(theta_1_deg, i_measured_1, 'ro-', label=r'$I_{exp}$')  # exp代表实验值
            ax1.plot(theta_1_deg, i_theory_1, 'b^--', label=r'$I_{th}$')    # th代表理论值
            ax1.set_xlabel(r'$\theta\ (^\circ)$', fontsize=12)
            ax1.set_ylabel(r'$I\ (mW)$', fontsize=12)
            ax1.set_xticks(theta_1_deg)
            ax1.legend()
            ax1.grid(True, linestyle='--', alpha=0.6)
            st.pyplot(fig1)

        # 图像 2：1/2 波片极坐标图
        with col2:
            st.markdown("##### 图2：1/2 波片极坐标")
            fig2 = plt.figure(figsize=(5, 5))
            ax2 = fig2.add_subplot(111, projection='polar')
            ax2.plot(theta_2_rad, i_measured_2, 'bo-', linewidth=1.5,
