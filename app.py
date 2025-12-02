import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Konfigurasi halaman
st.set_page_config(
    page_title="Demo Visualisasi Data",
    layout="wide"
)

st.title("Dashboard Visualisasi Data Sederhana")

st.write(
    """
    Aplikasi ini bisa:
    - Menampilkan data (default atau dari file CSV yang kamu upload)
    - Membuat grafik **line chart** dan **bar chart** secara interaktif
    """
)

# ====== SIDEBAR ======
st.sidebar.header("Pengaturan")

data_source = st.sidebar.radio(
    "Sumber data",
    ("Gunakan data contoh", "Upload file CSV sendiri")
)

# ====== LOAD DATA ======
@st.cache_data
def generate_sample_data():
    dates = pd.date_range("2025-01-01", periods=12, freq="M")
    df = pd.DataFrame({
        "tanggal": dates,
        "penjualan": np.random.randint(100, 500, size=len(dates)),
        "biaya": np.random.randint(50, 300, size=len(dates)),
        "kota": np.random.choice(["Jakarta", "Bandung", "Surabaya"], size=len(dates)),
    })
    return df

if data_source == "Upload file CSV sendiri":
    uploaded_file = st.sidebar.file_uploader("Upload file CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("Silakan upload file CSV terlebih dahulu, atau pilih 'Gunakan data contoh'.")
        df = generate_sample_data()
else:
    df = generate_sample_data()

# Coba konversi kolom bertipe tanggal (jika ada nama kolom 'tanggal')
if "tanggal" in df.columns:
    try:
        df["tanggal"] = pd.to_datetime(df["tanggal"])
    except Exception:
        pass  # kalau gagal, biarkan saja

# ====== TAMPILKAN DATA ======
st.subheader("Data yang digunakan")
st.dataframe(df, use_container_width=True)

# ====== PILIH KOLOM UNTUK GRAFIK ======
numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

if not numeric_cols:
    st.error("Tidak ada kolom numerik di data. Tambahkan kolom angka (int/float) di CSV kamu.")
else:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Pengaturan Grafik")

    chart_type = st.sidebar.selectbox(
        "Jenis grafik",
        ["Line chart (built-in Streamlit)", "Bar chart (Matplotlib)"]
    )

    x_col = st.sidebar.selectbox(
        "Kolom sumbu X",
        df.columns
    )

    y_col = st.sidebar.selectbox(
        "Kolom sumbu Y (numerik)",
        numeric_cols
    )

    # Filter data (opsional)
    if "kota" in df.columns:
        unique_cities = ["(Semua)"] + sorted(df["kota"].astype(str).unique().tolist())
        selected_city = st.sidebar.selectbox("Filter kota (opsional)", unique_cities)

        if selected_city != "(Semua)":
            df_plot = df[df["kota"].astype(str) == selected_city]
        else:
            df_plot = df.copy()
    else:
        df_plot = df.copy()

    if df_plot.empty:
        st.warning("Data kosong setelah filter. Coba ubah filter atau upload data lain.")
    else:
        # ====== TAMPILKAN GRAFIK ======
        st.subheader("Visualisasi Data")

        col1, col2 = st.columns([2, 1])

        with col1:
            if chart_type == "Line chart (built-in Streamlit)":
                st.markdown("#### Line Chart")
                try:
                    chart_data = df_plot[[x_col, y_col]].set_index(x_col)
                    st.line_chart(chart_data, use_container_width=True)
                except Exception as e:
                    st.error(f"Gagal membuat line chart: {e}")

            elif chart_type == "Bar chart (Matplotlib)":
                st.markdown("#### Bar Chart")
                try:
                    fig, ax = plt.subplots()
                    ax.bar(df_plot[x_col].astype(str), df_plot[y_col])
                    ax.set_xlabel(x_col)
                    ax.set_ylabel(y_col)
                    ax.set_title(f"{y_col} berdasarkan {x_col}")
                    plt.xticks(rotation=45, ha="right")
                    plt.tight_layout()
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Gagal membuat bar chart: {e}")

        with col2:
            st.markdown("#### Statistik Ringkas")
            st.write(df_plot[y_col].describe())
            st.markdown("#### Info")
            st.write(
                f"""
                **Sumbu X:** `{x_col}`  
                **Sumbu Y:** `{y_col}`  
                **Jumlah baris:** {len(df_plot)}
                """
            )

st.markdown("---")
st.caption("Contoh aplikasi Streamlit untuk visualisasi data dan siap di-deploy via GitHub.")
