# Pantau Pasar - Data Science

Bagian ini mencakup proses pengumpulan, penilaian, dan pembersihan data untuk proyek Pantau Pasar, sebuah sistem pemantauan dan prediksi harga pangan strategis di Indonesia.

## Sumber Data

Data dikumpulkan dari dua sumber utama:

**PIHPS Nasional (hargapangan.id)**
- Cakupan: seluruh provinsi (agregat nasional)
- Periode: Januari 2022 sampai April 2026
- Komoditas: 21 jenis bahan pangan (beras, cabai, bawang, daging, telur, minyak goreng, gula, garam)
- Tipe laporan: harian, pasar tradisional

**SP2KP Kemendag (sp2kp.kemendag.go.id)**
- Cakupan: 514 kabupaten/kota
- Periode: Januari 2026 sampai April 2026
- Komoditas: 17 jenis bahan pangan

## Struktur Folder

```
├── data/
│   ├── raw/         # data mentah hasil unduhan
│   └── cleaned/     # data hasil proses wrangling
├── data_wrangling.ipynb
├── .gitignore
└── README.md
```

## Proses Data Wrangling

Seluruh proses ada di `data_wrangling.ipynb` dengan alur berikut:

**1. Gathering**
- Load 5 file Excel PIHPS (per tahun) dan 1 file CSV SP2KP
- Preview struktur data mentah dari masing-masing sumber

**2. Assessing**
- Cek dimensi, tipe data, dan periode per file
- Identifikasi missing values (PIHPS 2022 memiliki 2.4% nilai kosong berupa tanda -)
- Identifikasi baris header grup (nomor romawi) yang bukan data asli
- Verifikasi konsistensi nama komoditas antar tahun (100% konsisten)
- Identifikasi masalah format: harga tersimpan sebagai string, tanggal ada spasi, format wide

**3. Cleaning**
- Filter baris header grup (I, II, III, dst)
- Strip whitespace pada nama komoditas dan kolom tanggal
- Konversi format tanggal menjadi datetime
- Konversi harga dari string ke float
- Melt format wide menjadi long agar siap untuk time-series
- Interpolasi linear untuk mengisi missing values per komoditas
- Flag outlier menggunakan metode IQR (tidak dihapus, dijadikan fitur)
- Tambah kolom sumber untuk membedakan asal data

## Output

| File | Jumlah Baris | Keterangan |
|------|-------------|------------|
| `data/cleaned/pihps_cleaned.csv` | 23.709 | Data nasional harian Jan 2022 - Apr 2026 |
| `data/cleaned/sp2kp_cleaned.csv` | 456.590 | Data per kabupaten Jan - Apr 2026 |

Kolom output PIHPS: `Komoditas`, `tanggal`, `harga`, `sumber`, `is_outlier`

Kolom output SP2KP: `no`, `kode_wilayah`, `provinsi`, `kabupaten_kota`, `komoditas`, `hetha`, `tanggal`, `harga`, `sumber`

Saat load file hasil cleaning, gunakan parameter `parse_dates=['tanggal']` agar kolom tanggal terbaca sebagai datetime.
