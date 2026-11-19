import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Konfigurasi
st.set_page_config(page_title="Dashboard Analisis Diamonds", layout="wide")

st.markdown(
    """
    <style>

    /*Background Gradasi Utama*/
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(
                ellipse at 10% 10%,
                #FFDDEB 0%,
                transparent 45%
            ),
            radial-gradient(
                ellipse at 90% 20%,
                #E8D5FF 0%,
                transparent 45%
            ),
            radial-gradient(
                ellipse at 50% 100%,
                #FFE2D5 0%,
                transparent 50%
            ),
            linear-gradient(
                135deg,
                #FFF8FC,
                #FCEAF5,
                #F5EEFF
            );
    }

    /*Sidebar Gradasi*/
    [data-testid="stSidebar"] {
        background: linear-gradient(
            160deg,
            #F7D6E8,
            #EBCFEF,
            #E2D6FA
        );
    }

    /*Area Dashboard Transparan*/
    [data-testid="stMain"] {
        background: transparent;
    }

    /*Warna Font Utama*/
    .stApp,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: #8E1649;
    }

    /*Warna Judul*/
    h1, h2, h3, h4, h5, h6 {
        color: #C2185B !important;
    }

    /*Judul Dashboard*/
    h1 {
        font-size: 42px !important;
        font-weight: bold !important;
        text-align: center !important;
    }

    /*Warna Font Sidebar*/
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #8E1649 !important;
    }

    /*Judul Filter*/
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #C2185B !important;
    }

    /*Dropdown dan Filter*/
    [data-baseweb="select"] *,
    [data-baseweb="tag"] *,
    [data-baseweb="slider"] *,
    [data-baseweb="input"] * {
        color: #8E1649 !important;
    }

    /*Pilihan Dropdown*/
    [role="option"] {
        color: #8E1649 !important;
        background-color: #FFFFFF !important;
    }

    /*KPI*/
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: #8E1649 !important;
    }

    /*Caption*/
    [data-testid="stCaptionContainer"] {
        color: #8E1649 !important;
    }

    /*Tabel Dataset*/
    [data-testid="stDataFrame"] {
        color: #8E1649;
    }

    /*Expander*/
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p {
        color: #8E1649 !important;
    }

    /*Tombol*/
    button {
        color: #8E1649 !important;
    }

    /*Kartu Dashboard*/
    [class*="st-key-bg_kpi"],
    [class*="st-key-bg_box"],
    [class*="st-key-bg_bar"],
    [class*="st-key-bg_pie"],
    [class*="st-key-bg_hist"],
    [class*="st-key-bg_heatmap"] {
        background-color: rgba(255, 255, 255, 0.94);
        border: 1.5px solid #E8A1C4;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0px 4px 15px rgba(194, 24, 91, 0.08);
    }

    </style>
    """,
    unsafe_allow_html=True,
)

sns.set_theme(style="whitegrid")

#Load Data
path = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv"
df_dashboard = pd.read_csv(path)

#Fitur Filter
st.sidebar.header("Filter Dashboard")

cut_value = list(df_dashboard["cut"].unique())
selected_cut = st.sidebar.multiselect(
    label="Diamond Cut Quality",
    options=cut_value,
    default=cut_value
)

color_value = sorted(list(df_dashboard["color"].unique()))
selected_color = st.sidebar.multiselect(
    label="Diamond Color",
    options=color_value,
    default=color_value
)

clarity_value = sorted(list(df_dashboard["clarity"].unique()))
selected_clarity = st.sidebar.multiselect(
    label="Diamond Clarity",
    options=clarity_value,
    default=clarity_value
)

carat_value = (
    float(df_dashboard["carat"].min()),
    float(df_dashboard["carat"].max())
)

selected_carat = st.sidebar.slider(
    label="Diamond Carat Range",
    min_value=carat_value[0],
    max_value=carat_value[1],
    value=carat_value
)

price_value = (
    int(df_dashboard["price"].min()),
    int(df_dashboard["price"].max())
)

selected_price = st.sidebar.slider(
    label="Diamond Price Range ($)",
    min_value=price_value[0],
    max_value=price_value[1],
    value=price_value
)

df_filtered = df_dashboard[
    (df_dashboard["cut"].isin(selected_cut)) &
    (df_dashboard["color"].isin(selected_color)) &
    (df_dashboard["clarity"].isin(selected_clarity)) &
    (df_dashboard["carat"].between(selected_carat[0], selected_carat[1])) &
    (df_dashboard["price"].between(selected_price[0], selected_price[1]))
]

if df_filtered.empty:
    st.warning("Tidak ada data yang sesuai dengan filter. Silakan pilih kembali opsi filter.")
    st.stop()

#Membuat Judul Dashboard
st.markdown(
    """
    <h1 style="
        color: #C2185B;
        font-size: 42px;
        font-weight: bold;
        text-align: center;
    ">
        DASHBOARD ANALISIS DIAMONDS
    </h1>
    """,
    unsafe_allow_html=True
)

st.caption("Dashboard Evaluasi Praktikum 9 Sains Data - Dataset NIM Genap")

#Membuat KPI
with st.container(border=True, key="bg_kpi"):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Jumlah Berlian",
            f"{len(df_filtered):,}"
        )

    with col2:
        st.metric(
            "Rata-Rata Harga Berlian",
            f"${df_filtered['price'].mean():,.2f}"
        )

    with col3:
        st.metric(
            "Rata-Rata Carat",
            f"{df_filtered['carat'].mean():.2f}"
        )

    with col4:
        st.metric(
            "Median Harga Berlian",
            f"${df_filtered['price'].median():,.2f}"
        )

#Membuat Visualisasi Tengah

##Persiapan dataset visualisasi
harga_per_cut = df_filtered.groupby("cut")["price"].mean().reset_index()
jumlah_per_cut = df_filtered.groupby("cut").size().reset_index(name="jumlah")
distribusi_cut = df_filtered["cut"].value_counts()

heatmap_df = df_filtered[
    ["carat", "depth", "table", "price", "x", "y", "z"]
].corr()

##Membuat fungsi pengaturan grafik
def atur_grafik(fig, ax, label_x, label_y):
    warna_kartu = "#FFFFFF"
    warna_teks = "#8E1649"
    warna_grid = "#F8D7E8"

    fig.patch.set_facecolor(warna_kartu)
    ax.set_facecolor(warna_kartu)
    ax.set_xlabel(label_x, color=warna_teks)
    ax.set_ylabel(label_y, color=warna_teks)
    ax.tick_params(colors=warna_teks)
    ax.grid(axis="y", color=warna_grid)
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_color("#E75480")

##Membuat visualisasi Boxplot
with st.container(border=True, key="bg_box"):
    col1_box, col2_box = st.columns(2)

    with col1_box:
        st.markdown("**Distribusi Harga Berlian Berdasarkan Cut**")

        fig1, ax1 = plt.subplots()

        sns.boxplot(
            data=df_filtered,
            x="cut",
            y="price",
            color="#F4A6C1",
            ax=ax1
        )

        atur_grafik(
            fig1,
            ax1,
            "Diamond Cut",
            "Diamond Price ($)"
        )

        st.pyplot(fig1)
        plt.close(fig1)

    with col2_box:
        st.markdown("**Distribusi Carat Berdasarkan Cut**")

        fig2, ax2 = plt.subplots()

        sns.boxplot(
            data=df_filtered,
            x="cut",
            y="carat",
            color="#E75480",
            ax=ax2
        )

        atur_grafik(
            fig2,
            ax2,
            "Diamond Cut",
            "Carat"
        )

        st.pyplot(fig2)
        plt.close(fig2)

#Membuat Visualisasi Barplot
with st.container(border=True, key="bg_bar"):
    col1_bar, col2_bar = st.columns(2)

    with col1_bar:
        st.markdown("**Rata-Rata Harga Berlian Berdasarkan Cut**")

        fig3, ax3 = plt.subplots()

        sns.barplot(
            data=harga_per_cut,
            x="cut",
            y="price",
            color="#E75480",
            ax=ax3
        )

        atur_grafik(
            fig3,
            ax3,
            "Diamond Cut",
            "Average Price ($)"
        )

        for container in ax3.containers:
            ax3.bar_label(
                container,
                fmt="$%.0f",
                color="#C2185B",
                fontsize=9,
                padding=3
            )

        st.pyplot(fig3)
        plt.close(fig3)

    with col2_bar:
        st.markdown("**Jumlah Berlian Berdasarkan Cut**")

        fig4, ax4 = plt.subplots()

        sns.barplot(
            data=jumlah_per_cut,
            x="cut",
            y="jumlah",
            color="#D62828",
            ax=ax4
        )

        atur_grafik(
            fig4,
            ax4,
            "Diamond Cut",
            "Number of Diamonds"
        )

        for container in ax4.containers:
            ax4.bar_label(
                container,
                fmt="%.0f",
                color="#8E1649",
                fontsize=9,
                padding=3
            )

        st.pyplot(fig4)
        plt.close(fig4)

#Membuat Visualisasi Pie Chart
with st.container(border=True, key="bg_pie"):
    st.markdown("**Persentase Berlian Berdasarkan Cut**")

    fig5, ax5 = plt.subplots()

    warna_pie = ["#F8D7E8", "#F4A6C1", "#E75480", "#C2185B", "#D62828"]

    fig5.patch.set_facecolor("#FFFFFF")
    ax5.set_facecolor("#FFFFFF")

    ax5.pie(
        distribusi_cut,
        labels=distribusi_cut.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=warna_pie,
        textprops={"color": "#8E1649"},
        wedgeprops={
            "edgecolor": "#FFFFFF",
            "linewidth": 2
        }
    )

    ax5.set_title(
        "Diamond Cut Distribution",
        color="#C2185B"
    )

    st.pyplot(fig5)
    plt.close(fig5)

#Membuat Visualisasi Histogram
with st.container(border=True, key="bg_hist"):
    st.markdown("**Distribusi Harga Berlian**")

    fig6, ax6 = plt.subplots()

    sns.histplot(
        data=df_filtered,
        x="price",
        bins=30,
        color="#E75480",
        kde=True,
        ax=ax6
    )

    if len(ax6.lines) > 0:
        ax6.lines[-1].set_color("#D62828")

    atur_grafik(
        fig6,
        ax6,
        "Diamond Price ($)",
        "Frequency"
    )

    st.pyplot(fig6)
    plt.close(fig6)

#Membuat Visualisasi Heatmap
with st.container(border=True, key="bg_heatmap"):
    st.markdown("**Heatmap Korelasi Variabel Numerik**")

    fig7, ax7 = plt.subplots()

    fig7.patch.set_facecolor("#FFFFFF")
    ax7.set_facecolor("#FFFFFF")

    sns.heatmap(
        heatmap_df,
        annot=True,
        fmt=".2f",
        cmap="RdPu",
        linecolor="#FFFFFF",
        linewidths=1,
        ax=ax7
    )

    ax7.set_xlabel("Variabel", color="#8E1649")
    ax7.set_ylabel("Variabel", color="#8E1649")
    ax7.tick_params(colors="#8E1649")

    st.pyplot(fig7)
    plt.close(fig7)

#Membuat View Dataset
with st.expander("**Dataset Overview**"):
    st.write("Jumlah Data:", len(df_filtered))
    st.dataframe(df_filtered, use_container_width=True)

    st.markdown("**Statistik Deskriptif**")
    st.dataframe(
        df_filtered.describe(),
        use_container_width=True
    )
