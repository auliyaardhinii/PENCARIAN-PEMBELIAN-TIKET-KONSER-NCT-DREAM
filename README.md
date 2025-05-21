# PENCARIAN & PEMBELIAN TIKET KONSER NCT DREAM

## 1.	Deskripsi Aplikasi
NCT Dream Concert App adalah aplikasi berbasis streamlit yang dirancang untuk memudahkan penggemar NCT DREAM dalam mendapatkan tiket konser secara online. Perancangan aplikasi memanfaatkan pendekatan data science yang terdiri dari supervised classification, content-based filtering, dan exploratory data analysis (EDA). Aplikasi ini juga dilengkapi dengan berbagai fitur yang menarik, diantaranya sebagai berikut:

## 2.	Fitur Utama:
1.	Visualisasi Data Konser
Menampilkan analisis konser seperti jumlah konser per negara dalam bentuk grafik interaktif.
2.	Prediksi Kursi Laku atau Tidak
Memprediksi apakah kursi akan terjual berdasarkan lokasi, harga, dan jenis seat dengan bantuan machine learning.
3.	Rekomendasi Konser Pribadi
Memberikan saran konser berdasarkan preferensi pengguna (lokasi & seat favorit), lengkap dengan jadwal, harga, dan status ketersediaan.
4.	Pemesanan Tiket Interaktif
Pengguna dapat memilih tanggal konser, lokasi, jenis seat, dan nomor kursi. Harga otomatis ditampilkan berdasarkan pilihan. Tersedia metode pembayaran melalui e-wallet atau kartu kredit.
5.	Riwayat Pemesanan Otomatis
Menampilkan daftar riwayat pembelian tiket secara real-time sebagai referensi dan bukti transaksi.

## 3.	Cara Install
1.	Pastikan perangkat Anda sudah memiliki Python dan Anaconda versi terbaru.
2.	Buka terminal atau Anaconda Prompt, lalu jalankan perintah berikut untuk menginstal Streamlit: pip install streamlit
3.	Setelah proses instalasi selesai, tambahkan file APLIKASI PENCARIAN DAN PEMBELIAN KONSER NCT DREAM.py yang berisi kode perancangan aplikasi ke dalam satu folder khusus.

## 4.	Cara menjalankan
1.	Buka VS Code atau editor Python lainnya, lalu jalankan keseluruhan kode dalam file konseryes.py.
2.	Simpan file tersebut di folder yang diinginkan, seperti: C:\Users\User\Downloads\APLIKASI PENCARIAN DAN PEMBELIAN KONSER NCT DREAM.py
3.	Buka terminal dan jalankan perintah
streamlit run C:\Users\User\Downloads\APLIKASI PENCARIAN DAN PEMBELIAN KONSER NCT DREAM.py
4.	Setelah berhasil dan tidak ada error, maka akan muncul permintaan untuk menambahkan email aktif secara otomatis pada terminal.
5.	Setelah email, diverifikasi browser akan otomatis membuka alamat localhost untuk menampilkan aplikasi pembelian tiket konser NCT dream
6.	Aplikasi pemesanan tiket konser NCT dream kini sudah bisa digunakan melalui localhost.
   
## 5.	Tampilan Aplikasi
 ![Screenshot (799)](https://github.com/user-attachments/assets/f7773438-7c0f-48de-a6e3-2632ea783688)

## 6.	Website Aplikasi pemesanan Tiket Konser NCT Dream:
https://sellkonsernctdream.streamlit.app/

## 7. Kesimpulan Model dan Teknik yang digunakan

| Fitur Aplikasi          | Teknik Data Science                               | Tujuan                                       |
| ----------------------- | ------------------------------------------------- | -------------------------------------------- |
| Visualisasi Data Konser | EDA & Visualisasi Interaktif (Bar Chart, Boxplot) | membantu pengguna memahami pola umum dan tren konser yang tersedia. Teknik ini termasuk dalam proses EDA (Exploratory Data Analysis) yang penting dalam mempersiapkan dan mengenali data sebelum dilakukan pemodelan machine learning.              |
| Prediksi Kursi          | Supervised Classification (Random Forest)         | membantu pengguna mengambil keputusan pembelian secara strategis, misalnya apakah sebaiknya langsung membeli kursi tersebut atau menunggu diskon/promosi.                 |
| Rekomendasi Konser      | Content-Based Filtering (KNN)                     | Aplikasi akan mencari konser-konser serupa dengan menggunakan algoritma content-based filtering dan K-Nearest Neighbors (KNN). Fitur ini memungkinkan pengguna menemukan konser yang cocok dengan minatnya, sekaligus melihat informasi detail seperti tanggal, harga, dan status ketersediaan kursi.                                                                                        |
| Pemesanan Tiket         | Logika Interaktif + Simulasi UI                   | Dengan antarmuka yang interaktif, pengguna dapat merasakan pengalaman seperti memesan tiket di platform resmi, namun dengan tambahan fitur pintar yang membantu pengambilan keputusan.
| Riwayat Pemesanan       | Session State / Simulasi Database                 | berguna untuk tracking pembelian, sebagai bukti transaksi, dan sebagai referensi jika ingin membeli tiket konser serupa di masa depan.                                    |



