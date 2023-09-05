import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import japanize_matplotlib
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import to_rgba
import plotly.graph_objects as go
import random
import imageio

# データの読み込み
def load_data():
    return pd.read_csv('data/data.csv')

df = load_data()
df['timeStamp'] = pd.to_datetime(df['timeStamp'])
df['year'] = df['timeStamp'].dt.year
df['date'] = df['timeStamp'].dt.date
df['hour'] = df['timeStamp'].dt.hour

# タイトル
st.title('点群')

# サイドバーにフィルターウィジェットを追加
year = 2021
date = st.sidebar.date_input('Choose a date', df['date'].iloc[0])

# 選択された日付に基づいて、利用可能な時間のリストを取得
available_hours = df[df['date'] == date]['hour'].unique()
hour = st.sidebar.selectbox('Choose an hour', available_hours)

# フィルタリング
filtered_df = df[(df['year'] == year) & (df['date'] == date) & (df['hour'] == hour)]

# データのプロット
fig1, ax1 = plt.subplots(figsize=(10, 6))

# 地図画像を背景としてプロット
img = plt.imread('data/map.png')
ax1.imshow(img, extent=[df['xCoordinate'].min(), df['xCoordinate'].max(), df['yCoordinate'].min(), df['yCoordinate'].max()], origin='lower')

# データポイントを地図の上にプロット
ax1.scatter(filtered_df['xCoordinate'], filtered_df['yCoordinate'], color='red', marker='o', alpha=0.7)
ax1.set_title(f'Data for {date} {hour}:00')
ax1.set_xlabel('xCoordinate')
ax1.set_ylabel('yCoordinate')

# ax1.invert_xaxis()
ax1.invert_yaxis()

st.pyplot(fig1)

# ヒートマップ
st.title('ヒートマップ')

# データのプロット
fig2, ax2 = plt.subplots(figsize=(10, 6))

density_min=st.slider('density_min', 0, 100, 0)
density_max=st.slider('density_max', 0, 1000, 100)
slider_bin=st.slider('bins', 0, 100, 18)

# カラーマップの範囲を調整
norm = mcolors.Normalize(vmin=density_min, vmax=density_max)

# 地図画像を背景としてプロット（Y座標の上下を逆にする）
img = plt.imread('data/map.png')
ax2.imshow(img, extent=[df['xCoordinate'].min(), df['xCoordinate'].max(), df['yCoordinate'].min(), df['yCoordinate'].max()], origin='lower')

# カスタムカラーマップ（黄色からオレンジを介して赤のグラデーション）を作成
colors = ['yellow', 'orange', 'red']
n_bin = 100  # カラービンの数
cmap_name = 'custom_yellow_orange_red'
cust_cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)

# 2Dヒストグラム（ヒートマップ）を生成
d = ax2.hist2d(filtered_df['xCoordinate'], filtered_df['yCoordinate'], bins=(slider_bin, slider_bin), alpha=0.6, cmap=cust_cmap, cmin=5, norm=norm)

# カラーバーの追加
cbar = plt.colorbar(d[3], ax=ax2)
cbar.set_label('密度')

ax2.set_title(f'Data for {date} {hour}:00')
ax2.set_xlabel('x座標(mm)')
ax2.set_ylabel('y座標(mm)')

# ax2.invert_xaxis()
ax2.invert_yaxis()

st.pyplot(fig2)

# 3D
st.title('3D')

# 3Dプロットの作成
fig = go.Figure()

# 各userIdごとに移動を線でプロット
unique_users = filtered_df['userId'].unique()
colors = ['#'+ ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(unique_users))]

timestamps = filtered_df['timeStamp'].dt.time.astype(str)

check1 = st.checkbox('全てのユーザーを見る', True)
if check1:
    unique_users_selected = unique_users
else:
	unique_users_selected = st.multiselect('Select users', unique_users)

for i, user_id in enumerate(unique_users_selected):
    user_data = filtered_df[filtered_df['userId'] == user_id]
    fig.add_trace(go.Scatter3d(
        x=user_data['xCoordinate'],
        y=user_data['yCoordinate'],
        z=timestamps,
        mode='lines',
        line=dict(color=colors[i], width=2),
        name=str(user_id)
    ))

# 軸のラベルとz軸のティックラベルを設定
fig.update_layout(scene=dict(
    xaxis_title='xCoordinate',
    yaxis_title='yCoordinate',
    zaxis_title='Time',
    zaxis=dict(tickvals=list(range(len(timestamps))), ticktext=timestamps),
    aspectmode='manual',
    aspectratio=dict(x=1, y=1, z=2)
),
width=1000, 
height=1500  
)

st.plotly_chart(fig, use_container_width=True)