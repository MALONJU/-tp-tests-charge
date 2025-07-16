# Tests de Charge - API BuyYourKawa

Ce projet contient l'ensemble des tests de charge réalisés sur l'API BuyYourKawa, ainsi que les analyses, résultats et recommandations qui en découlent.

## 1. Contexte

L'API BuyYourKawa est un service de gestion de clients pour une entreprise de vente de café. Elle permet la création, la consultation et la mise à jour des données clients. Ces tests de charge ont été réalisés pour valider la robustesse de l'API face à un trafic important, notamment dans le cadre d'une campagne marketing à venir.

## 2. Installation et configuration

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/votre-utilisateur/tp-tests-charge.git
cd tp-tests-charge

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows
venv\Scripts\activate
# Sur Linux/Mac
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

## 3. Structure du projet

```
/
├── charge_estimation/       # Estimations et analyses de charge
├── documentation/           # Documentation additionnelle
├── images/                  # Captures d'écran et graphiques
├── locust_tests/            # Tests de charge spécifiques
├── rapports/                # Rapports d'analyse au format CSV/JSON
├── security/                # Documentation de sécurité
├── tests/                   # Tests unitaires et d'intégration
├── locustfile.py           # Configuration principale Locust
├── main.py                 # Application principale
├── models.py               # Modèles de données
└── requirements.txt        # Dépendances Python
```

## 4. Exécution des tests

### Démarrer l'API

```bash
# Dans un terminal, démarrer l'API
python main.py
```

### Exécuter les tests de charge

```bash
# Dans un nouveau terminal, démarrer Locust
locust -f locustfile.py --host=http://localhost:8000
```

Puis, accéder à l'interface web de Locust à l'adresse: http://localhost:8089

### Configuration des tests

Pour reproduire les tests documentés:

1. Nombre d'utilisateurs: 300
2. Taux de spawn: 10 utilisateurs/seconde
3. Profil de charge: ramp-up (10min), plateau (30min), ramp-down (5min)

## 5. Résultats des tests

Les résultats détaillés sont disponibles dans les formats suivants:

- **HTML**: `rapports/locust_report.html`
- **CSV**: `rapports/requests_stats.csv` et `rapports/response_time_stats.csv`
- **JSON**: `rapports/simulation_params.json`

Les principaux résultats montrent:

- Temps de réponse moyen: 520ms
- Taux d'erreur global: 2%
- Capacité maximale: 300 utilisateurs simultanés
- RPS (Requêtes par seconde) maximum: 38.2

## 6. Analyses et recommandations

L'analyse complète est disponible dans le document `charge_estimation/charge_estimation.md`, qui inclut:

- Hypothèses de trafic
- Profils utilisateurs
- Modèle de charge
- Plan d'actions correctives
- Benchmark d'outils
- Recommandations d'infrastructure

Principales recommandations:

1. Optimiser l'authentification (endpoint `/token`)
2. Implémenter un cache Redis pour les données fréquemment consultées
3. Optimiser les requêtes SQL avec des index appropriés
4. Augmenter les ressources serveur (3x EC2 t3.large recommandés)

## 7. Code source sur GitHub

### Organisation du dépôt

Le dépôt est organisé selon les meilleures pratiques:

- **Branches**: 
  - `main`: code stable et fonctionnel
  - `develop`: développement en cours
  - `feature/*`: nouvelles fonctionnalités

- **Documentation**: 
  - Chaque dossier contient un README.md explicatif
  - Les tests sont documentés avec des docstrings

- **Workflow Git**: 
  - Commits atomiques avec messages clairs
  - Pull requests pour toute modification significative
  - Code review obligatoire

### Contribution

Pour contribuer au projet:

1. Forker le dépôt
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Commiter vos changements (`git commit -m 'Add some amazing feature'`)
4. Pousser la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 8. Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.