# ----- LIBRARY -----
import streamlit as st
import pandas as pd
import folium
from folium.plugins import Fullscreen
from streamlit_folium import st_folium
from folium import CircleMarker

st.set_page_config(
    page_title="BPS Kota Yogyakarta",
    page_icon="logo/Logo BPS.png",
    layout="wide"
)



# ----- LOAD DATA -----
@st.cache_data
def load_data():
    # Load data dari file Excel
    return pd.read_excel("clear_data.xlsx")

data = load_data()



# ----- Tambahkan Pilihan Jenis Inflasi -----
st.sidebar.header("Filter Jenis Inflasi")
inflasi_options = ["INF(MOM)", "INF(YTD)", "INF(YOY)"]  # Sesuaikan dengan nama kolom Anda
selected_inflasi_type = st.sidebar.selectbox("Pilih Jenis Inflasi:", inflasi_options)



# ----- INFLASI/DEFLASI COLOR FUNCTION -----
def get_color(Inflasi_value):
    if Inflasi_value > 0:
        return "red"  # warna merah untuk inflasi
    elif Inflasi_value < 0:
        return "blue"  # warna biru untuk deflasi
    else:
        return "grey"  # warna abu-abu jika nilai nol





# ----- INTERFACE WEBSITE -----
# ----- Judul Aplikasi -----
st.title("Peta Persebaran Inflasi Komoditas per Kabupaten/Kota Di Indonesia")

# ----- Create SideBar -----
st.sidebar.header("Komoditas Utama")

# ----- Button SideBar Untuk Komoditas Utama -----
st.sidebar.write("Pilih Komoditas : ")
selected_button = None

# ----- List Komoditas Utama + Label -----
commodity_labels = {
    "UMUM": "Umum",
    "BERAS": "Beras",
    "DAGING AYAM RAS": "Daging Ayam Ras",
    "TELUR AYAM RAS": "Telur Ayam Ras",
    "BAWANG MERAH": "Bawang Merah",
    "CABAI MERAH": "Cabe Merah",
    "CABAI RAWIT": "Cabe Rawit",
    "MINYAK GORENG": "Minyak Goreng",
    "GULA PASIR": "Gula Pasir",
    "BAWANG PUTIH": "Bawang Putih",
    "DAGING SAPI": "Daging Sapi",
    "UDANG BASAH": "Udang",
    "IKAN KEMBUNG/IKAN GEMBUNG/ IKAN BANYAR/IKAN GEMBOLO/ IKAN ASO-ASO": "Ikan Kembung",
    "MIE KERING INSTANT": "Mie Instan",
    "TEMPE": "Tempe",
    "TAHU MENTAH": "Tahu Mentah",
    "PISANG": "Pisang",
    "SUSU BUBUK UNTUK BALITA": "Susu Bubuk Balita",
    "SUSU BUBUK": "Susu Bubuk",
    "JERUK": "Jeruk"
}

# ----- Create Button Untuk List Komoditas Dengan Label Custom -----
for commodity, label in commodity_labels.items():
    if st.sidebar.button(label):
        selected_button = commodity  # Menyimpan nama komoditas asli saat tombol diklik

# ----- Daftar Komoditas Lainnya Untuk Selectbox ----- 
komoditas_list = data["Nama"].unique()

# Set pilihan `selectbox` berdasarkan tombol yang diklik atau pilihan pengguna di selectbox
# Jika tombol diklik, atur `selectbox` untuk menampilkan komoditas yang sama
if selected_button:
    # Jika tombol sidebar diklik, atur default `selectbox` ke komoditas dari tombol
    selected_komoditas = st.selectbox("Pilih Komoditas :", komoditas_list, index=list(komoditas_list).index(selected_button))
else:
    # Jika tidak ada tombol yang diklik, biarkan pengguna memilih dari `selectbox` secara manual
    selected_komoditas = st.selectbox("Pilih Komoditas :", komoditas_list)

# ----- Tentukan Komoditas Berdasarkan Pilihan Terakhir -----
komoditas_to_display = selected_button if selected_button else selected_komoditas

# ----- Filter Data Berdasarkan Komoditas Yang Dipilih -----
filtered_data = data[data["Nama"] == komoditas_to_display]




# ----- Buat Peta -----
m = folium.Map(location=[-3.5489, 120.0149], tiles="CartoDB.Voyager", zoom_start=5)

# ----- Plot Marker Berdasarkan Inflasi/Deflasi -----
for _, row in filtered_data.iterrows():
    inflasi_value = row[selected_inflasi_type]  # Gunakan jenis inflasi yang dipilih
    # Cek apakah kota adalah Yogyakarta
    if row["Nama Kota"] == "KOTA YOGYAKARTA":
        # Marker khusus untuk Yogyakarta
        CircleMarker(
            location=(row['latitude'], row['longitude']),
            radius=13,
            color='black',
            fill=True,
            fill_color=get_color(inflasi_value),
            fill_opacity=1.0,
            tooltip=f"{row['Nama Kota']}: <br> MoM: {inflasi_value}"
        ).add_to(m)
    else:
        # Marker umum untuk kota lain
        CircleMarker(
            location=(row['latitude'], row['longitude']),
            radius=5,
            color=get_color(inflasi_value),
            fill=True,
            fill_opacity=1.0,
            tooltip=f"{row['Nama Kota']} <br> MoM: {inflasi_value}"
        ).add_to(m)



# ----- Fullscreen Mneggunakan Plugin -----
Fullscreen(position="topleft").add_to(m)



# ----- Tampilkan Peta Pada Streamlit -----
st_folium(m, width=1400, height=700, returned_objects=[])



# ----- Copyright Footer -----
footer = """
<style>
.footer {
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: center;
}
</style>
<div class="footer">
    <p>Copyright © 2024 BPS Kota Yogyakarta.</p>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)