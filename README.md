# Pantau Pasar - Data Science

Bagian ini mencakup seluruh proses data hingga feature engineering untuk proyek Pantau Pasar, sebuah sistem pemantauan dan prediksi harga pangan strategis di Indonesia.

## Sumber Data

Data dikumpulkan dari dua sumber utama:

**PIHPS Nasional (hargapangan.id)**
- Cakupan: seluruh provinsi (agregat nasional)
- Periode: Januari 2022 sampai April 2026
- Komoditas: 21 jenis bahan pangan (beras, cabai, bawang, daging, telur, minyak goreng, gula)
- Tipe laporan: harian, pasar tradisional

**SP2KP Kemendag (sp2kp.kemendag.go.id)**
- Cakupan: 514 kabupaten/kota
- Periode: Januari 2026 sampai April 2026
- Komoditas: 17 jenis bahan pangan

## Struktur Folder & Pipeline Data

```
├── data/
│   ├── raw/                             # Data mentah hasil unduhan (PIHPS & SP2KP)
│   └── cleaned/                         # Dataset bersih siap pakai (output pengelolaan data)
├── notebook/                            # Notebook alur pemrosesan data (pipeline)
│   ├── data_wrangling.ipynb             # Tahap 1: Gathering, assessing, dan cleaning data
│   ├── eda.ipynb                        # Tahap 2: Exploratory Data Analysis (EDA) & pengelompokan
│   ├── feature_engineering.ipynb        # Tahap 3: Rekayasa fitur kalender dan cuaca (Open-Meteo API)
│   ├── data_visualization_and_explanatory.ipynb  # Tahap 4: Visualisasi data & analisis eksplanatori bisnis
│   └── gambaran_preprosessData.ipynb    # Tahap 5: Desain prapemrosesan lanjut & persiapan training model
├── .gitignore
├── requirements.txt
└── README.md
```

## Laporan Alur Pengelolaan Data (Data Pipeline)

Proses pengelolaan data dirancang secara terstruktur dan bertahap untuk memastikan kualitas data yang tinggi serta kesiapan fitur sebelum masuk ke tahap pemodelan prediktif. Berikut adalah penjelasan ringkas fungsi dan kegunaan masing-masing tahapan:

### 1. Integrasi & Pembersihan Data (`data_wrangling.ipynb`)
**Kegunaan**: Menyaring dan menyatukan data mentah dari dua sumber (PIHPS Nasional dan SP2KP Kemendag) ke dalam format standar yang siap dianalisis.
* **Proses Utama**:
  * Pengumpulan (gathering) data 5 file Excel PIHPS dan 1 file CSV SP2KP.
  * Pembersihan (cleaning) noise seperti baris header kelompok (angka romawi), perbaikan tipe data harga dan spasi pada tanggal.
  * Restrukturisasi dari format *wide* ke format *long* (berurutan waktu).
  * Penanganan *missing values* melalui interpolasi per komoditas dan pelabelan *outlier* dengan metode IQR.
* **Output**: `pihps_cleaned.csv` dan `sp2kp_cleaned.csv`

### 2. Eksplorasi & Analisis Kelompok (`eda.ipynb`)
**Kegunaan**: Memahami perilaku historis harga komoditas dan menentukan strategi pemodelan yang optimal.
* **Proses Utama**:
  * Analisis tren harga historis komoditas pangan dari tahun 2022 hingga 2026.
  * Identifikasi pola musiman (efek Ramadan/Lebaran) terhadap volatilitas harga.
  * Pengujian korelasi antar-komoditas. Ditemukan bahwa komoditas dalam satu kelompok (misalnya varian cabai) memiliki korelasi sangat tinggi (>0.95), sehingga lebih efisien jika dimodelkan per kelompok komoditas daripada per komoditas tunggal.
  * Pembagian 21 komoditas ke dalam 6 kelompok strategis: Beras, Cabai, Daging & Telur, Bawang, Minyak Goreng, dan Gula.

### 3. Rekayasa Fitur Eksogen (`feature_engineering.ipynb`)
**Kegunaan**: Memperkaya dataset dengan menambahkan konteks waktu (kalender) dan kondisi lingkungan (cuaca) untuk meningkatkan akurasi prediksi model.
* **Proses Utama**:
  * Penambahan fitur kalender: `is_holiday` (hari libur nasional/cuti bersama), `is_ramadan` (periode Ramadan), dan `days_to_lebaran` (jarak hari ke Idul Fitri terdekat).
  * Penambahan fitur cuaca harian Jakarta (suhu rata-rata, curah hujan, kecepatan angin) yang diintegrasikan secara otomatis melalui Open-Meteo API.
* **Output**: `pihps_featured.csv` (data historis lengkap dengan 11 kolom fitur eksternal).

### 4. Analisis Eksplanatori & Visualisasi Bisnis (`data_visualization_and_explanatory.ipynb`)
**Kegunaan**: Menyediakan visualisasi dan jawaban konkret atas pertanyaan bisnis utama guna membantu proses pengambilan keputusan strategis.
* **Fokus Analisis**:
  * Pertumbuhan harga secara Year-on-Year (YoY) untuk komoditas Beras dan Daging Sapi.
  * Penentuan komoditas yang paling volatil dan paling stabil menggunakan *Coefficient of Variation* (CV).
  * Analisis dampak Ramadan terhadap kenaikan harga komoditas pangan tertentu.
  * Analisis korelasi antara curah hujan dengan fluktuasi harga cabai dan bawang merah.

### 5. Konsep Prapemrosesan Lanjut & Persiapan Model (`gambaran_preprosessData.ipynb`)
**Kegunaan**: Menjembatani data pipeline dengan mesin pemodelan (Machine Learning) agar siap ditraining tanpa mengalami kebocoran data (*data leakage*).
* **Proses Utama**:
  * **Feature Encoding**: Mengubah kategori string komoditas menjadi kode numerik (`komoditas_encoded`) agar model dapat membedakan antar-varian dalam satu kelompok.
  * **Lag & Rolling Features**: Pembuatan fitur berbasis waktu seperti harga masa lalu (`harga_lag_1` s/d `harga_lag_30`) dan tren rata-rata bergerak (`rolling_mean_7` s/d `rolling_mean_30`) dengan teknik `groupby('Komoditas')` untuk mencegah kebocoran data.
  * **Time-based Train/Test Split**: Pembagian data latih (train) dan uji (test) secara kronologis waktu (bukan acak), dengan menyisihkan 3 bulan terakhir sebagai data uji untuk simulasi prediksi masa depan yang realistis.
  * **Multi-step Forecasting**: Konsep pergeseran target (*target shift*) untuk memprediksi harga komoditas dalam jangka waktu tertentu ke depan (misalnya horizon 7 hari).

## Output Data

| File | Baris | Keterangan |
|------|-------|------------|
| `data/cleaned/pihps_cleaned.csv` | 23.709 | Data nasional harian Jan 2022 - Apr 2026 |
| `data/cleaned/sp2kp_cleaned.csv` | 456.590 | Data per kabupaten Jan - Apr 2026 |
| `data/cleaned/pihps_featured.csv` | 23.709 | pihps_cleaned + fitur kalender dan cuaca |

Kolom `pihps_featured.csv`: `Komoditas`, `tanggal`, `harga`, `sumber`, `is_outlier`, `is_holiday`, `is_ramadan`, `days_to_lebaran`, `suhu_rata2`, `curah_hujan`, `kecepatan_angin`

Saat load, gunakan `parse_dates=['tanggal']` agar kolom tanggal terbaca sebagai datetime.

---
