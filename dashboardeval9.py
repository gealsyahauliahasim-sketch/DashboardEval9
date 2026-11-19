
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ==========================================
# KONFIGURASI DASHBOARD
# ==========================================
st.set_page_config(
    page_title="Dashboard Analisis Diamonds",
    page_icon="💎",
    layout="wide"
)

# ==========================================
# STYLE DAN BACKGROUND GRADASI
# ==========================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* BACKGROUND UTAMA */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse at 8% 12%,
            rgba(233, 79, 145, 0.48) 0%,
            transparent 38%),

        radial-gradient(ellipse at 90% 8%,
            rgba(135, 58, 145, 0.42) 0%,
            transparent 40%),

        radial-gradient(ellipse at 75% 85%,
            rgba(182, 108, 214, 0.40) 0%,
            transparent 42%),

        radial-gradient(ellipse at 15% 90%,
            rgba(246, 161, 203, 0.40) 0%,
            transparent 40%),

        linear-gradient(
            135deg,
            #FCE5F3 0%,
            #F5D3E9 30%,
            #E8C7F0 60%,
            #DCC8F5 100%
        );

    background-attachment: fixed;
}

/* AREA KONTEN */
[data-testid="stMain"] {
    background: transparent;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background:
        linear-gradient(
            160deg,
            rgba(233, 79, 145, 0.28),
            rgba(135, 58, 145, 0.22),
            rgba(182, 108, 214, 0.28)
        );
    border-right: 1px solid rgba(255,255,255,0.4);
}

/* SIDEBAR TEXT */
[data-testid="stSidebar"] * {
    color: #54264F;
}

/* JUDUL */
h1 {
    color: #762D69 !important;
    font-weight: 700 !important;
}

h2, h3 {
    color: #783B77 !important;
    font-weight: 600 !important;
}

/* PARAGRAF */
p, label, span {
    color: #593B59;
}

/* KPI CARDS */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.70);
    border: 1px solid rgba(255,255,255,0.75);
    padding: 18px 20px;
    border-radius: 18px;
    box-shadow: 0 6px 22px rgba(126, 55, 113, 0.10);
    backdrop-filter: blur(12px);
}

/* KPI LABEL */
[data-testid="stMetricLabel"] {
    color: #793E75 !important;
    font-weight: 500;
}

/* KPI VALUE */
[data-testid="stMetricValue"] {
    color: #782D6D !important;
    font-weight: 700;
}

/* SELECTBOX */
[data-testid="stSelectbox"] > div > div {
    background-color: rgba(255,255,255,0.78);
    border-radius: 12px;
}

/* SLIDER */
[data-testid="stSlider"] {
    padding-top: 5px;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

/* TAB */
button[data-baseweb="tab"] {
    color: #783B77 !important;
}

/* EXPANDER */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.55);
    border: 1px solid rgba(255,255,255,0.65);
    border-radius: 15px;
}

/* CHART CONTAINER */
[data-testid="stPlotlyChart"],
[data-testid="stImage"] {
    background: rgba(255,255,255,0.30);
    border-radius: 15px;
}

/* DIVIDER */
hr {
    border-color: rgba(135, 58, 145, 0.20);
}

/* FOOTER */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# MEMUAT DATA
# ==========================================
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv"

@st.cache_data
def load_data():
    return pd.read_csv(url)

data = load_data()


# ==========================================
# SIDEBAR - FILTER DATA
# ==========================================
st.sidebar.title("💎 Filter Dashboard")
st.sidebar.markdown("Atur pilihan data sesuai kebutuhan analisis.")

cut_options = ["All"] + sorted(data["cut"].unique().tolist())
color_options = ["All"] + sorted(data["color"].unique().tolist())
clarity_options = ["All"] + sorted(data["clarity"].unique().tolist())

selected_cut = st.sidebar.selectbox(
    "Cut",
    cut_options
)

selected_color = st.sidebar.selectbox(
    "Color",
    color_options
)

selected_clarity = st.sidebar.selectbox(
    "Clarity",
    clarity_options
)

carat_min = float(data["carat"].min())
carat_max = float(data["carat"].max())

selected_carat = st.sidebar.slider(
    "Rentang Carat",
    min_value=carat_min,
    max_value=carat_max,
    value=(carat_min, carat_max)
)

price_min = int(data["price"].min())
price_max = int(data["price"].max())

selected_price = st.sidebar.slider(
    "Rentang Harga ($)",
    min_value=price_min,
    max_value=price_max,
    value=(price_min, price_max)
)


# ==========================================
# FILTER DATA
# ==========================================
data_filter = data.copy()

if selected_cut != "All":
    data_filter = data_filter[data_filter["cut"] == selected_cut]

if selected_color != "All":
    data_filter = data_filter[data_filter["color"] == selected_color]

if selected_clarity != "All":
    data_filter = data_filter[data_filter["clarity"] == selected_clarity]

data_filter = data_filter[
    (data_filter["carat"] >= selected_carat[0]) &
    (data_filter["carat"] <= selected_carat[1]) &
    (data_filter["price"] >= selected_price[0]) &
    (data_filter["price"] <= selected_price[1])
]


# ==========================================
# JUDUL DASHBOARD
# ==========================================
st.title("💎 Dashboard Analisis Diamonds")

st.markdown("""
Dashboard ini menyajikan visualisasi data berlian berdasarkan
karakteristik fisik, kualitas, serta harga.
Gunakan filter pada sidebar untuk melihat data berdasarkan
kategori dan rentang nilai tertentu.
""")

st.markdown("---")


# ==========================================
# KPI
# ==========================================
col1, col2, col3, col4 = st.columns(4)

jumlah_data = len(data_filter)

rata_harga = (
    data_filter["price"].mean()
    if jumlah_data > 0 else 0
)

rata_carat = (
    data_filter["carat"].mean()
    if jumlah_data > 0 else 0
)

median_harga = (
    data_filter["price"].median()
    if jumlah_data > 0 else 0
)

col1.metric(
    "Jumlah Data",
    f"{jumlah_data:,}"
)

col2.metric(
    "Rata-rata Harga",
    f"${rata_harga:,.2f}"
)

col3.metric(
    "Rata-rata Carat",
    f"{rata_carat:.2f}"
)

col4.metric(
    "Median Harga",
    f"${median_harga:,.0f}"
)

st.markdown("---")


# ==========================================
# PENGATURAN WARNA GRAFIK
# ==========================================
warna = [
    "#E94F91",
    "#873A91",
    "#B66CD6",
    "#F6A1CB",
    "#7565D9"
]

sns.set_theme(style="whitegrid")


# ==========================================
# BOXPLOT
# ==========================================
st.subheader("📊 Distribusi Harga dan Carat Berdasarkan Cut")

col1, col2 = st.columns(2)

with col1:

    fig, ax = plt.subplots(figsize=(9, 5))

    sns.boxplot(
        data=data_filter,
        x="cut",
        y="price",
        palette=warna,
        ax=ax
    )

    ax.set_title(
        "Distribusi Harga Berdasarkan Cut",
        fontsize=13,
        fontweight="bold"
    )

    ax.set_xlabel("Cut")
    ax.set_ylabel("Harga ($)")

    ax.set_facecolor("#FFF9FC")
    fig.patch.set_facecolor("#FFF9FC")

    plt.xticks(rotation=15)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


with col2:

    fig, ax = plt.subplots(figsize=(9, 5))

    sns.boxplot(
        data=data_filter,
        x="cut",
        y="carat",
        palette=warna,
        ax=ax
    )

    ax.set_title(
        "Distribusi Carat Berdasarkan Cut",
        fontsize=13,
        fontweight="bold"
    )

    ax.set_xlabel("Cut")
    ax.set_ylabel("Carat")

    ax.set_facecolor("#FFF9FC")
    fig.patch.set_facecolor("#FFF9FC")

    plt.xticks(rotation=15)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


st.markdown("---")


# ==========================================
# BARPLOT
# ==========================================
st.subheader("📈 Perbandingan Harga dan Jumlah Berlian")

col1, col2 = st.columns(2)

with col1:

    harga_cut = (
        data_filter.groupby("cut")["price"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    harga_cut.plot(
        kind="bar",
        color=warna,
        ax=ax
    )

    ax.set_title(
        "Rata-rata Harga Berdasarkan Cut",
        fontsize=13,
        fontweight="bold"
    )

    ax.set_xlabel("Cut")
    ax.set_ylabel("Rata-rata Harga ($)")

    ax.set_facecolor("#FFF9FC")
    fig.patch.set_facecolor("#FFF9FC")

    plt.xticks(rotation=15)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


with col2:

    jumlah_cut = data_filter["cut"].value_counts()

    fig, ax = plt.subplots(figsize=(9, 5))

    jumlah_cut.plot(
        kind="bar",
        color=warna,
        ax=ax
    )

    ax.set_title(
        "Jumlah Berlian Berdasarkan Cut",
        fontsize=13,
        fontweight="bold"
    )

    ax.set_xlabel("Cut")
    ax.set_ylabel("Jumlah")

    ax.set_facecolor("#FFF9FC")
    fig.patch.set_facecolor("#FFF9FC")

    plt.xticks(rotation=15)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


st.markdown("---")


# ==========================================
# PIE CHART
# ==========================================
st.subheader("🍰 Proporsi Berlian Berdasarkan Cut")

cut_count = data_filter["cut"].value_counts()

fig, ax = plt.subplots(figsize=(8, 6))

ax.pie(
    cut_count,
    labels=cut_count.index,
    autopct="%1.1f%%",
    colors=warna,
    startangle=90,
    wedgeprops={
        "edgecolor": "white",
        "linewidth": 2
    },
    textprops={
        "fontsize": 10
    }
)

ax.set_title(
    "Proporsi Cut",
    fontsize=14,
    fontweight="bold"
)

fig.patch.set_facecolor("#FFF9FC")

plt.tight_layout()

st.pyplot(fig)
plt.close(fig)


st.markdown("---")


# ==========================================
# HISTOGRAM
# ==========================================
st.subheader("📉 Distribusi Harga Berlian")

fig, ax = plt.subplots(figsize=(10, 5))

sns.histplot(
    data=data_filter,
    x="price",
    bins=30,
    kde=True,
    color="#E94F91",
    ax=ax
)

ax.set_title(
    "Distribusi Harga Berlian",
    fontsize=13,
    fontweight="bold"
)

ax.set_xlabel("Harga ($)")
ax.set_ylabel("Frekuensi")

ax.set_facecolor("#FFF9FC")
fig.patch.set_facecolor("#FFF9FC")

plt.tight_layout()

st.pyplot(fig)
plt.close(fig)


st.markdown("---")


# ==========================================
# HEATMAP KORELASI
# ==========================================
st.subheader("🔥 Korelasi Antarvariabel Numerik")

variabel_numerik = [
    "carat",
    "depth",
    "table",
    "price",
    "x",
    "y",
    "z"
]

corr = data_filter[variabel_numerik].corr()

fig, ax = plt.subplots(figsize=(10, 7))

sns.heatmap(
    corr,
    annot=True,
    cmap="PuRd",
    fmt=".2f",
    linewidths=0.5,
    square=True,
    ax=ax
)

ax.set_title(
    "Heatmap Korelasi",
    fontsize=14,
    fontweight="bold"
)

fig.patch.set_facecolor("#FFF9FC")

plt.tight_layout()

st.pyplot(fig)
plt.close(fig)


st.markdown("---")


# ==========================================
# DATASET OVERVIEW
# ==========================================
with st.expander("📋 Dataset Overview"):

    st.markdown("### Data Berlian")

    st.write(
        "Jumlah baris:",
        data_filter.shape[0]
    )

    st.write(
        "Jumlah kolom:",
        data_filter.shape[1]
    )

    st.markdown("### Data")

    st.dataframe(
        data_filter,
        use_container_width=True
    )

    st.markdown("### Statistik Deskriptif")

    st.dataframe(
        data_filter.describe(),
        use_container_width=True
    )


# ==========================================
# FOOTER
# ==========================================
st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#783B77;
        padding:15px;
        font-size:13px;
    ">
        💎 Dashboard Analisis Diamonds
        <br>
        Dibuat menggunakan Python dan Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
