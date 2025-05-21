import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.neighbors import NearestNeighbors
import uuid

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("NCT_DREAM_KONSER.xlsx")
    return df

df = load_data()

# Simpan riwayat pemesanan dalam session
if 'riwayat' not in st.session_state:
    st.session_state.riwayat = []

# Sidebar menu
st.sidebar.title("🎤 NCT Dream Concert App")
menu = st.sidebar.radio("Pilih Fitur", ["📊 EDA & Visualisasi", "🧠 Prediksi Kursi", "🎫 Rekomendasi Konser", "🛒 Pemesanan Tiket", "📜 Riwayat Pemesanan"])

# ------------------ EDA & Visualisasi ------------------ #
if menu == "📊 EDA & Visualisasi":
    st.title("📊 EDA dan Visualisasi")

    st.subheader("Jumlah Konser per Negara")
    negara_count = df['Negara'].value_counts()
    st.bar_chart(negara_count)

    st.subheader("Kategori Kursi Paling Sering Tersedia / Tidak")
    kursi_status = df.groupby(['Seat Kursi', 'Status Kursi']).size().unstack()
    st.bar_chart(kursi_status)

    st.subheader("Harga Kursi vs Status Kursi")
    fig, ax = plt.subplots()
    sns.boxplot(x='Status Kursi', y='Harga', data=df, ax=ax)
    st.pyplot(fig)

    st.subheader("Distribusi Nomor Kursi")
    st.write(df['Nomor Kursi'].value_counts().sort_index())

# ------------------ Prediksi Kursi ------------------ #
elif menu == "🧠 Prediksi Kursi":
    st.title("🧠 Prediksi Kursi Laku atau Tidak")

    df_pred = df.copy()
    df_pred['Status Kursi'] = df_pred['Status Kursi'].apply(lambda x: 0 if x == "Tersedia" else 1)

    encoders = {}
    for col in ['Negara', 'Seat Kursi', 'Lokasi', 'Kota']:
        le = LabelEncoder()
        df_pred[col] = le.fit_transform(df_pred[col])
        encoders[col] = le

    X = df_pred[['Negara', 'Seat Kursi', 'Harga', 'Lokasi', 'Kota']]
    y = df_pred['Status Kursi']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    st.code(classification_report(y_test, y_pred, output_dict=False), language="text")

    st.subheader("Coba Prediksi Sendiri:")
    negara = st.selectbox("Negara", df['Negara'].unique())
    seat = st.selectbox("Seat Kursi", df['Seat Kursi'].unique())
    harga = st.number_input("Harga", value=3000000)
    lokasi = st.selectbox("Lokasi", df['Lokasi'].unique())
    kota = st.selectbox("Kota", df['Kota'].unique())

    input_data = pd.DataFrame([[
        encoders['Negara'].transform([negara])[0],
        encoders['Seat Kursi'].transform([seat])[0],
        harga,
        encoders['Lokasi'].transform([lokasi])[0],
        encoders['Kota'].transform([kota])[0]
    ]], columns=X.columns)

    hasil = model.predict(input_data)[0]
    if hasil == 1:
        st.success("✅ Kursi kemungkinan laku. Disarankan untuk booking cepat!")
    else:
        st.warning("❌ Kursi kemungkinan tidak laku. Kamu bisa menunggu promo atau alternatif lain.")

# ------------------ Rekomendasi Konser ------------------ #
elif menu == "🎫 Rekomendasi Konser":
    st.title("🎫 Rekomendasi Konser (Content-Based Filtering)")

    lokasi_input = st.selectbox("Pilih Lokasi Favorit", df['Lokasi'].unique())
    seat_input = st.selectbox("Pilih Seat Favorit", df['Seat Kursi'].unique())

    feature_df = df[['Lokasi', 'Seat Kursi']].copy()
    feature_df['Lokasi'] = LabelEncoder().fit_transform(feature_df['Lokasi'])
    feature_df['Seat Kursi'] = LabelEncoder().fit_transform(feature_df['Seat Kursi'])

    input_vec = feature_df[
        (df['Lokasi'] == lokasi_input) & (df['Seat Kursi'] == seat_input)
    ].head(1)

    if input_vec.empty:
        st.warning("Kombinasi tidak ditemukan.")
    else:
        model_knn = NearestNeighbors(n_neighbors=5)
        model_knn.fit(feature_df)
        distances, indices = model_knn.kneighbors(input_vec)

        st.subheader("Konser yang Mungkin Kamu Suka:")
        rekomendasi = df.iloc[indices[0]]
        st.dataframe(rekomendasi[['Tanggal', 'Negara', 'Lokasi', 'Seat Kursi', 'Nomor Kursi', 'Harga', 'Status Kursi']])

# ------------------ Pemesanan Tiket ------------------ #
elif menu == "🛒 Pemesanan Tiket":
    st.title("🛒 Pemesanan Tiket Konser NCT Dream")

    nama = st.text_input("Masukkan Nama Anda")
    lokasi_pilih = st.selectbox("Pilih Lokasi Konser", df['Lokasi'].unique())
    tanggal_tersedia = df[df['Lokasi'] == lokasi_pilih]['Tanggal'].unique()
    if len(tanggal_tersedia) > 0:
        tanggal_pilih = st.selectbox("Pilih Tanggal", tanggal_tersedia)

        kategori_pilih = st.selectbox("Pilih Kategori Kursi", df[df['Lokasi'] == lokasi_pilih]['Seat Kursi'].unique())

        kursi_tersedia = df[(df['Lokasi'] == lokasi_pilih) & (df['Tanggal'] == tanggal_pilih) & (df['Seat Kursi'] == kategori_pilih) & (df['Status Kursi'] == "Tersedia")]

        if not kursi_tersedia.empty:
            nomor_kursi = st.selectbox("Pilih Nomor Kursi", kursi_tersedia['Nomor Kursi'])
            harga = kursi_tersedia[kursi_tersedia['Nomor Kursi'] == nomor_kursi]['Harga'].values[0]
            st.write(f"Harga: Rp{harga:,.0f}")

            metode = st.selectbox("Pilih Metode Pembayaran", ["Transfer Bank", "E-Wallet", "Kartu Kredit"])

            if st.button("Pesan Sekarang"):
                kode = str(uuid.uuid4())[:8]
                st.success(f"Pembayaran Berhasil! 🎉\n\nKode Pembelian: {kode}")
                st.session_state.riwayat.append({
                    "Nama": nama,
                    "Lokasi": lokasi_pilih,
                    "Negara": df[df['Lokasi'] == lokasi_pilih]['Negara'].values[0],
                    "Kota": df[df['Lokasi'] == lokasi_pilih]['Kota'].values[0],
                    "Tanggal": tanggal_pilih,
                    "Seat Kursi": kategori_pilih,
                    "Nomor Kursi": nomor_kursi,
                    "Harga": harga,
                    "Metode": metode,
                    "Kode": kode
                })
        else:
            st.warning("Tidak ada kursi tersedia untuk pilihan ini.")

    if st.session_state.riwayat:
        st.subheader("🧾 Riwayat Pemesanan Anda")
        st.table(pd.DataFrame(st.session_state.riwayat))

# ------------------ Riwayat Pemesanan ------------------ #
elif menu == "📜 Riwayat Pemesanan":
    st.title("📜 Riwayat Pemesanan Tiket Kamu")

    if len(st.session_state.riwayat) == 0:
        st.info("Belum ada tiket yang dipesan.")
    else:
        riwayat_df = pd.DataFrame(st.session_state.riwayat)
        st.dataframe(riwayat_df[['Nama', 'Tanggal', 'Negara', 'Lokasi', 'Kota', 'Seat Kursi', 'Nomor Kursi', 'Harga', 'Kode']])
