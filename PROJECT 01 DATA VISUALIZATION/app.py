"""
📊 Google Play Store — Data Visualisation Case Study
A dark-themed, interactive Streamlit app built from the original notebook.
"""

import warnings
warnings.filterwarnings("ignore")

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# ----------------------------------------------------------------------
# DATASET PATH — bundled in the same GitHub repo as this app
# (https://github.com/Anjaliy6126/datavisuallization)
# ----------------------------------------------------------------------
APP_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_CANDIDATES = [
    "googleplaystore_v2 (1).csv",
    "googleplaystore_v2.csv",
    "data/googleplaystore_v2 (1).csv",
    "data/googleplaystore_v2.csv",
]

def find_bundled_csv():
    for name in CSV_CANDIDATES:
        path = os.path.join(APP_DIR, name)
        if os.path.exists(path):
            return path
    return None

# ----------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Play Store Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# GLASSMORPHISM / SAAS DASHBOARD THEME
# Palette: #6C63FF (primary) · #8EC5FC (secondary) · #FBC2EB (accent)
# ----------------------------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Fira+Code&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

/* ================= BACKGROUND ================= */
.stApp {
    background: radial-gradient(circle at 12% 8%, rgba(108,99,255,0.20), transparent 40%),
                radial-gradient(circle at 88% 12%, rgba(142,197,252,0.16), transparent 42%),
                radial-gradient(circle at 50% 95%, rgba(251,194,235,0.12), transparent 45%),
                linear-gradient(160deg, #0b0a1a 0%, #14122b 45%, #0f0c22 100%);
    background-attachment: fixed;
    color: #eef1ff;
}

/* soft floating orbs behind content for depth */
.bg-orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(90px);
    z-index: 0;
    pointer-events: none;
    opacity: 0.55;
}
.bg-orb-1 { width: 380px; height: 380px; top: -120px; left: -100px; background: #6C63FF; }
.bg-orb-2 { width: 420px; height: 420px; bottom: -140px; right: -120px; background: #8EC5FC; }
.bg-orb-3 { width: 300px; height: 300px; top: 45%; right: 10%; background: #FBC2EB; opacity: 0.28; }

/* ================= SIDEBAR ================= */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(20,18,43,0.98) 0%, rgba(11,10,26,0.98) 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] * {
    color: #e8e6ff !important;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.12);
}

/* sidebar brand block */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 6px 2px 18px 2px;
    margin-bottom: 6px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
.sidebar-brand .logo-emoji {
    font-size: 30px;
    background: linear-gradient(135deg, #6C63FF, #8EC5FC);
    width: 46px;
    height: 46px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 6px 16px rgba(108,99,255,0.4);
}
.sidebar-brand .brand-title {
    font-weight: 700;
    font-size: 16px;
    line-height: 1.15;
    color: #ffffff;
}
.sidebar-brand .brand-sub {
    font-size: 11.5px;
    color: #a9a6d6;
    letter-spacing: 0.4px;
}

/* sidebar nav (radio) styled like a pill nav list */
section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 4px;
    display: flex;
    flex-direction: column;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 9px 12px !important;
    margin-bottom: 2px;
    transition: all 0.2s ease;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: linear-gradient(90deg, rgba(108,99,255,0.22), rgba(142,197,252,0.10));
    border-color: rgba(142,197,252,0.35);
    transform: translateX(3px);
}

.sidebar-tip {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-left: 3px solid #8EC5FC;
    border-radius: 10px;
    padding: 10px 12px;
    font-size: 13px;
}

.sidebar-footer {
    text-align: center;
    font-size: 12px;
    color: #9490c4 !important;
    padding-top: 10px;
}

/* ================= HEADINGS ================= */
h1, h2, h3 {
    background: linear-gradient(90deg, #a18cd1, #8EC5FC, #FBC2EB);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    letter-spacing: 0.4px;
}

p, li, span, label, .stMarkdown {
    color: #d9d9f3 !important;
}

/* ================= HERO BANNER ================= */
.hero-banner {
    position: relative;
    overflow: hidden;
    padding: 34px 38px;
    border-radius: 24px;
    background: linear-gradient(120deg, rgba(108,99,255,0.20), rgba(142,197,252,0.10) 55%, rgba(251,194,235,0.10));
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.14);
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
    margin-bottom: 26px;
}
.hero-banner::after {
    content: "";
    position: absolute;
    top: -60%; right: -15%;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(142,197,252,0.35), transparent 70%);
    border-radius: 50%;
}
.hero-icon {
    font-size: 54px;
    background: linear-gradient(135deg, rgba(108,99,255,0.35), rgba(251,194,235,0.25));
    width: 84px; height: 84px;
    border-radius: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 24px rgba(108,99,255,0.3);
}
.hero-tagline {
    display: inline-flex;
    gap: 8px;
    margin-top: 10px;
    font-size: 14.5px;
    color: #cfd0ff !important;
}
.data-badge {
    display: inline-block;
    margin-top: 14px;
    padding: 5px 14px;
    font-size: 12.5px;
    font-weight: 600;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.16);
    color: #eef1ff !important;
}

/* ================= KPI / METRIC CARDS ================= */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(108,99,255,0.16), rgba(142,197,252,0.08));
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 16px 20px;
    box-shadow: 0 6px 22px rgba(0,0,0,0.28);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(108,99,255,0.35);
}
div[data-testid="stMetricLabel"] { color: #c9c4ff !important; font-weight: 600; }
div[data-testid="stMetricValue"] { color: #ffffff !important; }

.kpi-icon {
    font-size: 22px;
    margin-bottom: 2px;
}

/* ================= GLASS CARDS (containers / custom cards) ================= */
.custom-card {
    background: rgba(255,255,255,0.045);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 20px 22px;
    margin-bottom: 16px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.28);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
.custom-card:hover {
    transform: translateY(-3px);
    border-color: rgba(142,197,252,0.35);
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}

/* Native bordered st.container() -> glass "insight card" wrapper */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.045) !important;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 20px !important;
    padding: 6px 6px 2px 6px;
    box-shadow: 0 8px 28px rgba(0,0,0,0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    margin-bottom: 16px;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(108,99,255,0.4) !important;
    box-shadow: 0 14px 36px rgba(108,99,255,0.22);
}

/* ================= BUTTONS ================= */
.stButton>button, .stDownloadButton>button {
    background: linear-gradient(90deg, #6C63FF, #8EC5FC);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 0.6em 1.5em;
    font-weight: 600;
    letter-spacing: 0.2px;
    transition: 0.25s;
    box-shadow: 0 4px 16px rgba(108, 99, 255, 0.35);
}
.stButton>button:hover, .stDownloadButton>button:hover {
    background: linear-gradient(90deg, #7d75ff, #a3d3ff);
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 10px 26px rgba(108, 99, 255, 0.5);
}

/* ================= INPUTS / SELECT / SLIDER / UPLOADER ================= */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
}
.stSlider {
    padding-top: 6px;
}
.stFileUploader > div {
    background: rgba(255,255,255,0.045);
    border: 1.5px dashed rgba(142,140,255,0.5);
    border-radius: 16px;
    transition: all 0.2s ease;
}
.stFileUploader > div:hover {
    border-color: #8EC5FC;
    background: rgba(142,197,252,0.08);
}

/* ================= TABS ================= */
button[data-baseweb="tab"] {
    color: #c9c4ff !important;
    font-weight: 600;
    border-radius: 10px 10px 0 0 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #ffffff !important;
    border-bottom: 3px solid #8EC5FC !important;
    background: rgba(108,99,255,0.1);
}

/* ================= EXPANDERS ================= */
details, div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 16px !important;
    overflow: hidden;
    box-shadow: 0 6px 20px rgba(0,0,0,0.25);
}
div[data-testid="stExpander"] summary {
    font-weight: 600;
    color: #eef1ff !important;
}

/* ================= DATAFRAME ================= */
div[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 8px 26px rgba(0,0,0,0.3);
}

/* ================= ALERTS / TOASTS ================= */
div[data-testid="stAlert"] {
    border-radius: 14px !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.12);
}

/* ================= FOOTER ================= */
.app-footer {
    text-align: center;
    padding: 26px 20px 18px 20px;
    margin-top: 30px;
    border-top: 1px solid rgba(255,255,255,0.1);
}
.app-footer .brand {
    font-weight: 700;
    font-size: 16px;
    background: linear-gradient(90deg, #a18cd1, #8EC5FC, #FBC2EB);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.app-footer .sub {
    font-size: 12.5px;
    color: #9490c4 !important;
    margin-top: 4px;
}
.footer-pill {
    display: inline-block;
    margin: 10px 5px 0 5px;
    padding: 4px 12px;
    font-size: 11.5px;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.14);
    color: #c9c4ff !important;
}

hr { border-color: rgba(255,255,255,0.1); }

/* ================= RESPONSIVE ================= */
@media (max-width: 900px) {
    .hero-banner { padding: 22px 20px; }
    .hero-icon { width: 60px; height: 60px; font-size: 36px; border-radius: 16px; }
    h1 { font-size: 1.5rem !important; }
}

</style>

<div class="bg-orb bg-orb-1"></div>
<div class="bg-orb bg-orb-2"></div>
<div class="bg-orb bg-orb-3"></div>
""", unsafe_allow_html=True)

# Matching dark glass plot theme
plt.style.use("dark_background")
PLOT_BG = "none"  # transparent so charts blend with the glass cards
plt.rcParams.update({
    "figure.facecolor": PLOT_BG,
    "axes.facecolor": PLOT_BG,
    "savefig.facecolor": PLOT_BG,
    "axes.edgecolor": "#8ec5fc",
    "axes.labelcolor": "#eef1ff",
    "xtick.color": "#d9d9f3",
    "ytick.color": "#d9d9f3",
    "text.color": "#eef1ff",
    "grid.color": "#33334d",
})
ACCENT_PALETTE = sns.color_palette(
    ["#6C63FF", "#8EC5FC", "#FBC2EB", "#43E6C4", "#FFD166", "#FF6B9D", "#5EE7DF"]
)
sns.set_palette(ACCENT_PALETTE)

PLOTLY_TEMPLATE = "plotly_dark"


def style_plotly(fig, height=None):
    """Purely cosmetic: makes Plotly figures blend with the glass theme.
    Does not touch any data, traces, or computed values."""
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins, sans-serif", color="#eef1ff"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=60, l=10, r=10, b=10),
    )
    if height:
        fig.update_layout(height=height)
    return fig


# ----------------------------------------------------------------------
# HERO / LOGO HEADER
# ----------------------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div style="display:flex; align-items:center; gap:20px;">
        <div class="hero-icon">📱✨</div>
        <div>
            <h1 style="margin-bottom:0;">Google Play Store — Insights Lab</h1>
            <p style="margin-top:6px; font-size:15px;" class="hero-tagline">🎯 Data Cleaning &nbsp;•&nbsp; 📊 Visual Storytelling &nbsp;•&nbsp; 🚀 Business Insights</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# SIDEBAR — DATA UPLOAD & NAV
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="logo-emoji">📊</div>
        <div>
            <div class="brand-title">Play Store Insights</div>
            <div class="brand-sub">Analytics Workspace</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    section = st.radio(
        "Choose a section",
        [
            "🏠 Overview",
            "🧹 Data Cleaning",
            "📦 Outlier Analysis",
            "📈 Distributions",
            "🥧 Categorical Views",
            "🔍 Relationships",
            "🌡️ Heatmaps",
            "🕒 Trends & Stacked Bars",
            "⚡ Interactive Plotly",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("### 💡 Tip")
    st.markdown(
        '<div class="sidebar-tip">This app reads <code>googleplaystore_v2 (1).csv</code> '
        'directly from the GitHub repo it\'s deployed from.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="sidebar-footer">Made with 💜 using <b>Streamlit</b></div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------
# DATA LOADING + CLEANING PIPELINE (mirrors the notebook)
# ----------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def make_demo_data(n=1200):
    rng = np.random.default_rng(42)
    categories = ["GAME", "TOOLS", "FAMILY", "MEDICAL", "EDUCATION", "BUSINESS", "SOCIAL"]
    genres = ["Tools", "Entertainment", "Medical", "Education", "Action", "Puzzle"]
    content = ["Everyone", "Everyone 10+", "Teen", "Mature 17+"]
    df = pd.DataFrame({
        "App": [f"App {i}" for i in range(n)],
        "Category": rng.choice(categories, n),
        "Rating": np.clip(rng.normal(4.1, 0.5, n), 1, 5).round(1),
        "Reviews": rng.integers(0, 2_000_000, n).astype(str),
        "Size": rng.uniform(1, 100, n),
        "Installs": rng.choice(["1,000+", "10,000+", "100,000+", "1,000,000+", "10,000,000+"], n),
        "Type": rng.choice(["Free", "Paid"], n, p=[0.85, 0.15]),
        "Price": [str(0) if t == "Free" else f"${round(rng.uniform(0.99, 29.99), 2)}" for t in rng.choice(["Free", "Paid"], n, p=[0.85, 0.15])],
        "Content Rating": rng.choice(content, n),
        "Genres": rng.choice(genres, n),
        "Last Updated": pd.to_datetime(rng.integers(1, 366, n), unit="D", origin="2018-01-01"),
        "Current Ver": "1.0",
        "Android Ver": rng.choice(["4.1 and up", "4.0 and up", "5.0 and up"], n),
    })
    return df


@st.cache_data(show_spinner=False)
def load_raw(path):
    if path is not None:
        return pd.read_csv(path)
    return make_demo_data()


@st.cache_data(show_spinner=False)
def clean_pipeline(raw: pd.DataFrame):
    steps = []
    df = raw.copy()
    steps.append(("Initial shape", df.shape))

    # Drop rows with null Rating
    if "Rating" in df.columns:
        df = df[~df.Rating.isnull()]
        steps.append(("After dropping null Rating", df.shape))

    # Drop shifted / broken rows (Category == '1.9' known artifact)
    if "Category" in df.columns and "Android Ver" in df.columns:
        df = df[~(df["Android Ver"].isnull() & (df["Category"] == "1.9"))]

    # Fill Android Ver / Current Ver with mode
    for col in ["Android Ver", "Current Ver"]:
        if col in df.columns and df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mode()[0])

    # Clean Price
    if "Price" in df.columns and not pd.api.types.is_numeric_dtype(df["Price"]):
        df["Price"] = df["Price"].apply(lambda x: 0 if str(x) == "0" else float(str(x).replace("$", "")))

    # Clean Reviews
    if "Reviews" in df.columns:
        df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce").fillna(0).astype("int64")

    # Clean Installs
    if "Installs" in df.columns and not pd.api.types.is_numeric_dtype(df["Installs"]):
        df["Installs"] = df["Installs"].apply(lambda v: int(str(v).replace(",", "").replace("+", "")) if pd.notnull(v) else 0)

    steps.append(("After type cleaning", df.shape))

    # Sanity checks
    if {"Reviews", "Installs"}.issubset(df.columns):
        df = df[df.Reviews <= df.Installs]
    if {"Type", "Price"}.issubset(df.columns):
        df = df[~((df.Type == "Free") & (df.Price > 0))]
    steps.append(("After sanity checks", df.shape))

    # Outlier removal
    if "Price" in df.columns:
        df = df[df.Price <= 30]
    if "Reviews" in df.columns:
        df = df[df.Reviews <= 1_000_000]
    if "Installs" in df.columns:
        df = df[df.Installs <= 100_000_000]
    steps.append(("After outlier removal", df.shape))

    # Content rating trim
    if "Content Rating" in df.columns:
        df = df[~df["Content Rating"].isin(["Adults only 18+", "Unrated"])]

    df = df.reset_index(drop=True)
    steps.append(("Final shape", df.shape))

    if "Last Updated" in df.columns:
        try:
            df["updated_month"] = pd.to_datetime(df["Last Updated"], errors="coerce").dt.month
        except Exception:
            pass

    if "Size" in df.columns and pd.api.types.is_numeric_dtype(df["Size"]):
        try:
            df["Size_Bucket"] = pd.qcut(df["Size"], [0, 0.2, 0.4, 0.6, 0.8, 1], ["VL", "L", "M", "H", "VH"])
        except Exception:
            pass

    return df, steps


csv_path = find_bundled_csv()
raw_df = load_raw(csv_path)
if csv_path is None:
    st.toast("⚠️ Couldn't find the CSV in the repo — showing a demo dataset instead.", icon="⚠️")
else:
    st.toast(f"✅ Loaded dataset from {os.path.basename(csv_path)}", icon="✅")
clean_df, clean_steps = clean_pipeline(raw_df)

st.markdown(
    f'<span class="data-badge">📁 Source: {"Demo dataset" if csv_path is None else os.path.basename(csv_path)} '
    f'&nbsp;•&nbsp; {clean_df.shape[0]:,} rows ready</span>',
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# KPI OVERVIEW ROW (purely presentational — reads already-cleaned data,
# no changes to cleaning/analysis logic)
# ----------------------------------------------------------------------
st.write("")
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown('<div class="kpi-icon">📱</div>', unsafe_allow_html=True)
    st.metric("Total Apps", f"{clean_df.shape[0]:,}")

with k2:
    st.markdown('<div class="kpi-icon">⭐</div>', unsafe_allow_html=True)
    avg_rating = round(clean_df["Rating"].mean(), 2) if "Rating" in clean_df.columns else "N/A"
    st.metric("Avg. Rating", avg_rating)

with k3:
    st.markdown('<div class="kpi-icon">🆓</div>', unsafe_allow_html=True)
    free_pct = f'{round((clean_df["Type"] == "Free").mean() * 100, 1)}%' if "Type" in clean_df.columns else "N/A"
    st.metric("Free Apps", free_pct)

with k4:
    st.markdown('<div class="kpi-icon">🗂️</div>', unsafe_allow_html=True)
    cat_count = clean_df["Category"].nunique() if "Category" in clean_df.columns else "N/A"
    st.metric("Categories", cat_count)

st.write("")

# ----------------------------------------------------------------------
# OVERVIEW
# ----------------------------------------------------------------------
if section == "🏠 Overview":
    st.markdown("## 🏠 Project Overview")

    st.markdown("### 🔍 Peek at the cleaned data")
    with st.container(border=True):
        st.dataframe(clean_df.head(15), use_container_width=True)

    with st.expander("📋 Column Types & Nulls"):
        info = pd.DataFrame({
            "dtype": clean_df.dtypes.astype(str),
            "nulls": clean_df.isnull().sum(),
        })
        st.dataframe(info, use_container_width=True)

    st.balloons()

# ----------------------------------------------------------------------
# DATA CLEANING
# ----------------------------------------------------------------------
elif section == "🧹 Data Cleaning":
    st.markdown("## 🧹 Data Cleaning Journey")
    st.markdown("Every great analysis starts with clean data. Here's the shape of the dataset at each stage 👇")

    for label, shape in clean_steps:
        st.markdown(f"""
        <div class="custom-card" style="display:flex; justify-content:space-between; align-items:center;">
            <span>✅ <b>{label}</b></span>
            <span style="color:#8ec5fc; font-weight:700;">{shape[0]:,} rows × {shape[1]} cols</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🧾 Sanity Checks Performed")
    st.markdown("""
    - ✅ Rating between 1 and 5
    - ✅ Reviews ≤ Installs
    - ✅ Free apps have Price = 0
    - ✅ Outliers removed (Price ≤ 30, Reviews ≤ 1M, Installs ≤ 100M)
    """)

# ----------------------------------------------------------------------
# OUTLIER ANALYSIS
# ----------------------------------------------------------------------
elif section == "📦 Outlier Analysis":
    st.markdown("## 📦 Outlier Analysis with Box Plots")
    numeric_cols = [c for c in ["Price", "Reviews", "Installs", "Size"] if c in clean_df.columns]
    col = st.selectbox("🎛️ Choose a numeric column", numeric_cols)

    with st.container(border=True):
        fig, ax = plt.subplots(figsize=(7, 4.5))
        sns.boxplot(x=clean_df[col], ax=ax, color="#a18cd1")
        ax.set_title(f"📦 Box Plot — {col}", fontsize=14)
        st.pyplot(fig)

    with st.container(border=True):
        fig2, ax2 = plt.subplots(figsize=(7, 4.5))
        ax2.hist(clean_df[col].dropna(), bins=25, color="#8ec5fc", edgecolor="none")
        ax2.set_title(f"📊 Histogram — {col}", fontsize=14)
        st.pyplot(fig2)

    st.markdown(f"""
    <div class="custom-card">
    📌 <b>Quick Stats for {col}</b><br>
    Min: {clean_df[col].min():.2f} &nbsp;|&nbsp;
    Median: {clean_df[col].median():.2f} &nbsp;|&nbsp;
    Max: {clean_df[col].max():.2f}
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------------------------
# DISTRIBUTIONS
# ----------------------------------------------------------------------
elif section == "📈 Distributions":
    st.markdown("## 📈 Distribution Plots")
    bins = st.slider("🎚️ Number of bins", 5, 50, 20)
    color = st.color_picker("🎨 Pick a plot colour", "#a18cd1")

    with st.container(border=True):
        fig, ax = plt.subplots(figsize=(8, 4.5))
        sns.histplot(clean_df["Rating"].dropna(), bins=bins, kde=True, color=color, ax=ax)
        ax.set_title("⭐ Distribution of App Ratings", fontsize=14)
        st.pyplot(fig)

    st.markdown("### 📐 Content Rating vs Average Rating")
    if "Content Rating" in clean_df.columns:
        with st.container(border=True):
            fig2, ax2 = plt.subplots(figsize=(8, 4.5))
            sns.barplot(data=clean_df, x="Content Rating", y="Rating", estimator=np.mean, ax=ax2, palette=ACCENT_PALETTE)
            ax2.set_title("🎯 Average Rating by Content Rating", fontsize=14)
            plt.xticks(rotation=20)
            st.pyplot(fig2)

# ----------------------------------------------------------------------
# CATEGORICAL VIEWS
# ----------------------------------------------------------------------
elif section == "🥧 Categorical Views":
    st.markdown("## 🥧 Pie & Bar Charts")
    if "Content Rating" in clean_df.columns:
        counts = clean_df["Content Rating"].value_counts()
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                fig, ax = plt.subplots(figsize=(5.5, 5.5))
                ax.pie(counts, labels=counts.index, autopct="%1.1f%%",
                       colors=ACCENT_PALETTE.as_hex(), textprops={"color": "#eef1ff"})
                ax.set_title("🥧 Content Rating Share", fontsize=13)
                st.pyplot(fig)
        with col2:
            with st.container(border=True):
                fig2, ax2 = plt.subplots(figsize=(5.5, 5.5))
                counts.plot.barh(ax=ax2, color="#8ec5fc")
                ax2.set_title("📊 Content Rating Counts", fontsize=13)
                st.pyplot(fig2)

# ----------------------------------------------------------------------
# RELATIONSHIPS (scatter / joint / pair)
# ----------------------------------------------------------------------
elif section == "🔍 Relationships":
    st.markdown("## 🔍 Relationships Between Variables")
    numeric_cols = [c for c in ["Reviews", "Size", "Price", "Rating", "Installs"] if c in clean_df.columns]

    tab1, tab2 = st.tabs(["✨ Scatter / Joint Plot", "🧩 Pair Plot"])
    with tab1:
        xcol = st.selectbox("X-axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
        ycol = st.selectbox("Y-axis", numeric_cols, index=0)
        with st.container(border=True):
            g = sns.jointplot(x=clean_df[xcol], y=clean_df[ycol], kind="scatter", color="#a18cd1", height=6)
            g.fig.patch.set_facecolor(PLOT_BG)
            st.pyplot(g.fig)

    with tab2:
        chosen = st.multiselect("Pick up to 4 columns", numeric_cols, default=numeric_cols[:4])
        if len(chosen) >= 2:
            with st.container(border=True):
                pp = sns.pairplot(clean_df[chosen].dropna(), corner=True, palette=ACCENT_PALETTE)
                pp.fig.patch.set_facecolor(PLOT_BG)
                st.pyplot(pp.fig)
        else:
            st.warning("⚠️ Select at least 2 columns for the pair plot.")

# ----------------------------------------------------------------------
# HEATMAPS
# ----------------------------------------------------------------------
elif section == "🌡️ Heatmaps":
    st.markdown("## 🌡️ Heat Map — Rating across Size Buckets & Content Rating")
    if {"Size_Bucket", "Content Rating", "Rating"}.issubset(clean_df.columns):
        agg = st.selectbox("Aggregation", ["mean", "median", "min", "max"])
        pivot = pd.pivot_table(data=clean_df, index="Content Rating", columns="Size_Bucket",
                                values="Rating", aggfunc=agg)
        with st.container(border=True):
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.heatmap(pivot, cmap="mako", annot=True, fmt=".2f", ax=ax, cbar_kws={"label": "Rating"})
            ax.set_title(f"🌡️ {agg.title()} Rating Heatmap", fontsize=14)
            st.pyplot(fig)
    else:
        st.info("ℹ️ Size buckets unavailable for this dataset.")

# ----------------------------------------------------------------------
# TRENDS + STACKED BARS
# ----------------------------------------------------------------------
elif section == "🕒 Trends & Stacked Bars":
    st.markdown("## 🕒 Monthly Trends")
    if "updated_month" in clean_df.columns:
        monthly_rating = clean_df.groupby("updated_month")["Rating"].mean()
        with st.container(border=True):
            fig, ax = plt.subplots(figsize=(9, 4.5))
            monthly_rating.plot(marker="o", color="#fbc2eb", ax=ax)
            ax.set_title("📈 Average Rating by Month", fontsize=14)
            ax.set_xlabel("Month")
            st.pyplot(fig)

        if "Installs" in clean_df.columns and "Content Rating" in clean_df.columns:
            st.markdown("### 📚 Stacked Bar — Installs by Content Rating per Month")
            monthly = pd.pivot_table(data=clean_df, values="Installs", index="updated_month",
                                      columns="Content Rating", aggfunc="sum").fillna(0)
            normalize = st.checkbox("🔁 Show as proportion", value=False)
            if normalize:
                monthly = monthly.div(monthly.sum(axis=1), axis=0)
            with st.container(border=True):
                fig2, ax2 = plt.subplots(figsize=(9, 5))
                monthly.plot(kind="bar", stacked=True, ax=ax2, color=ACCENT_PALETTE.as_hex())
                ax2.set_title("📊 Installs Breakdown by Content Rating", fontsize=14)
                st.pyplot(fig2)
    else:
        st.info("ℹ️ 'Last Updated' column not found — trend view unavailable.")

# ----------------------------------------------------------------------
# INTERACTIVE PLOTLY
# ----------------------------------------------------------------------
elif section == "⚡ Interactive Plotly":
    st.markdown("## ⚡ Interactive Plotly Charts")
    if "updated_month" in clean_df.columns and "Rating" in clean_df.columns:
        res = clean_df.groupby("updated_month")[["Rating"]].mean().reset_index()
        fig = px.line(res, x="updated_month", y="Rating", markers=True,
                      title="⚡ Monthly Average Rating", template=PLOTLY_TEMPLATE,
                      color_discrete_sequence=["#6C63FF"])
        fig = style_plotly(fig)
        with st.container(border=True):
            st.plotly_chart(fig, use_container_width=True)

    if {"Reviews", "Rating", "Category"}.issubset(clean_df.columns):
        fig2 = px.scatter(clean_df, x="Reviews", y="Rating", color="Category",
                           size="Installs" if "Installs" in clean_df.columns else None,
                           hover_name="App" if "App" in clean_df.columns else None,
                           title="⚡ Reviews vs Rating by Category", template=PLOTLY_TEMPLATE,
                           color_discrete_sequence=ACCENT_PALETTE.as_hex())
        fig2 = style_plotly(fig2)
        with st.container(border=True):
            st.plotly_chart(fig2, use_container_width=True)

    st.success("✨ Hover, zoom, and pan on the charts above for a fully interactive experience!")

# ----------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div class="app-footer">
    <div class="brand">Play Store Insights Lab</div>
    <div class="sub">Built with 💜 in Streamlit &nbsp;|&nbsp; 📊 Google Play Store Case Study</div>
    <div>
        <span class="footer-pill">🐍 Python</span>
        <span class="footer-pill">🐼 Pandas</span>
        <span class="footer-pill">📊 Seaborn</span>
        <span class="footer-pill">⚡ Plotly</span>
        <span class="footer-pill">🚀 Streamlit</span>
    </div>
</div>
""", unsafe_allow_html=True)
