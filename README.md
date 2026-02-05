# 🌍 Morocco Weather Analytics Pro
![App Preview](assets/app_preview.png)

Une application d'analyse météorologique professionnelle pour le Maroc, développée avec Streamlit.

## 🚀 Fonctionnalités

- **12 Modules d'Analyse** : Dashboard, Température, Précipitations, Atmosphère, Solaire, Tendances, Corrélations, Statistiques, Anomalies, Prédictions, Données, et Insights
- **44 Villes Marocaines** : Données météorologiques complètes
- **Mode Comparaison** : Comparez deux villes simultanément
- **Visualisations Interactives** : Graphiques Plotly, Altair, et cartes Pydeck
- **Design Premium** : Interface moderne avec thème sombre personnalisé

## 📊 Données

L'application analyse 34 variables météorologiques incluant :
- Températures (min, max, horaires)
- Précipitations et neige
- Humidité et point de rosée
- Vent et pression atmosphérique
- Ensoleillement et UV
- Visibilité et couverture nuageuse

## 🛠️ Installation Locale

```bash
# Cloner le dépôt
git clone <votre-repo>
cd 46100099-fra

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```


## 📁 Structure du Projet

```
46100099-fra/
├── app.py                      # Application principale
├── requirements.txt            # Dépendances Python
├── .streamlit/
│   └── config.toml            # Configuration Streamlit
├── export-*.csv               # Fichiers de données (44 villes)
└── README.md                  # Ce fichier
```

## 🎨 Villes Disponibles

Agadir, Al Hoceima, Assilah, Azilal, Azrou, Beni Mellal, Berkane, Boujdour, Casablanca, Chefchaouen, Chichaoua, Dakhla, Demnate, El Jadida, Essaouira, Fes, Guelmim, Kasba Tadla, Kel At Mgouna, Kenitra, Khemisset, Khouribga, Ksar El Kebir, La Youne, Larache, Marrakech, Meknes, Mohammedia, Oued Zem, Ouezzane, Rabat, Safi, Saidia, Sefrou, Settat, Sidi Bennour, Sidi Ifni, Sidi Slimane, Tanger, Taounate, Tarfaya, Taroudant, Tetouan, Tinghir

## 🔧 Technologies

- **Streamlit** : Framework d'application
- **Pandas** : Manipulation de données
- **Plotly** : Graphiques interactifs
- **Altair** : Visualisations déclaratives
- **Pydeck** : Cartes 3D
- **NumPy & SciPy** : Calculs scientifiques

## 📝 Notes

- Les données sont mises en cache pour optimiser les performances
- L'application détecte automatiquement les fichiers CSV dans le répertoire
- Compatible avec Streamlit Cloud sans modifications supplémentaires

## 🌟Link

https://analyse-meteo-maroc.streamlit.app

---

Développé avec ❤️ pour l'analyse météorologique du Maroc
