import streamlit as st
import numpy as np
import pydeck as pdk

st.title("人流ヒートマップ表示")

# 3つダミー人流データを生成
data1 = np.random.rand(100, 100)
data2 = np.random.rand(100, 100) * 0.7
data3 = np.random.rand(100, 100) * 1.3

# タイトル
st.title("インタラクティブな人流ヒートマップ")

# サイドバーにデータ選択用のセレクトボックスを追加
selected_data = st.sidebar.selectbox(
    "表示するデータを選択してください",
    ("データ1", "データ2", "データ3")
)

# 選択されたデータに基づいてヒートマップデータを設定
if selected_data == "データ1":
    heatmap_data = data1
elif selected_data == "データ2":
    heatmap_data = data2
else:
    heatmap_data = data3

# ヒートマップのデータをpydeck用の形式に変換
heatmap_list = []
for i in range(100):
    for j in range(100):
        heatmap_list.append([j, i, heatmap_data[i][j]])

# pydeckでヒートマップを作成
layer = pdk.Layer(
    "HeatmapLayer",
    heatmap_list,
    opacity=0.7,
    get_position="[x, y]",
    get_weight="z"
)

view_state = pdk.ViewState(latitude=50, longitude=50, zoom=10)
deck = pdk.Deck(layers=[layer], initial_view_state=view_state)
st.pydeck_chart(deck)