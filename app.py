import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 地図のサイズ
width, height = 100, 100

# 地図模擬データの作成
map_image = np.ones((height, width, 3))

# 3つの人流データを生成
data1 = np.random.rand(height, width)
data2 = np.random.rand(height, width) * 0.7  # データ2
data3 = np.random.rand(height, width) * 1.3  # データ3

st.title("人流ヒートマップ表示")

selected_data = st.sidebar.selectbox(
    "表示するデータを選択してください",
    ("データ1", "データ2", "データ3")
)

if selected_data == "データ1":
    heatmap_data = data1
elif selected_data == "データ2":
    heatmap_data = data2
else:
    heatmap_data = data3

# ヒートマップの作成
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(map_image, extent=[0, width, 0, height])
sns.heatmap(heatmap_data, cmap='YlGnBu', alpha=0.7, cbar=True, ax=ax)

# カーソルをかざした位置の値を表示
x, y = st.mouse_coordinates()
if x and y:
    st.write(f"位置: ({x:.2f}, {y:.2f}), 値: {heatmap_data[int(y), int(x)]:.2f}")

# Streamlitにヒートマップを表示
st.pyplot(fig)