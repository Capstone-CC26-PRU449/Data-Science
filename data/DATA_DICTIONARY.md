# Kamus Data (Data Dictionary) - Pantau Pasar

Kamus data ini memberikan gambaran lengkap mengenai dataset yang digunakan dalam proyek **Pantau Pasar**, baik data mentah hasil unduhan (`data/raw/`) maupun data bersih hasil wrangling dan rekayasa fitur (`data/cleaned/`).

---

## 1. Sumber Data & Informasi Umum

Data yang digunakan dikumpulkan dari dua portal pemantauan harga pangan resmi di Indonesia:
1. **PIHPS Nasional (Pusat Informasi Harga Pangan Strategis Nasional - hargapangan.id)**:
   * **Cakupan**: Rata-rata nasional agregat (harian).
   * **Periode**: Januari 2022 s/d April 2026.
   * **Komoditas**: 21 jenis sub-komoditas bahan pangan strategis (seperti beras, cabai, bawang, daging, telur, minyak goreng, gula).
2. **SP2KP Kemendag (Sistem Pemantauan Pasar dan Kebutuhan Pokok - sp2kp.kemendag.go.id)**:
   * **Cakupan**: 514 Kabupaten/Kota di 38 Provinsi (harian).
   * **Periode**: Januari 2026 s/d April 2026.
   * **Komoditas**: 17 jenis komoditas bahan pangan pokok.

---

## 2. Struktur Direktori Data

```
data/
├── raw/                      # Berkas data mentah hasil unduhan
│   ├── Tabel Harga Berdasarkan Daerah_2022.xlsx
│   ├── Tabel Harga Berdasarkan Daerah_2023.xlsx
│   ├── Tabel Harga Berdasarkan Daerah_2024.xlsx
│   ├── Tabel Harga Berdasarkan Daerah_2025.xlsx
│   ├── Tabel Harga Berdasarkan Daerah_2026_jan-apr.xlsx
│   ├── Tabel Harga Berdasarkan Komoditas.xlsx
│   └── Tabulasi SP2KP.csv
└── cleaned/                  # Berkas hasil cleaning & feature engineering
    ├── pihps_cleaned.csv     # Data PIHPS Nasional ter-wrangling (Long format)
    ├── pihps_featured.csv    # pihps_cleaned + fitur cuaca & kalender
    └── sp2kp_cleaned.csv     # Data SP2KP Kabupaten/Kota ter-wrangling (Long format)
```

---

## 3. Spesifikasi Data Mentah (Raw Data Dictionary)

Semua data mentah disimpan dalam format **Wide**, di mana kolom-kolom sebelah kanan merepresentasikan tanggal pencatatan harga harian.

### A. Tabel Harga Berdasarkan Daerah_[Tahun].xlsx (PIHPS)
* **Deskripsi**: Data perkembangan harga harian tingkat Nasional (agregat) per tahun. Meskipun terdapat kata "Daerah" pada nama berkas, isinya adalah rata-rata harga nasional untuk komoditas pangan.
* **Format**: Excel (`.xlsx`), Wide format.
* **Dimensi**: 31 baris x ~262 kolom per tahun (kolom tanggal bervariasi tergantung hari kerja).
* **Kolom Utama**:
  * `No` (Text): Nomor baris komoditas (menggunakan angka romawi `I` s/d `X` untuk nama komoditas utama/grup, dan angka biasa `1` s/d `21` untuk sub-komoditas eceran).
  * `Komoditas (Rp)` (Text): Nama bahan pangan pokok dan satuannya.
  * `[Tanggal]` (Text): Kolom tanggal pencatatan (format: `DD/ MM/ YYYY` dengan whitespace). Berisi harga dalam bentuk string (contoh: `"11,750"`) atau tanda `"-"` untuk hari libur/kosong.

### B. Tabel Harga Berdasarkan Komoditas.xlsx (PIHPS Regional)
* **Deskripsi**: Data rata-rata harga harian per provinsi tahun 2022. *Catatan: Tidak aktif digunakan dalam alur modeling utama saat ini.*
* **Format**: Excel (`.xlsx`), Wide format.
* **Dimensi**: 35 baris (Provinsi) x 262 kolom.
* **Kolom Utama**:
  * `No` (Text): Indeks Romawi.
  * `Komoditas (Rp)` (Text): Nama wilayah/provinsi (misal: "Semua Provinsi", "Aceh", "Sumatera Utara").
  * `[Tanggal]` (Text): Kolom tanggal eceran.

### C. Tabulasi SP2KP.csv (SP2KP)
* **Deskripsi**: Data eceran harian tingkat kabupaten/kota di seluruh Indonesia (Januari - April 2026).
* **Format**: Tab-separated CSV, Encoding UTF-16.
* **Dimensi**: 7.830 baris x 65 kolom.
* **Kolom Utama**:
  * `cekNo` (Float): ID indeks baris data mentah.
  * `Kode Wilayah` (Integer): Kode administratif wilayah BPS (4 digit).
  * `Provinsi` (Text): Nama Provinsi.
  * `Kabupaten Kota` (Text): Nama Kabupaten/Kota.
  * `Komoditas ` (Text): Nama komoditas pangan pokok (17 jenis).
  * `HET/HA ` (Float): Harga Eceran Tertinggi atau Harga Acuan Pemerintah (dalam satuan ribuan, contoh: `41.5` untuk Rp41.500).
  * `[Tanggal]` (Float): Kolom tanggal transaksi (contoh: `02/01/2026`).

---

## 4. Spesifikasi Data Bersih (Cleaned & Featured Data Dictionary)

Semua data bersih telah dikonversi menjadi format **Long** (kolom tanggal dilebur menjadi satu baris per tanggal), sehingga ramah untuk visualisasi dan input model machine learning.

### A. pihps_cleaned.csv
* **Deskripsi**: Data PIHPS Nasional yang telah dibersihkan, di-melt menjadi format Long, dan ditangani missing value-nya.
* **Dimensi**: 23.709 baris x 5 kolom.
* **Kamus Kolom**:

| Nama Kolom | Tipe Data | Deskripsi | Contoh Nilai |
| :--- | :--- | :--- | :--- |
| `Komoditas` | String | Nama sub-komoditas bahan pangan strategis (21 jenis unik). | `Beras Kualitas Medium I` |
| `tanggal` | Date | Tanggal pencatatan harga (format `YYYY-MM-DD`). | `2022-01-03` |
| `harga` | Float | Rata-rata harga eceran nasional per kilogram dalam Rupiah. | `11750.0` |
| `sumber` | String | Sumber data pangan, bernilai konstan `'PIHPS'`. | `PIHPS` |
| `is_outlier` | Boolean | Penanda apakah harga pada tanggal tersebut merupakan pencilan (IQR > 1.5). | `False` |

---

### B. pihps_featured.csv
* **Deskripsi**: Data bersih PIHPS (`pihps_cleaned.csv`) yang telah ditambahkan fitur-fitur eksternal seperti kalender hari libur, periode keagamaan (Ramadan/Lebaran), serta kondisi cuaca harian DKI Jakarta.
* **Dimensi**: 23.709 baris x 11 kolom.
* **Kamus Kolom**:

| Nama Kolom | Tipe Data | Deskripsi | Contoh Nilai |
| :--- | :--- | :--- | :--- |
| `Komoditas` | String | Nama sub-komoditas pangan (21 jenis). | `Cabai Rawit Merah` |
| `tanggal` | Date | Tanggal pencatatan harga (format `YYYY-MM-DD`). | `2022-01-03` |
| `harga` | Float | Harga eceran nasional (Rupiah/kg). | `45000.0` |
| `sumber` | String | Sumber data pangan, bernilai konstan `'PIHPS'`. | `PIHPS` |
| `is_outlier` | Boolean | Flag outlier harga berdasarkan metode IQR per komoditas. | `False` |
| `is_holiday` | Binary (0/1) | Flag penanda hari libur nasional atau cuti bersama resmi pemerintah. | `0` |
| `is_ramadan` | Binary (0/1) | Flag penanda apakah tanggal tersebut berada pada bulan suci Ramadan. | `0` |
| `days_to_lebaran`| Integer | Selisih hari ke Hari Raya Idul Fitri terdekat (negatif = sebelum, positif = sesudah). | `-119` |
| `suhu_rata2` | Float | Suhu harian rata-rata di wilayah Jakarta (°C) dari Open-Meteo API. | `27.4` |
| `curah_hujan` | Float | Jumlah curah hujan harian di wilayah Jakarta (mm) dari Open-Meteo API. | `0.5` |
| `kecepatan_angin`| Float | Rata-rata kecepatan angin harian di Jakarta (km/jam) dari Open-Meteo API. | `10.6` |

---

### C. sp2kp_cleaned.csv
* **Deskripsi**: Data harga tingkat Kabupaten/Kota se-Indonesia dari SP2KP yang telah dibersihkan, di-melt menjadi format Long, disatukan satuan harganya ke Rupiah utuh, dan diurutkan.
* **Dimensi**: 456.590 baris x 9 kolom.
* **Kamus Kolom**:

| Nama Kolom | Tipe Data | Deskripsi | Contoh Nilai |
| :--- | :--- | :--- | :--- |
| `no` | Float | Nomor indeks baris dari berkas data mentah. | `62.0` |
| `kode_wilayah` | Integer | Kode administratif kabupaten/kota resmi BPS (4 digit). | `1105` |
| `provinsi` | String | Nama Provinsi (38 Provinsi unik di Indonesia). | `Aceh` |
| `kabupaten_kota` | String | Nama Kabupaten atau Kota (514 Kab/Kota unik). | `Kab. Aceh Barat` |
| `komoditas` | String | Nama komoditas bahan pangan pokok (17 jenis unik). | `Bawang Merah` |
| `hetha` | Float | Harga Eceran Tertinggi (HET) atau Harga Acuan (HA) dalam **Rupiah Utuh**. | `41500.0` |
| `tanggal` | Date | Tanggal pencatatan transaksi harga (format `YYYY-MM-DD`). | `2026-01-02` |
| `harga` | Float | Harga eceran komoditas di tingkat pasar lokal dalam **Rupiah Utuh**. | `50000.0` |
| `sumber` | String | Sumber data pangan, bernilai konstan `'SP2KP'`. | `SP2KP` |

---

## 5. Penjelasan Khusus Kolom & Regulasi Data

### 5.1 Kesetaraan Unit `harga` dan `hetha`
> [!IMPORTANT]
> Pada data awal SP2KP (`Tabulasi SP2KP.csv`), kolom `HET/HA` ditulis dalam skala ribuan (misal: `41.5`), sementara kolom harga tanggal ditulis dalam Rupiah utuh (misal: `50000`).
> * **Tindakan Perbaikan**: Kode wrangling telah direvisi untuk mengalikan kolom `hetha` dengan `1000`.
> * **Kondisi Saat Ini**: Di dalam berkas `sp2kp_cleaned.csv`, baik kolom `harga` maupun `hetha` **keduanya telah menggunakan satuan Rupiah Utuh**. Perbandingan selisih harga pasar terhadap harga acuan pemerintah kini dapat dihitung secara langsung tanpa perlu konversi tambahan (misal: `harga - hetha`).

### 5.2 Penjelasan Ketiadaan Data HET/HA (100% Null)
Beberapa komoditas di dalam data SP2KP memiliki nilai `hetha` yang bernilai **kosong (Null/NaN) secara keseluruhan (100% Null)**, yaitu:
1. `Cabai Merah Besar`
2. `Garam Halus`
3. `Ikan Kembung`
4. `Minyak Goreng Sawit Curah`
5. `Minyak Goreng Sawit Kemasan Premium`
6. `Tepung Terigu`

> [!NOTE]
> **Konteks Kebijakan**: Nilai kosong ini mencerminkan bahwa selama periode Januari - April 2026, Pemerintah RI (Kementerian Perdagangan / Badan Pangan Nasional) **tidak menetapkan atau tidak memberlakukan batas harga acuan (HET/HA) resmi** eceran untuk komoditas-komoditas tersebut. Ketiadaan data ini bersifat valid berdasarkan kondisi regulasi riil di lapangan.

### 5.3 Regulasi Zonasi HET Beras di Indonesia
Khusus untuk komoditas **Beras Medium** dan **Beras Premium**, pemerintah membagi tarif HET berdasarkan 3 Zona Wilayah Geografis guna menyesuaikan dengan biaya logistik. Oleh karena itu, kolom `hetha` pada Beras bervariasi sesuai lokasi kabupaten/kota pencatatan:

| Nama Komoditas | Zona 1 (Rp/kg) | Zona 2 (Rp/kg) | Zona 3 (Rp/kg) |
| :--- | :--- | :--- | :--- |
| **Beras Medium** | `13500.0` | `14000.0` | `15500.0` |
| **Beras Premium** | `14900.0` | `15400.0` | `15800.0` |

* **Cakupan Wilayah**:
  * **Zona 1**: Jawa, Lampung, Sumatera Selatan, Bali, NTB, dan Sulawesi.
  * **Zona 2**: Sumatera lainnya (Aceh, Sumut, Sumbar, Riau, Kepri, Jambi, Bengkulu, Babel), NTT, dan Kalimantan.
  * **Zona 3**: Maluku dan Papua.

---

## 6. Ringkasan Alur Wrangling & Transformasi

Berikut adalah ringkasan proses transformasi dari data mentah hingga menjadi data bersih siap guna:
1. **Filtering & Cleaning Baris**:
   * Menghapus baris romawi (header grup komoditas) pada data mentah PIHPS.
   * Melakukan pembersihan whitespace pada nama komoditas dan nama kolom tanggal.
2. **Penyelarasan Skala (Melting)**:
   * Mengubah struktur data dari format lebar (*Wide*) menjadi format panjang (*Long*) agar mempermudah analisis berbasis deret waktu (time series).
3. **Penyelarasan Tipe Data & Satuan**:
   * Mengonversi harga eceran berformat string (mengandung koma) menjadi numerik (*float*).
   * Mengalikan harga dan HET/HA data SP2KP dengan 1000 agar setara dalam satuan Rupiah utuh.
4. **Penanganan Nilai Kosong (Imputasi)**:
   * Mengganti tanda strip (`"-"`) dengan NaN, kemudian melakukan interpolasi linier secara berkelompok per komoditas pada data PIHPS untuk mengisi data hari libur/kosong tanpa merusak karakteristik per komoditas.
5. **Feature Engineering**:
   * Melakukan integrasi data kalender libur nasional, hari keagamaan Islam (Ramadan & Idul Fitri), serta menarik data historis cuaca Jakarta (suhu rata-rata, curah hujan, kecepatan angin) dari Open-Meteo API untuk memperkaya analisis volatilitas harga pangan.
