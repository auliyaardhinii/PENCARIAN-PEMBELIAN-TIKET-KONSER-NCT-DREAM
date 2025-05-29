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
menu = st.sidebar.radio(" ", ["🧠 Prediksi Kursi", "🌻 Rekomendasi Konser", "🛒 Pemesanan Tiket", "📜 Riwayat Pemesanan", "📊 EDA & Visualisasi"])

# ------------------ Prediksi Kursi ------------------ #
if menu == "🧠 Prediksi Kursi":
    st.title("🧠 Prediksi Kursi Laku atau Tidak")
    
    # Tambahkan gambar di sini
    st.image("660b7f8281215-tiket-konser-tds-3-nct-dream_1265_711.jpg", caption="🎫 Kursi Konser", use_column_width=True)
    
    df_pred = df.copy()
    # Ubah status kursi ke 0 dan 1
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

    st.subheader("Coba Prediksi Sendiri:")
    negara = st.selectbox("Negara", df['Negara'].unique())
    seat = st.selectbox("Seat Kursi", df['Seat Kursi'].unique())
    lokasi = st.selectbox("Lokasi", df['Lokasi'].unique())
    kota = st.selectbox("Kota", df['Kota'].unique())

    # Deteksi harga otomatis berdasarkan kombinasi input
    harga_terkait = df[
        (df['Negara'] == negara) &
        (df['Seat Kursi'] == seat) &
        (df['Lokasi'] == lokasi) &
        (df['Kota'] == kota)
    ]['Harga']

    if not harga_terkait.empty:
        harga_otomatis = int(harga_terkait.median())
    else:
        harga_otomatis = int(df['Harga'].median())

    st.number_input("Harga (otomatis terdeteksi)", value=harga_otomatis, disabled=True)

    input_data = pd.DataFrame([[
        encoders['Negara'].transform([negara])[0],
        encoders['Seat Kursi'].transform([seat])[0],
        harga_otomatis,
        encoders['Lokasi'].transform([lokasi])[0],
        encoders['Kota'].transform([kota])[0]
    ]], columns=X.columns)

    hasil = model.predict(input_data)[0]
    if hasil == 1:
        st.success("✅ Kursi Tersedia. Disarankan untuk booking cepat!")
    else:
        st.warning("❌ Tidak ada kursi yang tersedia. Silahkan pilih kursi yang tersedia atau alternatif lain.")

# ------------------ Rekomendasi Konser ------------------ #
if menu == "🌻 Rekomendasi Konser":
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
if menu == "🛒 Pemesanan Tiket":
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
if menu == "📜 Riwayat Pemesanan":
    st.title("📜 Riwayat Pemesanan Tiket Kamu")

    if len(st.session_state.riwayat) == 0:
        st.info("Belum ada tiket yang dipesan.")
    else:
        riwayat_df = pd.DataFrame(st.session_state.riwayat)
        st.dataframe(riwayat_df[['Nama', 'Tanggal', 'Negara', 'Lokasi', 'Kota', 'Seat Kursi', 'Nomor Kursi', 'Harga', 'Kode']])

# ------------------ EDA & Visualisasi ------------------ #
if menu == "📊 EDA & Visualisasi":
    st.title("📊 EDA dan Visualisasi")

    st.subheader("Jumlah Konser per Negara")
    negara_count = df['Negara'].value_counts()
    st.bar_chart(negara_count)
    st.markdown(f"**Insight:** Negara dengan konser terbanyak adalah **{negara_count.idxmax()}**, menunjukkan kemungkinan basis fans yang besar atau infrastruktur konser yang baik di negara tersebut. Negara lain dengan konser lebih sedikit mungkin bisa menjadi potensi pasar baru.")

    st.subheader("Kategori Kursi Paling Sering Tersedia / Tidak")
    kursi_status = df.groupby(['Seat Kursi', 'Status Kursi']).size().unstack()
    st.bar_chart(kursi_status)
    st.markdown("**Insight:** Grafik ini membantu mengidentifikasi kategori kursi mana yang paling cepat terjual atau sering tidak terjual. Kursi dengan tingkat keterisian tinggi menunjukkan popularitas dan potensi keuntungan lebih besar.")

    st.subheader("Harga Kursi vs Status Kursi")
    fig, ax = plt.subplots()
    sns.boxplot(x='Status Kursi', y='Harga', data=df, ax=ax)
    ax.set_title("Perbandingan Harga Kursi Berdasarkan Status")
    ax.set_xlabel("Status Kursi")
    ax.set_ylabel("Harga")
    st.pyplot(fig)
    with st.expander("📌 Insight"):
        st.markdown("Harga kursi yang tidak laku cenderung lebih tinggi dari yang laku. Ini menunjukkan bahwa penetapan harga sangat mempengaruhi keputusan pembelian. Penyelenggara bisa mempertimbangkan strategi diskon atau paket bundling untuk kategori harga tinggi.")

    st.subheader("Distribusi Nomor Kursi Berdasarkan Negara")
    negara_pilihan = st.selectbox("Pilih Negara", df['Negara'].unique())
    df_filtered = df[df['Negara'] == negara_pilihan]
    distribusi_kursi = df_filtered.groupby(['Seat Kursi', 'Nomor Kursi']).size().reset_index(name='Total')
    st.dataframe(distribusi_kursi.sort_values(by='Total', ascending=False))
    st.markdown("**Insight:** Distribusi ini menunjukkan preferensi penonton terhadap nomor kursi tertentu di setiap kategori kursi. Nomor kursi dengan total tinggi kemungkinan besar berada di posisi strategis dengan visibilitas panggung yang baik.")

    st.subheader("Korelasi Antar Faktor Numerik")
    df_corr = df.copy()
    df_corr['Status Kursi'] = df_corr['Status Kursi'].apply(lambda x: 0 if x == "Tersedia" else 1)
    df_corr = df_corr[['Harga', 'Status Kursi']]
    corr_matrix = df_corr.corr()
    fig_corr, ax_corr = plt.subplots()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax_corr)
    st.pyplot(fig_corr)
    st.markdown("**Insight:** Korelasi negatif antara harga dan status kursi menunjukkan bahwa semakin tinggi harga, semakin kecil kemungkinan kursi tersebut laku. Hal ini dapat dijadikan pertimbangan untuk segmentasi harga dan promosi.")
