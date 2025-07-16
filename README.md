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
├── documentation/           # Documentation du projet
│   ├── data/                # Documentation liée aux données
│   │   ├── qualite_donnees.md    # Qualité des données
│   │   └── fiabilite_donnees.md  # Fiabilité des données
│   ├── testing/             # Documentation liée aux tests
│   │   ├── estimation_charge.md       # Estimation de charge
│   │   ├── resultats_locust.md        # Résultats des tests
│   │   ├── benchmark_outils.md        # Benchmark d'outils
│   │   └── documentation_complete_charge.md  # Documentation complète
│   └── optimization/        # Documentation liée à l'optimisation
│       └── plan_actions_correctives.md # Plan d'actions correctives
├── charge_estimation/       # Version originale des estimations de charge
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

Les analyses et recommandations sont disponibles dans plusieurs documents structurés :

- **Hypothèses et estimations** : [`documentation/testing/estimation_charge.md`](documentation/testing/estimation_charge.md)
- **Résultats des tests** : [`documentation/testing/resultats_locust.md`](documentation/testing/resultats_locust.md)
- **Plan d'actions correctives** : [`documentation/optimization/plan_actions_correctives.md`](documentation/optimization/plan_actions_correctives.md)
- **Benchmark d'outils** : [`documentation/testing/benchmark_outils.md`](documentation/testing/benchmark_outils.md)
- **Documentation complète** : [`documentation/testing/documentation_complete_charge.md`](documentation/testing/documentation_complete_charge.md)

La documentation sur la qualité et fiabilité des données est disponible dans :
- [`documentation/data/qualite_donnees.md`](documentation/data/qualite_donnees.md)
- [`documentation/data/fiabilite_donnees.md`](documentation/data/fiabilite_donnees.md)

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

## 8. Auteurs

Ce projet a été réalisé par :

- MALONJU Bibiche
- ANDRIAMANANJARA MANDIMBY Harena
- BAH Elhadj Ibrahima
- TABAR LABONNE Baptiste

## 9. Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.