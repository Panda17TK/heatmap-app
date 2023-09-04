import streamlit as st
import numpy as np
import pydeck as pdk
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static



st.title("人流ヒートマップ表示")

# 時間帯のリスト
hours = list(range(6, 18))

# 人の属性のリスト
attributes = [f"{i}0代{'女性' if j == 0 else '男性'}" for i in range(1, 9) for j in range(2)]

# 座標の生成 (10x10)
coordinates = [(x, y) for x in range(10) for y in range(10)]

# ダミーデータの生成
data = {
    "X": [],
    "Y": [],
    "Hour": [],
    "Attribute": [],
    "Count": []
}

for x, y in coordinates:
    for hour in hours:
        for attribute in attributes:
            data["X"].append(x)
            data["Y"].append(y)
            data["Hour"].append(hour)
            data["Attribute"].append(attribute)
            data["Count"].append(np.random.randint(1, 100))  # 1から99までのランダムな滞在人数

# データフレームの作成
df = pd.DataFrame(data)


# セレクトボックスからの入力を取得
#hour_selected = st.selectbox("時間を選択", list(range(6, 18)))
#attribute_selected = st.selectbox("属性を選択", [f"{i}0代{'女性' if j == 0 else '男性'}" for i in range(1, 9) for j in range(2)])

# 選択された時間と属性に基づくデータをフィルタリング
#filtered_data = df[(df["Hour"] == hour_selected) & (df["Attribute"] == attribute_selected)]

# ヒートマップの作成
#m = folium.Map([4.5, 4.5], zoom_start=7)

#heat_data = [[row['X'], row['Y'], row['Count']] for _, row in filtered_data.iterrows()]
#HeatMap(heat_data, radius=10).add_to(m)

#folium_static(m)

# セレクトボックスからの入力を取得
hour_selected = st.selectbox("時間を選択", list(range(6, 18)))
attribute_selected = st.selectbox("属性を選択", [f"{i}0代{'女性' if j == 0 else '男性'}" for i in range(1, 9) for j in range(2)])

# 選択された時間と属性に基づくデータをフィルタリング
filtered_data = df[(df["Hour"] == hour_selected) & (df["Attribute"] == attribute_selected)]

# ヒートマップの作成
m = folium.Map([4.5, 4.5], zoom_start=7)

# カラーマッピングのための関数
def color_mapper(count):
    if count < 25:
        return '#fee5d9'
    elif count < 50:
        return '#fcbba1'
    elif count < 75:
        return '#fc9272'
    else:
        return '#de2d26'

for _, row in filtered_data.iterrows():
    folium.Rectangle(
        bounds=[[row['X'], row['Y']], [row['X'] + 1, row['Y'] + 1]],
        color=color_mapper(row['Count']),
        fill=True,
        fill_color=color_mapper(row['Count'])
    ).add_to(m)

folium_static(m)