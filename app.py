import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
import re
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import warnings
import pyarrow
warnings.filterwarnings('ignore')

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Analyse Météo Maroc Pro",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== OPTIMIZED STYLING ====================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [class*="css"] {
        font-family: 'Open Sans', sans-serif;
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1428 100%);
        color: #ffffff;
    }
    
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1428 100%);
        padding: 2rem 1.5rem;
    }
    
    /* ===== HEADERS ===== */
    h1 {
        font-size: 2.5rem;
        color: #00f0ff;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-size: 1.8rem;
        color: #00f0ff;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-size: 1.3rem;
        color: #00ccff;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }
    
    h4 {
        font-size: 1.1rem;
        color: #00ccff;
        font-weight: 600;
        margin-top: 0.8rem;
        margin-bottom: 0.6rem;
    }
    
    /* ===== BODY TEXT ===== */
    p, span, div, label {
        font-size: 1rem;
        color: #ffffff;
        line-height: 1.6;
    }
    
    /* ===== METRIC CARDS ===== */
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.1) 0%, rgba(0, 136, 255, 0.1) 100%);
        border: 1px solid rgba(0, 240, 255, 0.3);
        border-radius: 8px;
        padding: 0.5rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 4px 16px rgba(0, 240, 255, 0.1);
        transition: all 0.3s ease;
        text-align: center;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .metric-card:hover {
        border-color: rgba(0, 240, 255, 0.6);
        box-shadow: 0 8px 24px rgba(0, 240, 255, 0.2);
        transform: translateY(-2px);
    }
    
    /* ===== STAT VALUES ===== */
    .stat-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #00f0ff;
        margin: 0.1rem 0;
        white-space: nowrap;
    }
    
    .stat-label {
        font-size: 0.7rem;
        color: #b0c4de;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.2rem;
        font-weight: 500;
        line-height: 1.2;
    }
        font-weight: 500;
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 14, 39, 0.95) 0%, rgba(26, 31, 58, 0.95) 100%);
        border-right: 1px solid rgba(0, 240, 255, 0.2);
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.1) 0%, rgba(0, 136, 255, 0.1) 100%);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 1px solid rgba(0, 240, 255, 0.2);
        gap: 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        border-bottom: 3px solid #00f0ff !important;
    }
    
    /* ===== FILTERS & INPUTS ===== */
    .stSelectbox, .stDateInput, .stMultiSelect {
        color: white !important;
    }
    
    /* Input Container Styling */
    .stSelectbox div[data-baseweb="select"] > div,
    .stDateInput div[data-baseweb="input"] > div {
        background-color: rgba(10, 14, 39, 0.6) !important;
        border: 1px solid rgba(0, 240, 255, 0.3) !important;
        border-radius: 8px !important;
        color: white !important;
        transition: all 0.3s ease;
    }
    
    /* Hover State */
    .stSelectbox div[data-baseweb="select"] > div:hover,
    .stDateInput div[data-baseweb="input"] > div:hover {
        border-color: rgba(0, 240, 255, 0.8) !important;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
    }
    
    /* Text Color inside Inputs */
    .stSelectbox div[data-baseweb="select"] span,
    .stDateInput input {
        color: #ffffff !important;
        font-weight: 500;
    }
    
    /* Dropdown/Popover Styling (Best Effort) */
    div[data-baseweb="popover"], div[data-baseweb="menu"] {
        background-color: #0f1428 !important;
        border: 1px solid rgba(0, 240, 255, 0.3) !important;
    }
    
    div[data-baseweb="option"] {
        color: white !important;
    }
    
    div[data-baseweb="option"]:hover, div[aria-selected="true"] {
        background-color: rgba(0, 240, 255, 0.2) !important;
        font-weight: bold;
    }
    
    /* Label Styling */
    .stSelectbox label, .stDateInput label {
        color: #00ccff !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }
    
    /* Icons (Calendar, Arrows) */
    .stDateInput svg, .stSelectbox svg {
        fill: #00f0ff !important;
    }
    
    /* ===== BUTTON ===== */
    .stButton > button {
        background: linear-gradient(135deg, #00f0ff 0%, #0088ff 100%);
        color: #0a0e27;
        border: none;
        border-radius: 8px;
        font-weight: 700;
        padding: 0.8rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 8px 20px rgba(0, 240, 255, 0.3);
        transform: translateY(-2px);
    }
    
    /* ===== DIVIDER ===== */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 240, 255, 0.2), transparent);
        margin: 2rem 0;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 240, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(0, 240, 255, 0.3);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 240, 255, 0.5);
    }
    
    /* ===== DATAFRAME ===== */
    .stDataFrame {
        font-size: 1rem !important;
    }
    
    /* ===== EXPANDER ===== */
    .stExpander {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.05) 0%, rgba(0, 136, 255, 0.05) 100%);
        border: 1px solid rgba(0, 240, 255, 0.15);
        border-radius: 8px;
    }
    
    /* ===== HIGHLIGHT BOXES ===== */
    .highlight-box {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(0, 240, 255, 0.1) 100%);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(255, 200, 0, 0.1) 0%, rgba(255, 100, 0, 0.1) 100%);
        border: 1px solid rgba(255, 150, 0, 0.3);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== CACHE & UTILITIES ====================

# ==================== CITY COORDINATES ====================
CITY_COORDS = {
    "Agadir": [30.4278, -9.5981],
    "Al Hoceima": [35.2517, -3.9372],
    "Assilah": [35.4667, -6.0333],
    "Azilal": [31.9667, -6.5667],
    "Azrou": [33.4333, -5.2167],
    "Beni Mellal": [32.3333, -6.35],
    "Berkane": [34.9167, -2.3167],
    "Boujdour": [26.12, -14.48],
    "Casablanca": [33.5731, -7.5898],
    "Chefchaouen": [35.1714, -5.2691],
    "Chichaoua": [31.5333, -8.7667],
    "Dakhla": [23.6848, -15.9579],
    "Demnate": [31.7311, -6.9583],
    "El Jadida": [33.2333, -8.5],
    "Essaouira": [31.5125, -9.77],
    "Fes": [34.0181, -5.0078],
    "Guelmim": [28.9833, -10.0667],
    "Kasba Tadla": [32.5972, -6.2653],
    "Kel At Mgouna": [31.2403, -6.1264],
    "Kenitra": [34.2530, -6.5891],
    "Khemisset": [33.8167, -6.0667],
    "Khouribga": [32.8833, -6.9167],
    "Ksar El Kebir": [35.0, -6.1833],
    "La Youne": [27.1500, -13.2000],
    "Larache": [35.1833, -6.15],
    "Marrakech": [31.6295, -7.9811],
    "Meknes": [33.8933, -5.5547],
    "Mohammedia": [33.6833, -7.3833],
    "Oued Zem": [32.8667, -6.5667],
    "Ouezzane": [34.8, -5.5833],
    "Rabat": [34.0209, -6.8416],
    "Safi": [32.2994, -9.2372],
    "Saidia": [35.0833, -2.2333],
    "Sefrou": [33.8333, -4.8333],
    "Settat": [33.0, -7.6167],
    "Sidi Bennour": [32.65, -8.4333],
    "Sidi Ifni": [29.3833, -10.1833],
    "Sidi Slimane": [34.26, -5.92],
    "Tanger": [35.7595, -5.8340],
    "Taounate": [34.5333, -4.6333],
    "Tarfaya": [27.9333, -12.9167],
    "Taroudant": [30.47, -8.87],
    "Tetouan": [35.5889, -5.3626],
    "Tinghir": [31.5167, -5.5333],
}

# ==================== CACHE & UTILITIES ====================

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data(file_path):
    """
    Charge les données avec optimisations de performance.
    Priorise le format Parquet pour un chargement instantané.
    """
    parquet_path = file_path.replace('.csv', '.parquet')
    
    # Si le parquet n'existe pas, on le crée une seule fois
    if not os.path.exists(parquet_path) and os.path.exists(file_path):
        with st.spinner('📦 Optimisation de la base de données (Conversion CSV -> Parquet)...'):
            df_temp = pd.read_csv(file_path, parse_dates=['DATE'])
            # Conversion optimisée des types
            for col in df_temp.select_dtypes(include=['float64']).columns:
                df_temp[col] = df_temp[col].astype('float32')
            df_temp.to_parquet(parquet_path, engine='pyarrow', compression='snappy')
    
    # Charger depuis Parquet (beaucoup plus rapide)
    if os.path.exists(parquet_path):
        return pd.read_parquet(parquet_path)
    
    # Fallback CSV si Parquet échoue
    df = pd.read_csv(
        file_path, 
        dtype={
            'MAX_TEMPERATURE_C': 'float32',
            'MIN_TEMPERATURE_C': 'float32',
            # ... autres types déjà optimisés en float32 par défaut si on lit du CSV
        },
        parse_dates=['DATE']
    )
    numeric_cols = df.select_dtypes(include=['float64']).columns
    df[numeric_cols] = df[numeric_cols].astype('float32')
    return df

def get_city_name(filename):
    match = re.search(r'export-(.*)0\.csv', filename)
    if match:
        return match.group(1).replace('-', ' ').title()
    return filename

@st.cache_data
def calculate_weather_insights(df):
    insights = {
        'avg_temp': df['MAX_TEMPERATURE_C'].mean(),
        'temp_volatility': df['MAX_TEMPERATURE_C'].std(),
        'humidity_avg': df['HUMIDITY_MAX_PERCENT'].mean(),
        'rainy_days_pct': (len(df[df['PRECIP_TOTAL_DAY_MM'] > 0]) / len(df)) * 100,
        'avg_wind': df['WINDSPEED_MAX_KMH'].mean(),
        'sunny_days': len(df[df['SUNHOUR'] > 8]),
        'total_precipitation': df['PRECIP_TOTAL_DAY_MM'].sum(),
    }
    return insights

def create_metric_col(label, value, unit="", icon=""):
    return f"""
    <div class="metric-card">
        <div style="font-size: 1rem; margin-bottom: 0.1rem;">{icon}</div>
        <div class="stat-value">{value}{unit}</div>
        <div class="stat-label">{label}</div>
    </div>
    """

# ==================== DATA LOADING (OPTIMIZED) ====================

from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent if '__file__' in globals() else Path.cwd()
DATA_DIR = str(SCRIPT_DIR)

MERGED_DATA_FILE = os.path.join(DATA_DIR, 'data', 'morocco_weather_data_merged.csv')

@st.cache_data(ttl=3600)
def get_all_data():
    if not os.path.exists(MERGED_DATA_FILE):
        return None
    return load_data(MERGED_DATA_FILE)

# Spinner de chargement global initial
with st.spinner('🚀 Initialisation des données météorologiques du Maroc...'):
    full_df = get_all_data()

if full_df is None:
    st.error("⚠️ Fichier de données fusionné manquant. Veuillez exécuter merge_data.py.")
    st.stop()

# Liste des villes unique directement du DataFrame
available_cities = sorted(full_df['CITY'].unique())
cities = {city: city for city in available_cities}


# ==================== SIDEBAR ====================

st.sidebar.markdown("""
    <div class="sidebar-header">
        <h3 style="margin: 0; font-size: 1.3rem; color: #00f0ff;">⚙️ CONFIGURATION</h3>
        <p style="color: #b0c4de; margin-top: 0.3rem; font-size: 0.95rem;">Filtres et Paramètres</p>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("### 🌍 Sélection Ville")
selected_city_name = st.sidebar.selectbox(
    "Ville Principale",
    options=list(cities.keys()),
    index=list(cities.keys()).index("Agadir") if "Agadir" in cities else 0
)

comparison_mode = st.sidebar.toggle("🤝 Mode Comparaison", value=False)
selected_city_2_name = None
if comparison_mode:
    selected_city_2_name = st.sidebar.selectbox(
        "Ville de Comparaison",
        options=[c for c in cities.keys() if c != selected_city_name]
    )

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 Navigation")
menu_selection = st.sidebar.selectbox(
    "Section à afficher",
    options=[
        "📊 TABLEAU DE BORD", "🌡️ TEMPÉRATURE", "💧 PRÉCIPITATIONS", 
        "🌬️ ATMOSPHÈRE", "☀️ SOLAIRE", "📈 TENDANCES", 
        "🔗 CORRÉLATIONS", "📉 STATISTIQUES", "🎯 ANOMALIES", 
        "🔮 PRÉVISIONS", "📋 EXPLORATION", "⚡ ANALYSES IA"
    ],
    index=0
)

st.sidebar.markdown("### 📅 Période")
# Get date range from memory
min_date = full_df['DATE'].min()
max_date = full_df['DATE'].max()

date_selection = st.sidebar.date_input(
    "Plage de dates",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Process Data for City 1 from memory
with st.spinner(f'🎯 Filtrage pour {selected_city_name}...'):
    df = full_df[full_df['CITY'] == selected_city_name]
    
if len(date_selection) == 2:
    start_date, end_date = date_selection
    filtered_df = df[(df['DATE'] >= pd.Timestamp(start_date)) & (df['DATE'] <= pd.Timestamp(end_date))].copy()
else:
    filtered_df = df.copy()

# Process Data for City 2 if enabled from memory
filtered_df_2 = None
if comparison_mode and selected_city_2_name:
    with st.spinner(f'🤝 Comparaison avec {selected_city_2_name}...'):
        df2 = full_df[full_df['CITY'] == selected_city_2_name]
        
    if len(date_selection) == 2:
        filtered_df_2 = df2[(df2['DATE'] >= pd.Timestamp(start_date)) & (df2['DATE'] <= pd.Timestamp(end_date))].copy()
    else:
        filtered_df_2 = df2.copy()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Statistiques")
stats_col1, stats_col2 = st.sidebar.columns(2)
stats_col1.metric("Jours", len(filtered_df))
stats_col2.metric("Années", filtered_df['DATE'].dt.year.nunique())

st.sidebar.info(f"🚀 **App Optimisée**: {menu_selection} seule est calculée. Chargement via Parquet actif.")

insights = calculate_weather_insights(filtered_df)
insights_2 = calculate_weather_insights(filtered_df_2) if filtered_df_2 is not None else None

# ==================== MAIN CONTENT ====================

if comparison_mode and selected_city_2_name:
    st.markdown(f'<h1 style="text-align: center; font-size: 2.5rem;">🌍 {selected_city_name} vs {selected_city_2_name}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; font-size: 1.1rem; color: #b0c4de;">Analyse Comparative Professionnelle • {len(filtered_df)} jours</p>', unsafe_allow_html=True)
else:
    st.markdown(f'<h1 style="text-align: center; font-size: 2.5rem;">🌍 {selected_city_name}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; font-size: 1.1rem; color: #b0c4de;">Analyse Météorologique Complète • {len(filtered_df)} jours • 34 variables</p>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("## 📈 Indicateurs Clés")

if not comparison_mode:
    # Row 1: All 10 Metrics
    cols = st.columns(10)
    
    metrics = [
        ("Temp Moy", f"{insights['avg_temp']:.1f}", "°C", "🌡️"),
        ("Volatilité", f"{insights['temp_volatility']:.1f}", "°C", "📊"),
        ("Humidité", f"{insights['humidity_avg']:.0f}", "%", "💧"),
        ("Pluie %", f"{insights['rainy_days_pct']:.1f}", "%", "🌧️"),
        ("Vent Moy", f"{insights['avg_wind']:.1f}", "km/h", "💨"),
        ("Soleil", f"{insights['sunny_days']}", "j", "☀️"),
        ("Max", f"{filtered_df['MAX_TEMPERATURE_C'].max():.1f}", "°C", "🔥"),
        ("Min", f"{filtered_df['MIN_TEMPERATURE_C'].min():.1f}", "°C", "❄️"),
        ("Pluie Tot", f"{filtered_df['PRECIP_TOTAL_DAY_MM'].sum():.0f}", "mm", "💦"),
        ("Ensoleil", f"{filtered_df['SUNHOUR'].mean():.1f}", "h", "🌅")
    ]
    
    for i, col in enumerate(cols):
        with col:
            st.markdown(create_metric_col(*metrics[i]), unsafe_allow_html=True)

else:
    # Comparison metrics table
    metrics_data = {
        "Indicateur": ["Temp Moy (°C)", "Volatilité (°C)", "Humidité (%)", "Jours Pluie (%)", "Vent Moy (km/h)", "Pluie Total (mm)", "Soleil Moy (h)"],
        selected_city_name: [
            f"{insights['avg_temp']:.1f}", f"{insights['temp_volatility']:.1f}", f"{insights['humidity_avg']:.0f}", 
            f"{insights['rainy_days_pct']:.1f}", f"{insights['avg_wind']:.1f}", f"{insights['total_precipitation']:.1f}", f"{filtered_df['SUNHOUR'].mean():.1f}"
        ],
        selected_city_2_name: [
            f"{insights_2['avg_temp']:.1f}", f"{insights_2['temp_volatility']:.1f}", f"{insights_2['humidity_avg']:.0f}", 
            f"{insights_2['rainy_days_pct']:.1f}", f"{insights_2['avg_wind']:.1f}", f"{insights_2['total_precipitation']:.1f}", f"{filtered_df_2['SUNHOUR'].mean():.1f}"
        ]
    }
    st.table(pd.DataFrame(metrics_data))

st.markdown("---")

# ==================== PIE CHART SECTION ====================

st.markdown("## 📊 Distribution des Types Météo")

col_pie1, col_pie2 = st.columns([1.5, 1])

with col_pie1:
    st.markdown("### Résumé Avis Météo")
    
    opinion_counts = filtered_df['OPINION'].value_counts()
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=opinion_counts.index,
        values=opinion_counts.values,
        marker=dict(
            colors=['#00f0ff', '#0088ff', '#00ff88', '#ffaa00', '#ff6b6b', '#ff00ff'],
            line=dict(color='#0a0e27', width=2)
        ),
        textposition='inside',
        textinfo='label+percent',
        textfont=dict(size=11, color='white', family='Open Sans'),
        hovertemplate='<b>%{label}</b><br>Jours: <b>%{value}</b><extra></extra>',
    )])
    
    fig_pie.update_layout(
        height=350,
        template='plotly_dark',
        paper_bgcolor='rgba(10, 14, 39, 0.5)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='#ffffff', family='Open Sans', size=11),
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(font=dict(color="white", size=11))
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

with col_pie2:
    st.markdown("### Détails")
    
    opinion_stats = []
    for opinion in opinion_counts.index:
        count = opinion_counts[opinion]
        percentage = (count / len(filtered_df)) * 100
        opinion_stats.append({
            'Avis': opinion,
            'Jours': f"{count}",
            'Pourcentage': f"{percentage:.1f}%"
        })
    
    stats_df = pd.DataFrame(opinion_stats)
    st.dataframe(stats_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ==================== MAIN TABS ====================

# ==================== DYNAMIC CONTENT (LAZY LOADING) ====================
# We use conditional logic instead of st.tabs to ensure only the active section is processed
# This drastically reduces memory usage and execution time per rerun.

if menu_selection == "📊 TABLEAU DE BORD":
    # Section: Dashboard
    if True: 
        st.markdown("### Tableau de Bord")
        
        # Top: Précipitations & Vent
        st.markdown("#### 🌧️ Précipitations & Vent")
        base_pw = alt.Chart(filtered_df).encode(x=alt.X('DATE:T', title='Date'))
        bars = base_pw.mark_bar(opacity=0.7, color='#00f0ff').encode(
            y=alt.Y('PRECIP_TOTAL_DAY_MM:Q', title='Précipitations (mm)'),
            tooltip=['DATE:T', 'PRECIP_TOTAL_DAY_MM:Q']
        )
        line = base_pw.mark_line(stroke='#ff6b6b', strokeWidth=2).encode(
            y=alt.Y('WINDSPEED_MAX_KMH:Q', title='Vent Max (km/h)'),
            tooltip=['DATE:T', 'WINDSPEED_MAX_KMH:Q']
        )
        chart_pw = alt.layer(bars, line).resolve_scale(y='independent').properties(
            height=350
        ).interactive()
        st.altair_chart(chart_pw, use_container_width=True)

        st.markdown("---")
        
        # Bottom: Localisation
        st.markdown("#### 🗺️ Localisation")
        map_data = []
        if selected_city_name in CITY_COORDS:
            map_data.append({
                "city": selected_city_name,
                "lat": CITY_COORDS[selected_city_name][0],
                "lon": CITY_COORDS[selected_city_name][1],
                "color": [0, 240, 255, 200],
                "size": 10000
            })
        if comparison_mode and selected_city_2_name in CITY_COORDS:
            map_data.append({
                "city": selected_city_2_name,
                "lat": CITY_COORDS[selected_city_2_name][0],
                "lon": CITY_COORDS[selected_city_2_name][1],
                "color": [255, 107, 107, 200],
                "size": 10000
            })
        if map_data:
            import pydeck as pdk
            view_state = pdk.ViewState(
                latitude=31.7917,
                longitude=-7.0926,
                zoom=4,
                pitch=0
            )
            layer = pdk.Layer(
                "ScatterplotLayer",
                pd.DataFrame(map_data),
                get_position=["lon", "lat"],
                get_color="color",
                get_radius="size",
                pickable=True,
            )
            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/dark-v9",
                initial_view_state=view_state,
                layers=[layer],
                tooltip={"text": "{city}"}
            ), use_container_width=True)
        else:
            st.info("Coordonnées non disponibles.")

    st.markdown("---")
    
    st.markdown("#### 📅 Timeline Température")
    
    if not comparison_mode:
        base = alt.Chart(filtered_df).encode(x=alt.X('DATE:T', title='Date'))
        temp_area = base.mark_area(
            line={'color':'#00f0ff'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='rgba(0, 240, 255, 0.2)', offset=0), 
                        alt.GradientStop(color='#00f0ff', offset=1)],
                x1=1, x2=1, y1=1, y2=0
            ),
            opacity=0.7
        ).encode(y=alt.Y('MAX_TEMPERATURE_C:Q', title='Température (°C)')).properties(height=350)
        st.altair_chart(temp_area, use_container_width=True)
    else:
        # Comparison Chart
        df1_comp = filtered_df[['DATE', 'MAX_TEMPERATURE_C']].copy()
        df1_comp['Ville'] = selected_city_name
        df2_comp = filtered_df_2[['DATE', 'MAX_TEMPERATURE_C']].copy()
        df2_comp['Ville'] = selected_city_2_name
        comp_df = pd.concat([df1_comp, df2_comp])
        
        comp_chart = alt.Chart(comp_df).mark_line(size=2).encode(
            x=alt.X('DATE:T', title='Date'),
            y=alt.Y('MAX_TEMPERATURE_C:Q', title='Température (°C)'),
            color=alt.Color('Ville:N', scale=alt.Scale(domain=[selected_city_name, selected_city_2_name], range=['#00f0ff', '#ff6b6b'])),
            tooltip=['DATE:T', 'Ville:N', 'MAX_TEMPERATURE_C:Q']
        ).properties(height=350).interactive()
        st.altair_chart(comp_chart, use_container_width=True)

# ==================== TAB 2: TEMPERATURE ====================

elif menu_selection == "🌡️ TEMPÉRATURE":
    st.markdown("### Analyse Température")
    
    st.markdown("#### Évolution Diurne")
    
    hourly_cols = [
        'TEMPERATURE_MORNING_C_6H', 'TEMPERATURE_9H', 'TEMPERATURE_NOON_C_12H',
        'TEMPERATURE_15H', 'TEMPERATURE_EVENING_C_18H', 'TEMPERATURE_21H',
        'TEMPERATURE_NIGHT_C_3H', 'TEMPERATURE_MIDNIGHT_0H'
    ]
    
    temp_long = filtered_df.melt(
        id_vars=['DATE'],
        value_vars=hourly_cols,
        var_name='Hour',
        value_name='Temperature'
    )
    
    temp_chart = alt.Chart(temp_long).mark_line(point=True, opacity=0.8, size=2).encode(
        x=alt.X('DATE:T', title='Date'),
        y=alt.Y('Temperature:Q', title='Température (°C)'),
        color=alt.Color('Hour:N', scale=alt.Scale(scheme='spectral')),
        tooltip=['DATE:T', 'Hour:N', 'Temperature:Q']
    ).properties(height=380).interactive()
    
    st.altair_chart(temp_chart, use_container_width=True)
    
    st.markdown("---")
    
    col_tables1, col_tables2 = st.columns(2)
    
    with col_tables1:
        st.markdown("#### Statistiques")
        
        stats_data = {
            'Métrique': ['Maximum', 'Minimum', 'Moyenne', 'Écart-type'],
            'Valeur': [
                f"{filtered_df['MAX_TEMPERATURE_C'].max():.2f}°C",
                f"{filtered_df['MIN_TEMPERATURE_C'].min():.2f}°C",
                f"{filtered_df['MAX_TEMPERATURE_C'].mean():.2f}°C",
                f"{filtered_df['MAX_TEMPERATURE_C'].std():.2f}°C"
            ]
        }
        
        st.dataframe(pd.DataFrame(stats_data), use_container_width=True, hide_index=True)
        
    with col_tables2:
        st.markdown("#### Indices Thermiques")
        
        indices_metrics = {
            'Indice': ['Heat Index Max', 'Wind Chill Min', 'Point de Rosée Max'],
            'Valeur': [
                f"{filtered_df['HEATINDEX_MAX_C'].max():.2f}°C",
                f"{filtered_df['WINDTEMP_MAX_C'].min():.2f}°C",
                f"{filtered_df['DEWPOINT_MAX_C'].max():.2f}°C"
            ]
        }
        
        st.dataframe(pd.DataFrame(indices_metrics), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.markdown("#### Box Plots Saisonniers")
    
    filtered_df_copy = filtered_df.copy()
    filtered_df_copy['Season'] = filtered_df_copy['DATE'].dt.month.apply(
        lambda x: 'Hiver' if x in [12, 1, 2] else 'Printemps' if x in [3, 4, 5] 
        else 'Été' if x in [6, 7, 8] else 'Automne'
    )
    
    fig_season = go.Figure()
    
    for season, color in [('Hiver', '#4ecdc4'), ('Printemps', '#95e1d3'), ('Été', '#ff6b6b'), ('Automne', '#ffa502')]:
        season_data = filtered_df_copy[filtered_df_copy['Season'] == season]['MAX_TEMPERATURE_C']
        fig_season.add_trace(go.Box(
            y=season_data,
            name=season,
            marker_color=color,
            hovertemplate='<b>' + season + '</b><br>Temp: %{y:.1f}°C<extra></extra>'
        ))
    
    fig_season.update_layout(
        height=380,
        template='plotly_dark',
        paper_bgcolor='rgba(10, 14, 39, 0.8)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='#ffffff', family='Open Sans', size=11),
        yaxis_title='Température (°C)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="white", size=10),
            bgcolor="rgba(0,0,0,0)"
        )
    )
    
    st.plotly_chart(fig_season, use_container_width=True)

    st.markdown("#### Tendances Mensuelles")
    
    monthly_temps = filtered_df.copy()
    monthly_temps['Month'] = monthly_temps['DATE'].dt.to_period('M')
    monthly_summary = monthly_temps.groupby('Month')[['MAX_TEMPERATURE_C', 'MIN_TEMPERATURE_C']].mean()
    
    fig_monthly = go.Figure()
    
    fig_monthly.add_trace(go.Scatter(
        x=monthly_summary.index.astype(str),
        y=monthly_summary['MAX_TEMPERATURE_C'],
        name='Temp Max',
        mode='lines+markers',
        line=dict(color='#ff6b6b', width=2),
        marker=dict(size=8),
        hovertemplate='Mois: %{x}<br>Max: <b>%{y:.1f}°C</b><extra></extra>'
    ))
    
    fig_monthly.add_trace(go.Scatter(
        x=monthly_summary.index.astype(str),
        y=monthly_summary['MIN_TEMPERATURE_C'],
        name='Temp Min',
        mode='lines+markers',
        line=dict(color='#4ecdc4', width=2),
        marker=dict(size=8),
        fill='tonexty',
        hovertemplate='Mois: %{x}<br>Min: <b>%{y:.1f}°C</b><extra></extra>'
    ))
    
    fig_monthly.update_layout(
        height=380,
        template='plotly_dark',
        paper_bgcolor='rgba(10, 14, 39, 0.8)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='#ffffff', family='Open Sans', size=11),
        hovermode='x unified',
        yaxis_title='Température (°C)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="white", size=10),
            bgcolor="rgba(0,0,0,0)"
        )
    )
    
    st.plotly_chart(fig_monthly, use_container_width=True)

# ==================== TAB 3: PRECIPITATION ====================

elif menu_selection == "💧 PRÉCIPITATIONS":
    st.markdown("### Analyse Précipitations")
    
    col_p1, col_p2 = st.columns([2, 1])
    
    with col_p1:
        st.markdown("#### Chronologie Pluie")
        
        precip_df = filtered_df[['DATE', 'PRECIP_TOTAL_DAY_MM']].copy()
        precip_df['PRECIP_MA7'] = precip_df['PRECIP_TOTAL_DAY_MM'].rolling(7).mean()
        
        precip_bars = alt.Chart(precip_df).mark_bar(color='#00f0ff', opacity=0.7).encode(
            x=alt.X('DATE:T', title='Date'),
            y=alt.Y('PRECIP_TOTAL_DAY_MM:Q', title='Pluie (mm)'),
            tooltip=['DATE:T', 'PRECIP_TOTAL_DAY_MM:Q']
        ).properties(height=350)
        
        precip_line = alt.Chart(precip_df).mark_line(color='#ff6b6b', size=2).encode(
            x='DATE:T',
            y=alt.Y('PRECIP_MA7:Q', title='Moyenne 7j (mm)', axis=alt.Axis(orient='right'))
        )
        
        combined_p = alt.layer(precip_bars, precip_line).resolve_scale(y='independent')
        st.altair_chart(combined_p, use_container_width=True)
    
    with col_p2:
        st.markdown("#### Jours Pluvieux")
        
        rainy_days = len(filtered_df[filtered_df['PRECIP_TOTAL_DAY_MM'] > 0])
        dry_days = len(filtered_df[filtered_df['PRECIP_TOTAL_DAY_MM'] == 0])
        
        fig_rain = go.Figure(data=[go.Pie(
            labels=['Pluvieux', 'Secs'],
            values=[rainy_days, dry_days],
            marker=dict(colors=['#00f0ff', '#ffa502'], line=dict(color='#0a0e27', width=2)),
            textposition='auto',
            textinfo='label+percent',
            textfont=dict(size=11, color='white'),
            hovertemplate='<b>%{label}</b><br>Jours: <b>%{value}</b><extra></extra>'
        )])
        
        fig_rain.update_layout(
            height=350,
            template='plotly_dark',
            paper_bgcolor='rgba(10, 14, 39, 0.5)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#ffffff', family='Open Sans', size=11)
        )
        
        st.plotly_chart(fig_rain, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("#### Métriques Précipitations")
    
    col_ps1, col_ps2, col_ps3, col_ps4, col_ps5 = st.columns(5)
    
    col_ps1.metric("Pluie Totale", f"{filtered_df['PRECIP_TOTAL_DAY_MM'].sum():.1f} mm")
    col_ps2.metric("Pluie Moy/Jour", f"{filtered_df['PRECIP_TOTAL_DAY_MM'].mean():.2f} mm")
    col_ps3.metric("Pluie Max/Jour", f"{filtered_df['PRECIP_TOTAL_DAY_MM'].max():.1f} mm")
    col_ps4.metric("Jours Pluie", rainy_days)
    col_ps5.metric("Neige Totale", f"{filtered_df['TOTAL_SNOW_MM'].sum():.1f} mm")
    
    st.markdown("---")
    
    st.markdown("#### Distribution Pluie")
    
    fig_precip_hist = go.Figure()
    
    fig_precip_hist.add_trace(go.Histogram(
        x=filtered_df[filtered_df['PRECIP_TOTAL_DAY_MM'] > 0]['PRECIP_TOTAL_DAY_MM'],
        name='Jours Pluvieux',
        marker_color='#00f0ff',
        nbinsx=40,
        hovertemplate='Pluie: %{x:.1f}mm<br>Jours: %{y}<extra></extra>'
    ))
    
    fig_precip_hist.update_layout(
        height=380,
        template='plotly_dark',
        paper_bgcolor='rgba(10, 14, 39, 0.8)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='#ffffff', family='Open Sans', size=11),
        xaxis_title='Précipitations (mm)',
        yaxis_title='Nombre de Jours'
    )
    
    st.plotly_chart(fig_precip_hist, use_container_width=True)

# ==================== TAB 4: ATMOSPHERE ====================

elif menu_selection == "🌬️ ATMOSPHÈRE":
    st.markdown("### Conditions Atmosphériques")
    
    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    col_a1.metric("Visibilité Moy", f"{filtered_df['VISIBILITY_AVG_KM'].mean():.1f} km")
    col_a2.metric("Nuages Moy", f"{filtered_df['CLOUDCOVER_AVG_PERCENT'].mean():.0f}%")
    col_a3.metric("Pression Max", f"{filtered_df['PRESSURE_MAX_MB'].max():.1f} mb")
    col_a4.metric("Vent Max", f"{filtered_df['WINDSPEED_MAX_KMH'].max():.1f} km/h")
    
    st.markdown("---")
    
    st.markdown("---")
    
    st.markdown("#### Visibilité")
    
    vis_chart = alt.Chart(filtered_df).mark_area(
        color='#00f0ff',
        opacity=0.6,
        line=True
    ).encode(
        x=alt.X('DATE:T', title='Date'),
        y=alt.Y('VISIBILITY_AVG_KM:Q', title='Visibilité (km)'),
        tooltip=['DATE:T', 'VISIBILITY_AVG_KM:Q']
    ).properties(height=380).interactive()
    
    st.altair_chart(vis_chart, use_container_width=True)

    st.markdown("#### Couverture Nuageuse")
    
    cloud_chart = alt.Chart(filtered_df).mark_line(
        color='#00ff88',
        size=2,
        point=True
    ).encode(
        x=alt.X('DATE:T', title='Date'),
        y=alt.Y('CLOUDCOVER_AVG_PERCENT:Q', title='Couverture (%)'),
        tooltip=['DATE:T', 'CLOUDCOVER_AVG_PERCENT:Q']
    ).properties(height=380).interactive()
    
    st.altair_chart(cloud_chart, use_container_width=True)

# ==================== TAB 5: SOLAR ====================

elif menu_selection == "☀️ SOLAIRE":
    st.markdown("### Analyse Solaire")
    
    col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
    col_s1.metric("Ensoleil Moy", f"{filtered_df['SUNHOUR'].mean():.1f} h")
    col_s2.metric("UV Max", f"{filtered_df['UV_INDEX'].max():.1f}")
    col_s3.metric("UV Moy", f"{filtered_df['UV_INDEX'].mean():.1f}")
    col_s4.metric("Jours >8h", len(filtered_df[filtered_df['SUNHOUR'] > 8]))
    col_s5.metric("Jours <3 UV", len(filtered_df[filtered_df['UV_INDEX'] < 3]))
    
    st.markdown("---")
    
    col_sol1, col_sol2 = st.columns(2)
    
    with col_sol1:
        st.markdown("#### Heures d'Ensoleillement")
        
        sun_chart = alt.Chart(filtered_df).mark_bar(color='#ffd700', opacity=0.8).encode(
            x=alt.X('DATE:T', title='Date'),
            y=alt.Y('SUNHOUR:Q', title='Heures'),
            tooltip=['DATE:T', 'SUNHOUR:Q']
        ).properties(height=380).interactive()
        
        st.altair_chart(sun_chart, use_container_width=True)
    
    with col_sol2:
        st.markdown("#### Distribution UV")
        
        fig_uv = go.Figure()
        
        fig_uv.add_trace(go.Histogram(
            x=filtered_df['UV_INDEX'],
            name='Indice UV',
            marker_color='#ff6b6b',
            nbinsx=30,
            hovertemplate='UV: %{x:.1f}<br>Jours: %{y}<extra></extra>'
        ))
        
        fig_uv.update_layout(
            height=380,
            template='plotly_dark',
            paper_bgcolor='rgba(10, 14, 39, 0.8)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#ffffff', family='Open Sans', size=11),
            xaxis_title='Indice UV',
            yaxis_title='Nombre de Jours'
        )
        
        st.plotly_chart(fig_uv, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("#### Données Solaires (20 Derniers Jours)")
    
    solar_df = filtered_df[['DATE', 'SUNRISE', 'SUNSET', 'SUNHOUR', 'UV_INDEX']].tail(20).copy()
    solar_df = solar_df.sort_values('DATE', ascending=False)
    solar_df['DATE'] = solar_df['DATE'].dt.strftime('%d/%m/%Y')
    solar_df.columns = ['Date', 'Lever', 'Coucher', 'Heures', 'UV']
    
    st.dataframe(solar_df, use_container_width=True, hide_index=True)

# ==================== TAB 6: TRENDS ====================

elif menu_selection == "📈 TENDANCES":
    st.markdown("### Tendances Long-Terme")
    
    st.markdown("#### Tendance Temp (Annuelle)")
    
    def get_yearly_trend(df_target, city_name):
        y_df = df_target.copy()
        y_df['Year'] = y_df['DATE'].dt.year
        return y_df.groupby('Year')['MAX_TEMPERATURE_C'].mean()

    yearly_1 = get_yearly_trend(filtered_df, selected_city_name)
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=yearly_1.index.astype(str), y=yearly_1.values,
        name=f"Max {selected_city_name}", mode='lines+markers',
        line=dict(color='#00f0ff', width=2),
        marker=dict(size=8)
    ))
    
    if comparison_mode and filtered_df_2 is not None:
        yearly_2 = get_yearly_trend(filtered_df_2, selected_city_2_name)
        fig_trend.add_trace(go.Scatter(
            x=yearly_2.index.astype(str), y=yearly_2.values,
            name=f"Max {selected_city_2_name}", mode='lines+markers',
            line=dict(color='#ff6b6b', width=2),
            marker=dict(size=8)
        ))
        
    fig_trend.update_layout(
        height=380, template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Open Sans', size=11),
        yaxis_title='Température Moyenne (°C)',
        xaxis_title='Année',
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(color="white", size=10), bgcolor="rgba(0,0,0,0)"
        )
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")
    
    st.markdown("#### Accum. Pluie (Mensuelle)")
    
    def get_monthly_precip(df_target):
        m_df = df_target.copy()
        m_df['Month'] = m_df['DATE'].dt.to_period('M')
        return m_df.groupby('Month')['PRECIP_TOTAL_DAY_MM'].sum()

    monthly_1 = get_monthly_precip(filtered_df)
    
    fig_precip_trend = go.Figure()
    fig_precip_trend.add_trace(go.Bar(
        x=monthly_1.index.astype(str), y=monthly_1.values,
        name=selected_city_name, marker_color='#00f0ff'
    ))
    
    if comparison_mode and filtered_df_2 is not None:
        monthly_2 = get_monthly_precip(filtered_df_2)
        fig_precip_trend.add_trace(go.Bar(
            x=monthly_2.index.astype(str), y=monthly_2.values,
            name=selected_city_2_name, marker_color='#ff6b6b'
        ))
        
    fig_precip_trend.update_layout(
        height=380, barmode='group', template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Open Sans', size=11),
        yaxis_title='Précipitations (mm)',
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(color="white", size=10), bgcolor="rgba(0,0,0,0)"
        )
    )
    st.plotly_chart(fig_precip_trend, use_container_width=True)

# ==================== TAB 7: CORRELATIONS ====================

elif menu_selection == "🔗 CORRÉLATIONS":
    st.markdown("### Matrice de Corrélation")
    
    correlation_vars = [
        'MAX_TEMPERATURE_C', 'MIN_TEMPERATURE_C', 'PRECIP_TOTAL_DAY_MM',
        'HUMIDITY_MAX_PERCENT', 'WINDSPEED_MAX_KMH', 'VISIBILITY_AVG_KM',
        'PRESSURE_MAX_MB', 'CLOUDCOVER_AVG_PERCENT', 'UV_INDEX', 'SUNHOUR'
    ]
    
    corr_matrix = filtered_df[correlation_vars].corr()
    
    fig_corr = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=correlation_vars,
        y=correlation_vars,
        colorscale='RdBu',
        zmid=0,
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 9},
        hovertemplate='%{x} vs %{y}<br>Corr: <b>%{z:.2f}</b><extra></extra>',
        colorbar=dict(title='Corrélation')
    ))
    
    fig_corr.update_layout(
        height=650,
        template='plotly_dark',
        paper_bgcolor='rgba(10, 14, 39, 0.8)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='#ffffff', family='Open Sans', size=10),
        xaxis={'side': 'bottom'}
    )
    
    st.plotly_chart(fig_corr, use_container_width=True)

# ==================== TAB 8: STATISTICS ====================

elif menu_selection == "📉 STATISTIQUES":
    st.markdown("### Analyse Statistique")
    
    col_st1, col_st2 = st.columns(2)
    
    with col_st1:
        st.markdown("#### Distribution Température")
        
        fig_temp_dist = go.Figure()
        
        fig_temp_dist.add_trace(go.Histogram(
            x=filtered_df['MAX_TEMPERATURE_C'],
            name='Max',
            marker_color='#ff6b6b',
            opacity=0.8,
            nbinsx=40
        ))
        
        fig_temp_dist.add_trace(go.Histogram(
            x=filtered_df['MIN_TEMPERATURE_C'],
            name='Min',
            marker_color='#4ecdc4',
            opacity=0.8,
            nbinsx=40
        ))
        
        fig_temp_dist.update_layout(
            height=380,
            template='plotly_dark',
            barmode='overlay',
            paper_bgcolor='rgba(10, 14, 39, 0.8)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#ffffff', family='Open Sans', size=11),
            xaxis_title='Température (°C)',
            yaxis_title='Jours'
        )
        
        st.plotly_chart(fig_temp_dist, use_container_width=True)
    
    with col_st2:
        st.markdown("#### Distribution Humidité")
        
        fig_humid = go.Figure()
        
        fig_humid.add_trace(go.Histogram(
            x=filtered_df['HUMIDITY_MAX_PERCENT'],
            name='Humidité',
            marker_color='#00f0ff',
            nbinsx=40
        ))
        
        fig_humid.update_layout(
            height=380,
            template='plotly_dark',
            paper_bgcolor='rgba(10, 14, 39, 0.8)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#ffffff', family='Open Sans', size=11),
            xaxis_title='Humidité (%)',
            yaxis_title='Jours'
        )
        
        st.plotly_chart(fig_humid, use_container_width=True)

# ==================== TAB 9: ANOMALIES ====================

elif menu_selection == "🎯 ANOMALIES":
    st.markdown("### Détection Anomalies")
    
    def detect_anomalies(series, threshold=2.5):
        z_scores = np.abs(stats.zscore(series.dropna()))
        return z_scores > threshold
    
    temp_anomalies = detect_anomalies(filtered_df['MAX_TEMPERATURE_C'])
    
    col_an1, col_an2, col_an3 = st.columns(3)
    col_an1.metric("Anomalies Temp", temp_anomalies.sum())
    col_an2.metric("Anomalies Pluie", detect_anomalies(filtered_df['PRECIP_TOTAL_DAY_MM']).sum())
    col_an3.metric("Anomalies Vent", detect_anomalies(filtered_df['WINDSPEED_MAX_KMH']).sum())
    
    st.markdown("---")
    
    st.markdown("#### Anomalies Température")
    
    anomaly_df = filtered_df.copy()
    anomaly_df['Temp_Anomaly'] = temp_anomalies.values
    anomaly_temp = anomaly_df[anomaly_df['Temp_Anomaly']].sort_values('DATE', ascending=False).head(20)
    
    if len(anomaly_temp) > 0:
        fig_anom_temp = go.Figure()
        
        normal = filtered_df[~temp_anomalies.values]
        fig_anom_temp.add_trace(go.Scatter(
            x=normal['DATE'],
            y=normal['MAX_TEMPERATURE_C'],
            name='Normal',
            mode='markers',
            marker=dict(color='rgba(0, 240, 255, 0.3)', size=4)
        ))
        
        fig_anom_temp.add_trace(go.Scatter(
            x=anomaly_temp['DATE'],
            y=anomaly_temp['MAX_TEMPERATURE_C'],
            name='Anomalie',
            mode='markers',
            marker=dict(color='#ff6b6b', size=10, symbol='diamond')
        ))
        
        fig_anom_temp.update_layout(
            height=380,
            template='plotly_dark',
            paper_bgcolor='rgba(10, 14, 39, 0.8)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#ffffff', family='Open Sans', size=11),
            yaxis_title='Température (°C)'
        )
        
        st.plotly_chart(fig_anom_temp, use_container_width=True)

# ==================== TAB 10: FORECASTS ====================

elif menu_selection == "🔮 PRÉVISIONS":
    st.markdown("### Prédictions 6 Mois")
    
    from numpy.polynomial.polynomial import Polynomial
    
    forecast_df = filtered_df.copy()
    forecast_df['Days'] = (forecast_df['DATE'] - forecast_df['DATE'].min()).dt.days
    
    X = forecast_df['Days'].values
    y_temp = forecast_df['MAX_TEMPERATURE_C'].values
    
    coeffs = np.polyfit(X, y_temp, 3)
    poly = np.poly1d(coeffs)
    
    future_days = np.arange(0, len(X) + 180)
    forecast_temps = poly(future_days)
    forecast_dates = forecast_df['DATE'].min() + pd.to_timedelta(future_days, unit='D')
    
    col_fc1, col_fc2 = st.columns([2, 1])
    
    with col_fc1:
        st.markdown("#### Tendance Prédite")
        
        fig_forecast = go.Figure()
        
        fig_forecast.add_trace(go.Scatter(
            x=forecast_df['DATE'],
            y=y_temp,
            name='Historique',
            mode='lines',
            line=dict(color='#00f0ff', width=2)
        ))
        
        forecast_mask = forecast_dates >= forecast_df['DATE'].max()
        fig_forecast.add_trace(go.Scatter(
            x=forecast_dates[forecast_mask],
            y=forecast_temps[forecast_mask],
            name='Prédiction',
            mode='lines',
            line=dict(color='#ff6b6b', width=2, dash='dash')
        ))
        
        fig_forecast.update_layout(
            height=380,
            template='plotly_dark',
            paper_bgcolor='rgba(10, 14, 39, 0.8)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#ffffff', family='Open Sans', size=11),
            yaxis_title='Température (°C)'
        )
        
        st.plotly_chart(fig_forecast, use_container_width=True)
    
    with col_fc2:
        st.markdown("#### Aperçus")
        
        current_avg = y_temp[-30:].mean()
        forecast_avg = forecast_temps[len(X):len(X)+90].mean()
        
        st.markdown(f"""
        <div class="highlight-box">
        <h4>📊 Résumé</h4>
        <p><strong>Actuelle (30j):</strong> <span style="color: #00f0ff; font-size: 1.3rem;">{current_avg:.1f}°C</span></p>
        <p><strong>Prédite (90j):</strong> <span style="color: #ff6b6b; font-size: 1.3rem;">{forecast_avg:.1f}°C</span></p>
        <p><strong>Changement:</strong> <span style="color: #00ff88; font-size: 1.3rem;">{forecast_avg-current_avg:+.1f}°C</span></p>
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 11: DATA ====================

elif menu_selection == "📋 EXPLORATION":
    st.markdown("### Exploration des Données")
    
    col_exp1, col_exp2, col_exp3 = st.columns(3)
    
    with col_exp1:
        sort_by = st.selectbox(
            "Trier par",
            options=['DATE', 'MAX_TEMPERATURE_C', 'PRECIP_TOTAL_DAY_MM', 'WINDSPEED_MAX_KMH']
        )
    
    with col_exp2:
        sort_order = st.radio("Ordre", options=['Croissant', 'Décroissant'], horizontal=True)
    
    with col_exp3:
        rows_display = st.slider("Lignes", 10, 500, 100)
    
    ascending = sort_order == 'Croissant'
    display_df = filtered_df.sort_values(by=sort_by, ascending=ascending).head(rows_display)
    
    st.markdown("---")
    st.dataframe(display_df, use_container_width=True, height=600)
    
    st.markdown("---")
    
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Télécharger CSV",
        data=csv,
        file_name=f"{selected_city_name}_weather_{datetime.now().strftime('%Y%m%d')}.csv"
    )

# ==================== TAB 12: INSIGHTS ====================

elif menu_selection == "⚡ ANALYSES IA":
    st.markdown("### Analyses IA")
    
    col_ins1, col_ins2 = st.columns(2) if comparison_mode else (st.container(), None)
    
    with col_ins1:
        st.markdown(f"#### Profil: {selected_city_name}")
        st.markdown(f"""
        <div class="highlight-box">
        <ul style="font-size: 1rem;">
        <li><strong>Temp Moyenne:</strong> {insights['avg_temp']:.1f}°C</li>
        <li><strong>Volatilité:</strong> {insights['temp_volatility']:.1f}°C</li>
        <li><strong>Humidité:</strong> {insights['humidity_avg']:.0f}%</li>
        <li><strong>Jours Pluie:</strong> {insights['rainy_days_pct']:.1f}%</li>
        <li><strong>Vent Moyen:</strong> {insights['avg_wind']:.1f} km/h</li>
        <li><strong>Jours Ensoleillés:</strong> {insights['sunny_days']}</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
    if comparison_mode and insights_2:
        with col_ins2:
            st.markdown(f"#### Profil: {selected_city_2_name}")
            st.markdown(f"""
            <div class="highlight-box" style="border-color: #ff6b6b; background: linear-gradient(135deg, rgba(255, 107, 107, 0.1) 0%, rgba(255, 0, 0, 0.1) 100%);">
            <ul style="font-size: 1rem;">
            <li><strong>Temp Moyenne:</strong> {insights_2['avg_temp']:.1f}°C</li>
            <li><strong>Volatilité:</strong> {insights_2['temp_volatility']:.1f}°C</li>
            <li><strong>Humidité:</strong> {insights_2['humidity_avg']:.0f}%</li>
            <li><strong>Jours Pluie:</strong> {insights_2['rainy_days_pct']:.1f}%</li>
            <li><strong>Vent Moyen:</strong> {insights_2['avg_wind']:.1f} km/h</li>
            <li><strong>Jours Ensoleillés:</strong> {insights_2['sunny_days']}</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Patterns Mensuels (Ville Principale)")
    
    monthly_data = filtered_df.copy()
    monthly_data['Month'] = monthly_data['DATE'].dt.month
    monthly_summary = monthly_data.groupby('Month').agg({
        'MAX_TEMPERATURE_C': 'mean',
        'PRECIP_TOTAL_DAY_MM': 'sum',
        'SUNHOUR': 'mean'
    }).round(2)
    
    month_names = ['Jan', 'Fev', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aou', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_summary.index = [month_names[i-1] if i <= 12 else '' for i in monthly_summary.index]
    monthly_summary.columns = ['Temp (°C)', 'Pluie (mm)', 'Soleil (h)']
    st.dataframe(monthly_summary, use_container_width=True)

# ==================== FOOTER ====================

st.markdown("---")
st.markdown("""
    <p style="text-align: center; color: #b0c4de; font-size: 0.95rem; margin-top: 2rem;">
    🌍 Analyse Météo Maroc<br>
    <span style="font-size: 0.85rem;">Abdellah Maghous @2006</span>
    </p>
    """, unsafe_allow_html=True)