<div align="center">
  <img src="assets/app_preview.png" alt="Morocco Weather Analytics Pro" width="800">

  <h1>🌍 Morocco Weather Analytics Pro</h1>
  <p><b>Professional Meteorological Intelligence Platform | 44 Moroccan Cities</b></p>

  [![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
  [![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
  [![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-analyse--meteo--maroc.streamlit.app-success?style=for-the-badge)](https://analyse-meteo-maroc.streamlit.app)

  > **A high-performance weather analytics dashboard** covering 44 Moroccan cities  
  > with 12 analysis modules, 34 meteorological variables, and interactive visualizations.

  [🚀 Live Demo](#-live-demo) • [✨ Features](#-key-features) • [📊 Data](#-data--variables) • [🛠️ Installation](#️-installation--local-setup) • [🌆 Cities](#-available-cities)

</div>

---

## 🚀 Live Demo

Experience the full platform live on Streamlit Cloud:

🔗 **[analyse-meteo-maroc.streamlit.app](https://analyse-meteo-maroc.streamlit.app)**

> No installation required — explore Moroccan weather data directly in your browser.

---

## ✨ Key Features

### 📦 12 Analysis Modules

| Module | Description |
|---|---|
| 📊 **Dashboard** | General overview with key meteorological indicators |
| 🌡️ **Temperature** | Min/max trends, hourly patterns, and heat analysis |
| 🌧️ **Precipitation** | Rainfall distribution, snowfall, and seasonal patterns |
| 💨 **Atmosphere** | Wind speed, pressure, and atmospheric dynamics |
| ☀️ **Solar** | Sunshine duration, UV index, and irradiance data |
| 📈 **Trends** | Long-term meteorological trend detection |
| 🔗 **Correlations** | Cross-variable statistical relationship mapping |
| 📉 **Statistics** | Descriptive stats, distributions, and percentiles |
| ⚠️ **Anomalies** | Detection of extreme and unusual weather events |
| 🔮 **Predictions** | Forecasting models based on historical patterns |
| 🗄️ **Data** | Raw data explorer and export functionality |
| 💡 **Insights** | AI-generated meteorological summaries |

### 🆚 City Comparison Mode
Compare **two cities simultaneously** across all meteorological variables — perfect for regional climate studies.

### 🗺️ Interactive Visualizations
- **Plotly** — Dynamic charts and time series
- **Altair** — Declarative statistical visualizations
- **Pydeck** — 3D geospatial maps of Morocco

### 🎨 Premium UI
Modern dark-themed interface inspired by professional meteorological dashboards.

---

## 📊 Data & Variables

The platform analyzes **34 meteorological variables** across all 44 cities:

| Category | Variables |
|---|---|
| 🌡️ **Temperature** | Min, Max, Mean, Hourly profiles, Dew point |
| 🌧️ **Precipitation** | Rainfall, Snowfall, Precipitation probability |
| 💧 **Humidity** | Relative humidity, Dew point temperature |
| 💨 **Wind** | Speed, Direction, Gusts |
| 🔵 **Pressure** | Atmospheric pressure, Sea-level pressure |
| ☀️ **Solar** | Sunshine duration, UV index, Solar irradiance |
| 👁️ **Visibility** | Visibility range, Cloud cover percentage |

> 📌 Data is auto-detected from CSV files in the project directory and cached for optimal performance.

---

## 🛠️ Installation & Local Setup

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Step-by-step

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd 46100099-fra
```

**2. Create a virtual environment** *(recommended)*
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Launch the application**
```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501` 🎉

---

## 📁 Project Structure
```
46100099-fra/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── assets/
│   └── app_preview.png       # App screenshot
├── .streamlit/
│   └── config.toml           # Streamlit theme & configuration
├── export-*.csv              # Weather data files (44 cities)
└── README.md                 # Project documentation
```

---

## 🌆 Available Cities

The platform covers **44 Moroccan cities** spanning all regions:

<details>
<summary>📍 Click to expand the full city list</summary>

| | | | |
|---|---|---|---|
| Agadir | Al Hoceima | Assilah | Azilal |
| Azrou | Beni Mellal | Berkane | Boujdour |
| Casablanca | Chefchaouen | Chichaoua | Dakhla |
| Demnate | El Jadida | Essaouira | Fes |
| Guelmim | Kasba Tadla | Kel At Mgouna | Kenitra |
| Khemisset | Khouribga | Ksar El Kebir | Laayoune |
| Larache | Marrakech | Meknes | Mohammedia |
| Oued Zem | Ouezzane | Rabat | Safi |
| Saidia | Sefrou | Settat | Sidi Bennour |
| Sidi Ifni | Sidi Slimane | Tanger | Taounate |
| Tarfaya | Taroudant | Tetouan | Tinghir |

</details>

---

## 🔧 Technology Stack

| Category | Technology | Purpose |
|---|---|---|
| **Framework** | [Streamlit](https://streamlit.io/) | Web application engine |
| **Data** | [Pandas](https://pandas.pydata.org/) | Data manipulation & analysis |
| **Charts** | [Plotly](https://plotly.com/) | Interactive visualizations |
| **Stats Viz** | [Altair](https://altair-viz.github.io/) | Declarative statistical charts |
| **Maps** | [Pydeck](https://deckgl.readthedocs.io/) | 3D geospatial mapping |
| **Science** | [NumPy](https://numpy.org/) & [SciPy](https://scipy.org/) | Statistical computations |

---

## ☁️ Deployment Notes

- ✅ Fully compatible with **Streamlit Community Cloud** — no extra configuration needed
- ✅ CSV files are **auto-detected** from the project directory
- ✅ Smart **caching layer** ensures fast load times and low memory footprint
- ✅ Runs seamlessly **under 1GB RAM** for cloud deployment

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your branch: `git checkout -b feature/NewCity`
3. Commit your changes: `git commit -m 'Add weather data for NewCity'`
4. Push and open a Pull Request

---

<div align="center">

**Built with ❤️ for Moroccan weather analysis and climate research**

⭐ If you find this project useful, please consider giving it a star!

🔗 **[analyse-meteo-maroc.streamlit.app](https://analyse-meteo-maroc.streamlit.app)**

</div>
