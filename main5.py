# ターミナルでfoliumのインポート
# 参考ULR：https://welovepython.net/streamlit-folium/
import streamlit as st                      # streamlit
from streamlit_folium import st_folium      # streamlitでfoliumを使う
import folium                               # folium
from folium import FeatureGroup             # FeatureGrop
import pandas as pd                         # CSVをデータフレームとして読み込む



#  表示するデータを読み込み
df = pd.read_csv('221218-2025_hotpepper_beer.csv')



# 銘柄でのデータを抽出
all_data = df[df["menu"].str.contains("モルツ|アサヒ|ヱビス|キリン|プレミアム|ヒューガルデン|コロナ|ギネス")] #全店舗
mlts_data = df[df["menu"].str.contains("モルツ")]
asahi_data = df[df["menu"].str.contains("アサヒ")]
ebis_data = df[df["menu"].str.contains("ヱビス")]
kirin_data = df[df["menu"].str.contains("キリン")]
premium_data = df[df["menu"].str.contains("プレミアム")]
hoeg_data = df[df["menu"].str.contains("ヒューガルデン")]
corona_data = df[df["menu"].str.contains("コロナ")]
guinness_data = df[df["menu"].str.contains("ギネス")]



# セレクトボックス
bland_options = st.sidebar.selectbox(
    'ご希望のビール銘柄をお選びください。',
    ['全店舗','モルツ', 'アサヒ', 'ヱビス', 'キリン', 'プレミアム', 'ヒューガルデン', 'コロナ', 'ギネス'])

st.sidebar.write('現在の選択:', bland_options)



# スライダー
price_slider = st.sidebar.slider(
    '1杯の値段で絞り込みができます',
    min_value = 100,
    max_value = 1000,
    value = 500,
    step = 10,
    )
st.sidebar.write('希望価格：100円～', price_slider, '円です。')


all_data = all_data[all_data["price"] <= price_slider]
asahi_data = asahi_data[asahi_data["price"] <= price_slider]
kirin_data = kirin_data[kirin_data["price"] <= price_slider]
ebis_data = ebis_data[ebis_data["price"] <= price_slider]
premium_data = premium_data[premium_data["price"] <= price_slider]
mlts_data = mlts_data[mlts_data["price"] <= price_slider]
hoeg_data = hoeg_data[hoeg_data["price"] <= price_slider]



# 全店舗（all_map)：地図の中心の緯度/経度、タイル、初期のズームサイズを指定
all_map = folium.Map(
    # 地図の中心位置の指定(今回は大梅田駅を指定)
    location = [34.7055051, 135.4983028], 
    # タイル（デフォルトはOpenStreetMap)、アトリビュート(attr:右下の出典情報はデフォルト指定時は不要)指定
    tiles='https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg',
    attr='全国最新写真（シームレス）',
    # ズームを指定
    # 参考URL：https://maps.gsi.go.jp/development/ichiran.html#pale
    zoom_start = 15
)

#全店舗の層を作成
all_group = FeatureGroup(name="全店舗")

# 全店舗グループにマーカーを差す
all_group_popups = all_data["name"].values.tolist() # popup用の駅名配列
all_group_latlngs = all_data.iloc[:,6:8].values.tolist() # 座標の2次元配列


for i, row in df.iterrows():
    pop=f"{row['name']}<br>ジャンル：{row['genre']}<br>Hotpepper{row['url']}"


# darkblueのマーカーを全店舗の座標に差し、グループに追加
for name, latlng in zip(all_group_popups, all_group_latlngs): 
    folium.Marker(
        location=latlng, 
        popup = folium.Popup(pop, max_width=300),
        icon = folium.Icon(icon="beer", prefix='fa', icon_color="white", color="darkblue")
    ).add_to(all_group)




# アサヒマップ(asahi_map)；
asahi_map = folium.Map(
    location = [34.7055051, 135.4983028], 
    tiles = 'OpenStreetMap',
    zoom_start = 15
)

asahi_group = FeatureGroup(name="アサヒ")

asahi_group_popups = asahi_data["name"].values.tolist() 
asahi_group_latlngs = asahi_data.iloc[:,6:8].values.tolist() 


for name, latlng in zip(asahi_group_popups, asahi_group_latlngs): 
    folium.Marker(
        location=latlng, 
        popup = folium.Popup(pop, max_width=300),
        icon = folium.Icon(icon="beer", prefix='fa', icon_color="white", color="gray")
    ).add_to(asahi_group)




# キリン（kirin_map)：
kirin_map = folium.Map(
    location = [34.7055051, 135.4983028], 
    tiles = 'OpenStreetMap',
    zoom_start = 15
)

kirin_group = FeatureGroup(name="キリン")

kirin_group_popups = kirin_data["name"].values.tolist() 
kirin_group_latlngs = kirin_data.iloc[:,6:8].values.tolist() 



for name, latlng in zip(kirin_group_popups, kirin_group_latlngs): 
    folium.Marker(
        location=latlng, 
        popup = folium.Popup(pop, max_width=300),
        icon = folium.Icon(icon="beer", prefix='fa', icon_color="white", color="lightred")
    ).add_to(kirin_group)





# ヱビスマップ（ebis_map)
ebis_map = folium.Map(
    location = [34.7055051, 135.4983028], 
    tiles = 'OpenStreetMap',
    zoom_start = 15
)

ebis_group = FeatureGroup(name="ヱビス")

ebis_group_popups = ebis_data["name"].values.tolist() 
ebis_group_latlngs = ebis_data.iloc[:,6:8].values.tolist() 



for name, latlng in zip(ebis_group_popups, ebis_group_latlngs): 
    folium.Marker(
        location=latlng, 
        popup = folium.Popup(pop, max_width=300),
        icon = folium.Icon(icon="beer", prefix='fa', icon_color="white", color="orange")
    ).add_to(ebis_group)





# プレミアムマップ（premium_map)：
premium_map = folium.Map(
    location = [34.7055051, 135.4983028], 
    tiles = 'OpenStreetMap',
    zoom_start = 15
)

premium_group = FeatureGroup(name="プレミアム")

premium_group_popups = premium_data["name"].values.tolist()
premium_group_latlngs = premium_data.iloc[:,6:8].values.tolist() 


for name, latlng in zip(premium_group_popups, premium_group_latlngs): 
    folium.Marker(
        location=latlng, 
        popup = folium.Popup(pop, max_width=300),
        icon = folium.Icon(icon="beer", prefix='fa', icon_color="white", color="darkred")
    ).add_to(premium_group)







# モルツマップ（mlts_map)
mlts_map = folium.Map(
    location = [34.7055051, 135.4983028], 
    tiles = 'OpenStreetMap',
    zoom_start = 15
)

mlts_group = FeatureGroup(name="モルツ")

mlts_group_popups = mlts_data["name"].values.tolist() 
mlts_group_latlngs = mlts_data.iloc[:,6:8].values.tolist() 


for name, latlng in zip(mlts_group_popups, mlts_group_latlngs): 
    folium.Marker(
        location=latlng, 
        popup = folium.Popup(pop, max_width=300),
        icon = folium.Icon(icon="beer", prefix='fa', icon_color="white", color="blue")
    ).add_to(mlts_group)




# ヒューガルデンマップ（hoeg_map)：
hoeg_map = folium.Map(
    location = [34.7055051, 135.4983028], 
    tiles = 'OpenStreetMap',
    zoom_start = 15
)


hoeg_group = FeatureGroup(name="ヒューガルデン")

hoeg_group_popups = hoeg_data["name"].values.tolist()
hoeg_group_latlngs = hoeg_data.iloc[:,6:8].values.tolist() 


for name, latlng in zip(hoeg_group_popups, hoeg_group_latlngs): 
    folium.Marker(
        location=latlng, 
        popup = folium.Popup(pop, max_width=300),
        icon = folium.Icon(icon="beer", prefix='fa', icon_color="gray", color="white")
    ).add_to(hoeg_group)




# コロナマップ（corona_map)：
corona_map = folium.Map(
    location = [34.7055051, 135.4983028], 
    tiles = 'OpenStreetMap',
    zoom_start = 15
)


corona_group = FeatureGroup(name="コロナ")

corona_group_popups = corona_data["name"].values.tolist()
corona_group_latlngs = corona_data.iloc[:,6:8].values.tolist() 


for name, latlng in zip(corona_group_popups, corona_group_latlngs): 
    folium.Marker(
        location=latlng, 
        popup = folium.Popup(pop, max_width=300),
        icon = folium.Icon(icon="beer", prefix='fa', icon_color="white", color="beige")
    ).add_to(corona_group)




#ギネスマップ（guinness_map)：
guinness_map = folium.Map(
    location = [34.7055051, 135.4983028], 
    tiles = 'OpenStreetMap',
    zoom_start = 15
)


guinness_group = FeatureGroup(name="ギネス")

guinness_group_popups = guinness_data["name"].values.tolist()
guinness_group_latlngs = guinness_data.iloc[:,6:8].values.tolist() 


for name, latlng in zip(guinness_group_popups, guinness_group_latlngs): 
    folium.Marker(
        location=latlng, 
        popup = folium.Popup(pop, max_width=300),
        icon = folium.Icon(icon="beer", prefix='fa', icon_color="white", color="black")
    ).add_to(guinness_group)







# 各銘柄を地図に追加
all_group.add_to(all_map)
asahi_group.add_to(asahi_map)
kirin_group.add_to(kirin_map)
ebis_group.add_to(ebis_map)
premium_group.add_to(premium_map)
mlts_group.add_to(mlts_map)
hoeg_group.add_to(hoeg_map)
corona_group.add_to(corona_map)
guinness_group.add_to(guinness_map)



#追記 最安値
all_min_price = int(df["price"].min())
all_mean_price = int(df["price"].mean())


asahi_min_price = int(asahi_data["price"].min())
asahi_mean_price = int(asahi_data["price"].mean())

kirin_min_price = int(kirin_data["price"].min())
kirin_mean_price = int(kirin_data["price"].mean())

ebis_min_price = int(ebis_data["price"].min())
ebis_mean_price = int(ebis_data["price"].mean())

premium_min_price = int(premium_data["price"].min())
premium_mean_price = int(premium_data["price"].mean())

mlts_min_price = int(mlts_data["price"].min())
mlts_mean_price = int(mlts_data["price"].mean())

hoeg_min_price = int(hoeg_data["price"].min())
hoeg_mean_price = int(hoeg_data["price"].mean())

corona_min_price = int(corona_data["price"].min())
corona_mean_price = int(corona_data["price"].mean())

guinness_min_price = int(guinness_data["price"].min())
guinness_mean_price = int(guinness_data["price"].mean())




if bland_options == '全店舗':
    st.write('ビールが飲めるお店')
    st_folium(all_map, width=700, height=700)
    st.sidebar.write('大阪市北区のビール1杯の最安値は、',all_min_price,'円です')
    st.sidebar.write('大阪市北区のビール1杯の平均価格は、',all_mean_price,'円です')


if bland_options == 'アサヒ':
    st.write('アサヒが飲めるお店')
    st_folium(asahi_map, width=700, height=700)
    st.sidebar.write('大阪市北区のモルツビール1杯の最安値は、',asahi_min_price,'円です')
    st.sidebar.write('大阪市北区のモルツビール1杯の平均価格は、',asahi_mean_price,'円です')


if bland_options == 'キリン':
    st.write('キリンが飲めるお店')
    st_folium(kirin_map, width=700, height=700)
    st.sidebar.write('大阪市北区のキリン1杯の最安値は、',kirin_min_price,'円です')
    st.sidebar.write('大阪市北区のキリン1杯の平均価格は、',kirin_mean_price,'円です')


if bland_options == 'ヱビス':
    st.write('ヱビスが飲めるお店')
    st_folium(ebis_map, width=700, height=700)
    st.sidebar.write('大阪市北区のヱビス1杯の最安値は、',ebis_min_price,'円です')
    st.sidebar.write('大阪市北区のヱビスビール1杯の平均価格は、',ebis_mean_price,'円です')


if bland_options == 'プレミアム':
    st.write('プレミアムが飲めるお店')
    st_folium(premium_map, width=700, height=700)
    st.sidebar.write('大阪市北区のプレミアム1杯の最安値は、',premium_min_price,'円です')
    st.sidebar.write('大阪市北区のプレミアム1杯の平均価格は、',premium_mean_price,'円です')


if bland_options == 'モルツ':
    st.write('モルツが飲めるお店')
    st_folium(mlts_map, width=700, height=700)
    st.sidebar.write('大阪市北区のモルツビール1杯の最安値は、',mlts_min_price,'円です')
    st.sidebar.write('大阪市北区のモルツビール1杯の平均価格は、',mlts_mean_price,'円です')


if bland_options == 'ヒューガルデン':
    st.write('ヒューガルデンが飲めるお店')
    st_folium(hoeg_map, width=700, height=700)
    st.sidebar.write('大阪市北区のヒューガルデン1杯の最安値は、',hoeg_min_price,'円です')
    st.sidebar.write('大阪市北区のヒューガルデン1杯の平均価格は、',hoeg_mean_price,'円です')


if bland_options == 'コロナ':
    st.write('コロナビールが飲めるお店')
    st_folium(corona_map, width=700, height=700)
    st.sidebar.write('大阪市北区のコロナビール1杯の最安値は、',corona_min_price,'円です')
    st.sidebar.write('大阪市北区のコロナビール1杯の平均価格は、',corona_mean_price,'円です')
    
if bland_options == 'ギネス':
    st.write('ギネスビールが飲めるお店')
    st_folium(guinness_map, width=700, height=700)
    st.sidebar.write('大阪市北区のギネスビール1杯の最安値は、',guinness_min_price,'円です')
    st.sidebar.write('大阪市北区のギネスビール1杯の平均価格は、',guinness_mean_price,'円です')







