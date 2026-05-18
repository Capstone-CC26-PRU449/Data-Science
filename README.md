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

## Struktur Folder

```
├── data/
│   ├── raw/         # data mentah hasil unduhan
│   └── cleaned/     # output dari tiap tahap notebook
├── data_wrangling.ipynb
├── eda.ipynb
├── feature_engineering.ipynb
├── .gitignore
└── README.md
```

## Alur Notebook

### 1. Data Wrangling (`data_wrangling.ipynb`)

Gathering, assessing, dan cleaning data mentah dari kedua sumber.

- Load 5 file Excel PIHPS (per tahun) dan 1 file CSV SP2KP
- Identifikasi dan filter baris header grup (nomor romawi)
- Perbaikan format: harga sebagai string, tanggal ada spasi, format wide
- Konversi ke long format, interpolasi missing values per komoditas
- Flag outlier dengan IQR — tidak dihapus, dijadikan penanda

Output: `pihps_cleaned.csv`, `sp2kp_cleaned.csv`

### 2. EDA (`eda.ipynb`)

Eksplorasi data untuk memahami karakteristik harga tiap kelompok komoditas.

- Tren harga per kelompok komoditas dari 2022 ke 2026
- Pola musiman: dampak Ramadan dan Lebaran terhadap harga
- Distribusi dan volatilitas antar komoditas
- Korelasi antar komoditas dalam satu kelompok

### 3. Feature Engineering (`feature_engineering.ipynb`)

Penambahan fitur eksogen ke data PIHPS sebagai input model prediksi.

- `is_holiday` — hari libur nasional dan cuti bersama (PP + SKB 3 Menteri)
- `is_ramadan` — dalam periode Ramadan 1443H–1447H
- `days_to_lebaran` — selisih hari ke Idul Fitri terdekat (negatif = sebelum)
- `suhu_rata2`, `curah_hujan`, `kecepatan_angin` — cuaca harian Jakarta dari Open-Meteo API

Output: `pihps_featured.csv`

## Output Data

| File | Baris | Keterangan |
|------|-------|------------|
| `data/cleaned/pihps_cleaned.csv` | 23.709 | Data nasional harian Jan 2022 - Apr 2026 |
| `data/cleaned/sp2kp_cleaned.csv` | 456.590 | Data per kabupaten Jan - Apr 2026 |
| `data/cleaned/pihps_featured.csv` | 23.709 | pihps_cleaned + fitur kalender dan cuaca |

Kolom `pihps_featured.csv`: `Komoditas`, `tanggal`, `harga`, `sumber`, `is_outlier`, `is_holiday`, `is_ramadan`, `days_to_lebaran`, `suhu_rata2`, `curah_hujan`, `kecepatan_angin`

Saat load, gunakan `parse_dates=['tanggal']` agar kolom tanggal terbaca sebagai datetime.

---
