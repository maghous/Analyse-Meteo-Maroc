# 🌍 Morocco Weather Analytics Pro

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

## ☁️ Déploiement sur Streamlit Cloud

### Étape 1 : Préparer votre dépôt GitHub

1. Créez un nouveau dépôt sur GitHub
2. Poussez tous les fichiers :

```bash
git init
git add .
git commit -m "Initial commit - Morocco Weather Analytics"
git branch -M main
git remote add origin <votre-url-github>
git push -u origin main
```

### Étape 2 : Déployer sur Streamlit Cloud

1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. Connectez-vous avec votre compte GitHub
3. Cliquez sur "New app"
4. Sélectionnez :
   - **Repository** : Votre dépôt
   - **Branch** : main
   - **Main file path** : app.py
5. Cliquez sur "Deploy!"

### Étape 3 : Configuration (optionnel)

L'application utilise le fichier `.streamlit/config.toml` pour la configuration du thème.

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

## 🌟 Version

**v4.0 Final** - Analyse Météorologique Professionnelle

---

Développé avec ❤️ pour l'analyse météorologique du Maroc
