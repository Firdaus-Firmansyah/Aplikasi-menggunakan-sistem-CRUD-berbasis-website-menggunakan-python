# Aplikasi-menggunakan-sistem-CRUD-berbasis-website-menggunakan-python
Web Warung Toko Kasir 🛒
Aplikasi kasir sederhana berbasis web yang dibangun menggunakan Flask dan SQLite. Aplikasi ini memungkinkan pengguna untuk mengelola produk, melakukan transaksi penjualan, dan melihat riwayat transaksi.

Fitur Aplikasi
Manajemen Produk
Tambah produk baru.
Perbarui informasi produk (stok, harga, dll).
Hapus produk dari daftar.

Transaksi Penjualan
Tambahkan produk ke keranjang belanja.
Hitung total harga secara otomatis.
Selesaikan transaksi dengan metode pembayaran Tunai (Cash).

Riwayat Transaksi
Tampilkan daftar transaksi yang sudah diselesaikan.
Menyimpan waktu transaksi secara otomatis.

Teknologi yang Digunakan
Python (Flask framework)
HTML/CSS (Frontend)
SQLite (Database)
Jinja2 (Template engine Flask)

Persyaratan Sistem
Python 3.8 atau lebih tinggi
Paket/pustaka Python tambahan:
Flask
SQLite3

Langkah Instalasi dan Menjalankan Aplikasi
Ikuti langkah-langkah berikut untuk menjalankan proyek di komputer Anda:

1. Clone Repository
Salin repository ini ke komputer Anda menggunakan git clone.
git clone https://github.com/username/nama-repo-kasir.git
cd nama-repo-kasir

2. Buat Virtual Environment
Untuk menghindari konflik dependensi, gunakan virtual environment.
python -m venv venv
source venv/bin/activate    # Untuk Linux/macOS
venv\Scripts\activate       # Untuk Windows

3. Install Dependencies
Instal semua pustaka Python yang diperlukan.
pip install -r requirements.txt

Jika file requirements.txt belum ada, Anda bisa membuatnya dengan menjalankan:
pip freeze > requirements.txt

4. Siapkan Database
Buat file database store.db dan jalankan skrip inisialisasi database:
python -c "from app import init_db; init_db()"
Penjelasan:
Fungsi init_db() akan membuat tabel-tabel yang diperlukan (products, users, transactions) di database SQLite.

5. Jalankan Aplikasi Flask
Jalankan aplikasi dengan perintah berikut:
python app.py

Aplikasi akan berjalan di http://127.0.0.1:5000. Anda bisa mengaksesnya melalui browser.


Berikut adalah contoh file README.md yang lengkap dan informatif untuk proyek aplikasi kasir Anda. File ini mencakup deskripsi, fitur, langkah-langkah instalasi, penggunaan, serta cara menjalankan proyek.

Web Warung Toko Kasir 🛒
Aplikasi kasir sederhana berbasis web yang dibangun menggunakan Flask dan SQLite. Aplikasi ini memungkinkan pengguna untuk mengelola produk, melakukan transaksi penjualan, dan melihat riwayat transaksi.

Fitur Aplikasi
Manajemen Produk

Tambah produk baru.
Perbarui informasi produk (stok, harga, dll).
Hapus produk dari daftar.
Transaksi Penjualan

Tambahkan produk ke keranjang belanja.
Hitung total harga secara otomatis.
Selesaikan transaksi dengan metode pembayaran Tunai (Cash).
Riwayat Transaksi

Tampilkan daftar transaksi yang sudah diselesaikan.
Menyimpan waktu transaksi secara otomatis.
Teknologi yang Digunakan
Python (Flask framework)
HTML/CSS (Frontend)
SQLite (Database)
Jinja2 (Template engine Flask)
Persyaratan Sistem
Python 3.8 atau lebih tinggi
Paket/pustaka Python tambahan:
Flask
SQLite3
Langkah Instalasi dan Menjalankan Aplikasi
Ikuti langkah-langkah berikut untuk menjalankan proyek di komputer Anda:

1. Clone Repository
Salin repository ini ke komputer Anda menggunakan git clone.

bash
Copy code
git clone https://github.com/username/nama-repo-kasir.git
cd nama-repo-kasir
2. Buat Virtual Environment
Untuk menghindari konflik dependensi, gunakan virtual environment.

bash
Copy code
python -m venv venv
source venv/bin/activate    # Untuk Linux/macOS
venv\Scripts\activate       # Untuk Windows
3. Install Dependencies
Instal semua pustaka Python yang diperlukan.

bash
Copy code
pip install -r requirements.txt
Jika file requirements.txt belum ada, Anda bisa membuatnya dengan menjalankan:

bash
Copy code
pip freeze > requirements.txt
4. Siapkan Database
Buat file database store.db dan jalankan skrip inisialisasi database:

python
Copy code
python -c "from app import init_db; init_db()"
Penjelasan:
Fungsi init_db() akan membuat tabel-tabel yang diperlukan (products, users, transactions) di database SQLite.

5. Jalankan Aplikasi Flask
Jalankan aplikasi dengan perintah berikut:

bash
Copy code
python app.py
Aplikasi akan berjalan di http://127.0.0.1:5000. Anda bisa mengaksesnya melalui browser.

Struktur Proyek
nama-repo-kasir/
│
├── app.py                  # Main file Flask
├── store.db                # SQLite Database
├── requirements.txt        # File dependencies
│
├── static/                 
│   ├── style.css           # File CSS
│   └── style2.css          
│
├── templates/              # Folder HTML Templates
│   ├── add_product.html    
│   ├── checkout.html       
│   ├── transactions.html   
│   ├── start_transaction.html
│   ├── dashboard.html
│   ├── login.html
│   └── ... (file lainnya)
│
└── README.md               # Dokumentasi proyek


Cara Penggunaan
1. Login ke Aplikasi
Default login:
Username: admin
Password: admin123
2. Manajemen Produk
Tambahkan produk melalui halaman Tambah Produk.
Lihat daftar produk di halaman Produk.
Edit atau hapus produk sesuai kebutuhan.
3. Transaksi Penjualan
Tambahkan produk ke keranjang belanja dari halaman Transaksi Baru.
Lakukan Checkout dan pilih metode pembayaran Tunai (Cash).
4. Melihat Riwayat Transaksi
Riwayat transaksi dapat dilihat pada halaman Riwayat Transaksi.

Kontak
Jika ada pertanyaan atau masalah terkait proyek ini, silakan hubungi saya:

Instagram: @daussauruss
Email: firdifirdaus19@gmail.com
GitHub: https://github.com/Firdaus-Firmansyah
