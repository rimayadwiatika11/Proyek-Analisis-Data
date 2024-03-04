import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk menghitung total penyewaan per jam
def get_total_count_by_hour_df(hour_df):
    hour_count_df = hour_df.groupby(by="hours").agg({"count": ["sum"]})
    return hour_count_df

# Fungsi untuk menghitung total penyewaan per hari dalam rentang tahun 2011-2012
def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query('dateday >= "2011-01-01" and dteday < "2012-12-31"')
    return day_df_count_2011

# Fungsi untuk menghitung total pelanggan terdaftar per hari
def total_registered_df(day_df):
    reg_df = day_df.groupby(by="dateday").agg({"registered": "sum"})
    reg_df = reg_df.reset_index()
    reg_df.rename(columns={"registered": "register_sum"}, inplace=True)
    return reg_df

# Fungsi untuk menghitung total pelanggan casual per hari
def total_casual_df(day_df):
    cas_df = day_df.groupby(by="dateday").agg({"casual": ["sum"]})
    cas_df = cas_df.reset_index()
    cas_df.rename(columns={"casual": "casual_sum"}, inplace=True)
    return cas_df

# Fungsi untuk menghitung total order per jam
def sum_order(hour_df):
    sum_order_items_df = hour_df.groupby("hours").count.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

# Fungsi untuk menghitung total penyewaan berdasarkan musim
def macem_season(day_df): 
    season_df = day_df.groupby(by="season").count.sum().reset_index() 
    return season_df

# Fungsi untuk analisis pertanyaan ekploratory pertama
def analisis_cuaca(day_df):
    st.header("Analisis Hubungan Kondisi Cuaca dengan Jumlah Peminjaman")
    colors = ["#4CAF50", "#00FF00", "#33FF57"]
    plt.figure(figsize=(12, 8))
    sns.barplot(
        x="weather",
        y="count",
        data=day_df.sort_values(by="weather", ascending=False),
        palette=colors
    )
    plt.title("Grafik Perkiraan Peminjaman Berdasarkan Cuaca", fontsize=20)
    plt.xlabel("Cuaca", fontsize=15)
    plt.ylabel("Jumlah Peminjaman Sepeda", fontsize=15)
    st.pyplot(plt)
    st.write("Terlihat bahwa cuaca yang cerah (clear) memiliki jumlah peminjaman sepeda tertinggi.")

# Fungsi untuk analisis pertanyaan ekploratory kedua
def analisis_pola_peminjaman(day_df):
    st.header("Analisis Pola Peminjaman Pelanggan di Hari Libur atau Tidak Libur, Langsung (Casual) atau Member (Registered)")
    hasil = day_df.groupby(['holiday', 'workingday']).agg({'casual': 'sum', 'registered': 'sum'})
    colors = ["#FF5733", "#33FF57"]
    fig, ax = plt.subplots(figsize=(10, 6))
    hasil.plot(kind='bar', stacked=True, ax=ax, color=colors)
    plt.title('Total Peminjaman per Hari Libur atau Tidak Libur')
    plt.xlabel('Hari Libur atau Tidak Libur')
    plt.ylabel('Total Peminjaman')
    plt.legend(title='Jenis Pelanggan', loc='upper right')
    st.pyplot(fig)
    st.write("Terlihat bahwa pola peminjaman lebih banyak dilakukan oleh pelanggan registered pada hari kerja (workingday).")

# Fungsi untuk analisis pertanyaan ekploratory ketiga
def analisis_pukul_peminjaman(hour_df):
    st.header("Analisis Pukul Berapa Peminjaman Sepeda Meningkat")
    peminjaman_per_jam = hour_df.groupby('hours')['count'].sum()
    plt.figure(figsize=(10, 6))
    plt.plot(peminjaman_per_jam.index, peminjaman_per_jam.values, marker='o', linestyle='-', color='#00FF00')
    plt.title('Jumlah Peminjaman Sepeda per Jam')
    plt.xlabel('Jam')
    plt.ylabel('Jumlah Peminjaman')
    plt.grid(True)
    st.pyplot(plt)
    st.write("Terlihat bahwa peminjaman sepeda meningkat pada pukul 17.00.")

# Membaca data dari file CSV
day_df = pd.read_csv("day_data.csv")
hour_df = pd.read_csv("hour_data.csv")

# Melakukan penyesuaian pada kolom datetime
datetime_columns = ["dateday"]
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hour_df[column] = pd.to_datetime(hour_df[column])

# Sidebar untuk rentang tanggal
with st.sidebar:
    st.header("Pengaturan Rentang Waktu")
    min_date_day = day_df['dateday'].min()
    max_date_day = day_df['dateday'].max()
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=pd.to_datetime(min_date_day),
        max_value=pd.to_datetime(max_date_day),
        value=[pd.to_datetime(min_date_day), pd.to_datetime(max_date_day)]
    )

# Filter data berdasarkan rentang tanggal yang dipilih
main_df_day = day_df[(day_df["dateday"] >= start_date) & (day_df["dateday"] <= end_date)]
main_df_hour = hour_df[(hour_df["dateday"] >= start_date) & (hour_df["dateday"] <= end_date)]

# Visualisasi 1: Grafik Perkiraan Peminjaman Berdasarkan Cuaca
st.header("Grafik Perkiraan Peminjaman Berdasarkan Cuaca")
sns.set_style("whitegrid")
colors = ["#4CAF50", "#00FF00", "#33FF57"]
plt.figure(figsize=(12, 8))
sns.barplot(
    x="weather",
    y="count",
    data= main_df_day.sort_values(by="weather", ascending=False),
    palette=colors
)
plt.title("Grafik Perkiraan Peminjaman Berdasarkan Cuaca", fontsize=20)
plt.xlabel("Cuaca", fontsize=15)
plt.ylabel("Jumlah Peminjaman Sepeda", fontsize=15)
st.pyplot(plt)

# Visualisasi 2: Total Peminjaman per Tahun dan Hari Libur
st.header("Total Peminjaman per Tahun dan Hari Libur")
hasil = main_df_day.groupby(['year', 'holiday'], observed=False)[['casual', 'registered']].sum()
colors = ["#FF5733", "#33FF57"]
fig, ax = plt.subplots(figsize=(10, 6))
hasil.plot(kind='bar', stacked=True, ax=ax, color=colors)
plt.title('Total Peminjaman per Tahun dan Hari Libur')
plt.xlabel('Tahun dan Hari Libur')
plt.ylabel('Total Peminjaman')
plt.legend(title='Jenis Pelanggan', loc='upper right')
st.pyplot(fig)

# Visualisasi 3: Jumlah Peminjaman Sepeda per Jam
st.header("Jumlah Peminjaman Sepeda per Jam")
peminjaman_per_jam = main_df_hour.groupby('hour')['count'].sum()
plt.figure(figsize=(10, 6))
plt.plot(peminjaman_per_jam.index, peminjaman_per_jam.values, marker='o', linestyle='-', color='#00FF00')
plt.title('Jumlah Peminjaman Sepeda per Jam')
plt.xlabel('Jam')
plt.ylabel('Jumlah Peminjaman')
plt.grid(True)
st.pyplot(plt)

# Kesimpulan
st.subheader("Kesimpulan Pertanyaan:")
st.markdown("- **Pertanyaan 1:** Cuaca memiliki hubungan dengan seberapa banyak pelanggan yang melakukan peminjaman sepeda di waktu tersebut. Sehingga, kita dapat memperkirakan bahwa peminjaman sepeda akan meningkat di cuaca yang cerah (clear) karena pada saat itulah pelanggan merasa nyaman dalam bermain sepeda.")
st.markdown("- **Pertanyaan 2:** Pelanggan lebih sering melakukan peminjaman sepeda menggunakan pola mendaftar sebagai member terlebih dahulu dibanding secara langsung (tanpa terdaftar sebagai member) baik itu di waktu liburan maupun hari biasa. Kemungkinan, dengan mendaftar sebagai member mereka bisa rutin melakukan peminjaman sehingga lebih teratur dan berharap mendapatkan promo menarik apabila terdaftar sebagai member.")
st.markdown("- **Pertanyaan 3:** Pelanggan lebih sering melakukan peminjaman sepeda pada pukul 17.00 dan disaat itulah peminjaman akan meningkat. Kemungkinan, hal itu terjadi karena cuaca sore adalah waktu yang tepat dan baik untuk berolahraga sepeda.")
