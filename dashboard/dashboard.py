import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Pantau Pasar", layout="wide")

st.markdown("""
<style>
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0px;
    }
    .sub-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: #7f8c8d;
        margin-bottom: 30px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        border-bottom: 2px solid #e0e0e0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 0px;
        padding: 10px 24px;
        color: #7f8c8d;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        border-bottom: 3px solid #1976d2 !important;
        color: #1976d2 !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pihps_path = os.path.join(base_dir, 'data', 'cleaned', 'pihps_featured.csv')
    sp2kp_path = os.path.join(base_dir, 'data', 'cleaned', 'sp2kp_cleaned.csv')

    df_pihps = pd.read_csv(pihps_path, parse_dates=['tanggal'])
    df_sp2kp = pd.read_csv(sp2kp_path, parse_dates=['tanggal'])
    return df_pihps, df_sp2kp

try:
    df_pihps, df_sp2kp = load_data()
except Exception as e:
    st.error(f"Gagal memuat data: File tidak ditemukan atau path salah. Error: {e}")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Pengaturan")
    st.markdown("Pilih filter untuk menyesuaikan tampilan dashboard.")

    all_komoditas = sorted(df_pihps['Komoditas'].unique())
    default_komoditas = ['Beras Kualitas Medium I', 'Cabai Rawit Merah', 'Daging Sapi Kualitas 1']
    selected_komoditas = st.multiselect("Pilih Komoditas", options=all_komoditas, default=default_komoditas)

    st.markdown("---")

    # Date range filter — affects historical trend chart only
    min_date = df_pihps['tanggal'].min().date()
    max_date = df_pihps['tanggal'].max().date()
    date_input = st.date_input(
        "Rentang Tanggal Tren",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    date_start = date_input[0]
    date_end = date_input[1] if len(date_input) > 1 else max_date

    st.markdown("---")
    st.subheader("Opsi Tambahan")
    show_ramadan = st.checkbox("Tampilkan Periode Ramadan", value=True)
    show_outliers = st.checkbox("Tampilkan Titik Outlier", value=True)

if not selected_komoditas:
    st.warning("Silakan pilih minimal satu komoditas di menu pengaturan (sidebar).")
    st.stop()

# Filtered data for trend chart
df_filtered = df_pihps[
    (df_pihps['Komoditas'].isin(selected_komoditas)) &
    (df_pihps['tanggal'].dt.date >= date_start) &
    (df_pihps['tanggal'].dt.date <= date_end)
]

# --- HEADER ---
st.markdown("<h1 class='main-title'>Dashboard Pantau Pasar</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Pantau pergerakan harga komoditas pangan strategis nasional secara real-time dan interaktif.</p>", unsafe_allow_html=True)

# --- TABS ---
tab1, tab2 = st.tabs(["Interactive Dashboard", "Explanatory Analysis & Insights"])


# TAB 1: INTERACTIVE DASHBOARD

with tab1:
    # --- BAGIAN A: MARKET SNAPSHOT ---
    st.subheader("Snapshot Harga Terkini (Nasional)")

    max_cols = min(len(selected_komoditas), 4)
    cols = st.columns(max_cols)

    latest_date = df_pihps['tanggal'].max()
    prev_7_date = latest_date - pd.Timedelta(days=7)

    for i, kom in enumerate(selected_komoditas):
        df_kom = df_pihps[df_pihps['Komoditas'] == kom].sort_values('tanggal', ascending=False)
        if not df_kom.empty:
            latest_price = df_kom.iloc[0]['harga']
            df_prev_7 = df_kom[(df_kom['tanggal'] >= prev_7_date) & (df_kom['tanggal'] < latest_date)]
            avg_prev_7 = df_prev_7['harga'].mean() if not df_prev_7.empty else latest_price
            delta = latest_price - avg_prev_7
            delta_pct = (delta / avg_prev_7) * 100 if avg_prev_7 > 0 else 0

            col_idx = i % max_cols
            with cols[col_idx]:
                st.metric(
                    label=kom,
                    value=f"Rp {latest_price:,.0f}",
                    delta=f"{delta:,.0f} ({delta_pct:.1f}%) vs 7H lalu",
                    delta_color="inverse",
                )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- BAGIAN B: TREN HISTORIS HARGA ---
    st.subheader("Tren Historis Harga Komoditas")

    if df_filtered.empty:
        st.warning("Tidak ada data untuk rentang tanggal dan komoditas yang dipilih.")
    else:
        fig = go.Figure()
        color_palette = px.colors.qualitative.D3

        for i, kom in enumerate(selected_komoditas):
            df_kom = df_filtered[df_filtered['Komoditas'] == kom]
            if df_kom.empty:
                continue
            color = color_palette[i % len(color_palette)]

            fig.add_trace(go.Scatter(
                x=df_kom['tanggal'], y=df_kom['harga'],
                mode='lines', name=kom,
                line=dict(width=2.5, color=color),
            ))

            if show_outliers:
                df_outlier = df_kom[df_kom['is_outlier'] == True]
                fig.add_trace(go.Scatter(
                    x=df_outlier['tanggal'], y=df_outlier['harga'],
                    mode='markers',
                    marker=dict(color=color, size=6, symbol='diamond-open', line=dict(width=2, color=color)),
                    name=f'{kom} (Outlier)', showlegend=False,
                    hoverinfo='skip',
                ))

        if show_ramadan:
            ramadan_dates = sorted(df_pihps[df_pihps['is_ramadan'] == 1]['tanggal'].unique())
            if ramadan_dates:
                start = ramadan_dates[0]
                for j in range(1, len(ramadan_dates)):
                    if (ramadan_dates[j] - ramadan_dates[j - 1]).days > 1:
                        fig.add_vrect(x0=start, x1=ramadan_dates[j - 1], fillcolor="#f1c40f",
                                      opacity=0.15, line_width=0, annotation_text="Ramadan")
                        start = ramadan_dates[j]
                fig.add_vrect(x0=start, x1=ramadan_dates[-1], fillcolor="#f1c40f",
                              opacity=0.15, line_width=0, annotation_text="Ramadan")

        fig.update_layout(
            xaxis_title="Tanggal",
            yaxis_title="Harga (Rp)",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=50, b=0),
            plot_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
            yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- BAGIAN C: SNAPSHOT REGIONAL (SP2KP) ---
    st.subheader("Snapshot Perbandingan Wilayah (Jan-Apr 2026)")
    st.markdown("Disparitas harga antar provinsi berdasarkan data SP2KP.")

    selected_regional = st.selectbox("Pilih Komoditas untuk Analisis Wilayah", options=selected_komoditas)

    # Match ke SP2KP: coba 2 kata pertama dulu, fallback ke 1 kata
    words = selected_regional.split()
    keyword_primary = ' '.join(words[:2]) if len(words) >= 2 else words[0]
    keyword_fallback = words[0]

    df_sp2kp_filtered = df_sp2kp[df_sp2kp['komoditas'].str.contains(keyword_primary, case=False, na=False)]
    keyword_used = keyword_primary
    if df_sp2kp_filtered.empty:
        df_sp2kp_filtered = df_sp2kp[df_sp2kp['komoditas'].str.contains(keyword_fallback, case=False, na=False)]
        keyword_used = keyword_fallback

    if not df_sp2kp_filtered.empty:
        latest_sp2kp_date = df_sp2kp_filtered['tanggal'].max()
        st.caption(f"Data berdasarkan rekaman terakhir: **{latest_sp2kp_date.strftime('%d %B %Y')}**")

        df_latest_sp2kp = df_sp2kp_filtered[df_sp2kp_filtered['tanggal'] == latest_sp2kp_date]
        avg_provinsi = df_latest_sp2kp.groupby('provinsi')['harga'].mean().reset_index()
        avg_provinsi = avg_provinsi.sort_values('harga', ascending=True)

        fig_bar = px.bar(
            avg_provinsi, x='harga', y='provinsi', orientation='h',
            color='harga', color_continuous_scale='Reds',
            title=f"Rata-rata Harga {keyword_used} per Provinsi",
            labels={'harga': "Harga (Rp)", 'provinsi': ""},
        )
        fig_bar.update_layout(
            margin=dict(l=0, r=0, t=40, b=0),
            plot_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info(f"Data regional untuk '{selected_regional}' belum tersedia di dataset SP2KP saat ini.")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- BAGIAN D: PREDIKSI AI ---
    st.subheader("AI Price Prediction")
    st.info("Coming Soon: Fitur prediksi harga sedang dalam tahap pengerjaan. Segera hadir integrasi Model Machine Learning untuk memproyeksikan pergerakan harga komoditas ke depan.")


# TAB 2: EXPLANATORY ANALYSIS & INSIGHTS

with tab2:
    st.header("Executive Summary: Dinamika Pasar Pangan")
    st.markdown("""
    Bagian ini merangkum **Insight dan Kesimpulan** yang didapatkan dari proses *Exploratory Data Analysis (EDA)*
    dan *Feature Engineering* mendalam terhadap 21 komoditas pangan nasional periode 2022-2026.

    Secara garis besar, pergerakan harga pangan dipengaruhi oleh 4 pilar utama yang sangat krusial bagi ketahanan pasokan:
    """)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Inflasi Bersifat Struktural")
        st.markdown("""
        **Penyumbang Terbesar: Beras & Gula**
        - Harga pangan tidak sekadar berfluktuasi naik-turun secara acak, tetapi memiliki tren kenaikan **struktural jangka panjang**.
        - Analisis *Year-on-Year* membuktikan bahwa kelompok **Beras** merupakan komoditas dengan pertumbuhan kumulatif paling drastis sejak 2022 hingga 2026. Hal ini mengubah garis *baseline* "harga normal" di masyarakat secara permanen.
        """)

        st.subheader("3. Karakter Volatilitas Ekstrem")
        st.markdown("""
        **Cabai Sangat Liar, Daging Sapi Stabil**
        - Karakteristik pasar sangat terfragmentasi. **Cabai Rawit Merah** memiliki volatilitas (*Coefficient of Variation*) paling tinggi mencapai **24%**.
        - Berbanding terbalik dengan **Daging Sapi** yang meskipun mahal, memiliki volatilitas di bawah **3%** dan nyaris *flat* pada grafik *rolling 30-day volatility*. Hal ini mengindikasikan bahwa risiko lonjakan harga harian didominasi oleh kelompok hortikultura.
        """)

    with col2:
        st.subheader("2. Krisis Sentimen Musiman (Ramadan)")
        st.markdown("""
        **Lonjakan Ekstrem pada Komoditas Tertentu**
        - Bulan Ramadan terbukti secara data sebagai **katalis utama krisis musiman**.
        - Tidak semua bahan pangan melonjak. Pemeringkatan data historis menunjukkan Top 3 korban spekulasi dan lonjakan *demand* Lebaran adalah: **Cabai Rawit Merah (+10.8%)**, **Cabai Rawit Hijau (+5.6%)**, dan **Minyak Goreng Curah (+5.5%)**.
        """)

        st.subheader("4. Efek Lagging pada Gangguan Cuaca")
        st.markdown("""
        **Disrupsi Rantai Pasok Bukanlah Hal Instan**
        - Hasil korelasi *Spearman* (Heatmap) membuktikan bahwa **Curah Hujan** dan **Suhu Ekstrem** tidak memberikan *shock* (dampak instan pada hari-H) terhadap harga pasar ritel.
        - Cuaca ekstrem lebih sering menyebabkan gagal panen dan rusaknya logistik yang **membutuhkan waktu berminggu-minggu** (*Time-Lag*) sebelum menghantam suplai konsumen di level pasar.
        """)

    st.markdown("---")

    st.info("""Catatan untuk Model Machine Learning: Berdasarkan kesimpulan di atas, pemodelan AI untuk prediksi harga
    wajib menyertakan variabel `is_ramadan` sebagai fitur eksogen utama, serta melakukan transformasi *Rolling Window*
    atau *Time-Lag* pada data cuaca agar model dapat mempelajari dampak disrupsi secara lebih akurat.""")
