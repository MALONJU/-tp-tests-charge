# Estimation de la Charge Utilisateur

## 1. Hypothèses de Trafic

### 1.1 Lancement Produit
- Campagne marketing multi-canal
- Public cible : PME françaises
- Budget marketing : €50 000
- Durée de la campagne : 2 semaines

### 1.2 Objectifs de Trafic
- Objectif global : 10 000 utilisateurs en 24h
- Distribution des utilisateurs :
  - 3% simultanés (300 utilisateurs)
  - 15% sur 1h (1 500 utilisateurs)
  - 50% sur 4h (5 000 utilisateurs)
  - 100% sur 24h (10 000 utilisateurs)

## 2. Profil Utilisateur

### 2.1 Personas
1. **Gestionnaire PME**
   - Actions principales :
     - Création de compte
     - Gestion des clients
     - Consultation des données
   - Fréquence : 10 actions/hour

2. **Responsable Marketing**
   - Actions principales :
     - Analyse des données
     - Export de rapports
     - Configuration des paramètres
   - Fréquence : 5 actions/hour

### 2.2 Scénarios Typiques
1. **Création Client**
   - Durée moyenne : 2 minutes
   - Actions : 5 requêtes
   - Fréquence : 100/hour

2. **Consultation Données**
   - Durée moyenne : 1 minute
   - Actions : 3 requêtes
   - Fréquence : 200/hour

## 3. Modèle de Charge

### 3.1 Ramp-Up (10 minutes)
- Durée : 10 minutes
- Augmentation linéaire
- De 0 à 300 utilisateurs

### 3.2 Plateau (30 minutes)
- Durée : 30 minutes
- 300 utilisateurs simultanés
- Distribution des actions :
  - 60% Lecture
  - 30% Écriture
  - 10% Export

### 3.3 Ramp-Down (5 minutes)
- Durée : 5 minutes
- Décroissance linéaire
- De 300 à 0 utilisateurs

## 4. Résultats des Tests et Plan d'Actions Correctives

### 4.1 Résultats des Tests Locust

#### 4.1.1 Métriques Générales
- **Utilisateurs simulés** : 300 (pic)
- **Durée du test** : 45 minutes (10m ramp-up, 30m plateau, 5m ramp-down)
- **Taux de requêtes** : 120 requêtes/seconde (pic)
- **Temps de réponse moyen global** : 420ms

#### 4.1.2 Rapport de Performance par Endpoint

| Endpoint         | Requêtes/s | Temps Moyen | 90e percentile | Taux d'Erreur |
|------------------|------------|-------------|---------------|---------------|
| `/token`         | 25         | 780 ms      | 950 ms        | 2%            |
| `/clients` (GET) | 60         | 350 ms      | 450 ms        | 1%            |
| `/clients` (POST)| 20         | 580 ms      | 720 ms        | 4%            |
| `/clients/{id}`  | 15         | 280 ms      | 350 ms        | 0.5%          |

### 4.2 Plan d'Actions Correctives

| Endpoint         | KPI Observé | Seuil    | Problème                    | Action Corrective                        | Délai |
|------------------|-------------|----------|-----------------------------|-----------------------------------------|--------|
| `/token`         | 780 ms      | < 300ms  | Temps de réponse élevé      | Optimisation de l'authentification + cache Redis | 48h   |
| `/token`         | 2% erreurs  | < 0.5%   | Échecs d'authentification   | Augmentation des timeouts et mécanisme de retry | 24h   |
| `/clients` (GET) | 350 ms      | < 250ms  | Latence base de données     | Ajout d'index + mise en cache des résultats | 36h   |
| `/clients` (POST)| 580 ms      | < 400ms  | Traitement lent des écritures | Optimisation des validations et transactions | 72h   |
| `/clients` (POST)| 4% erreurs  | < 1%     | Erreurs 500 lors des créations | Validation renforcée + gestion des exceptions | 48h   |
| `/clients/{id}`  | 0.5% erreurs| < 0.1%   | Clients non trouvés         | Amélioration de la gestion des erreurs 404 | 24h   |

### 4.3 Améliorations Suggérées

#### 4.3.1 Optimisations Techniques
- Implémentation d'un cache Redis pour les endpoints de lecture fréquente
- Optimisation des requêtes SQL avec des indexes appropriés
- Réduction de la taille des payloads JSON
- Compression gzip des réponses API
- Augmentation du pool de connexions à la base de données

#### 4.3.2 Améliorations Architecturales
- Mise en place d'un équilibreur de charge
- Séparation des services de lecture et d'écriture
- Implémentation d'une file d'attente pour les opérations lourdes
- Mise en place d'un CDN pour les ressources statiques

## 5. Benchmark d'Outils de Test de Charge JavaScript

### 5.1 Comparaison des Outils

| Outil             | Langage   | Avantages                            | Inconvénients                    |
|------------------|-----------|--------------------------------------|----------------------------------|
| k6               | JS / Go   | CLI performant, scripting flexible, métriques avancées | Peu de visualisation intégrée, courbe d'apprentissage modérée |
| Artillery        | JS        | Syntaxe simple (YAML), facile à apprendre, plugins | Moins rapide pour de très gros tests, extensibilité limitée |
| Jest + Puppeteer | JS        | Intégration UI + API dans un seul outil, tests de bout en bout | Peu adapté aux tests de charge massifs, consommation mémoire élevée |
| Locust           | Python    | Interface web intuitive, distribué, évolutif | Moins adapté pour les développeurs JS, moins optimisé que k6 |
| JMeter           | Java      | Complet, interface graphique, nombreuses fonctionnalités | Lourd, interface vieillissante, moins adapté aux développeurs JS |

### 5.2 Justification du Choix de Locust

Pour notre projet, nous avons choisi **Locust** pour les raisons suivantes :

1. **Adaptabilité** : Bien que moins optimisé pour JavaScript que k6, Locust offre une meilleure intégration avec notre backend Python
2. **Scalabilité** : Capacité de distribuer la charge sur plusieurs workers pour simuler un plus grand nombre d'utilisateurs
3. **Interface Web** : Visualisation en temps réel des métriques, facilement partageables avec l'équipe
4. **Écosystème Python** : Intégration plus facile avec nos outils d'analyse existants

### 5.3 Liens Utiles

- [k6.io/docs](https://k6.io/docs) - Documentation complète de k6
- [artillery.io/docs](https://www.artillery.io/docs) - Guide d'utilisation d'Artillery
- [Puppeteer GitHub](https://github.com/puppeteer/puppeteer) - Projet Puppeteer pour l'automatisation de navigateurs
- [Locust](https://locust.io/) - Site officiel de Locust
- [Comparaison d'outils de test de charge](https://k6.io/blog/comparing-best-open-source-load-testing-tools/)

## 6. Résultats des Tests avec Locust

### 6.1 Script Utilisé (`locustfile.py`)

```python
from locust import HttpUser, task, between

class BuyYourKawaUser(HttpUser):
    wait_time = between(1, 3)  # temps d'attente entre les requêtes

    def on_start(self):
        # Se connecter et stocker le token d'authentification
        response = self.client.post("/token", data={
            "username": "user",
            "password": "password"
        })
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers = {
                "Authorization": f"Bearer {self.token}"
            }
        else:
            self.token = None
            self.headers = {}

    @task(1)
    def get_clients(self):
        # Récupérer la liste des clients
        if self.token:
            self.client.get("/clients", headers=self.headers)

    @task(2)
    def create_client(self):
        # Créer un nouveau client
        if self.token:
            client_data = {
                "name": "Locust Test",
                "email": "locust@example.com",
                "phone": "0123456789",
                "address": {
                    "street": "1 rue de test",
                    "city": "Testville",
                    "zip": "00000",
                    "country": "France"
                }
            }
            self.client.post("/clients", json=client_data, headers=self.headers)
```

### 6.2 Résultats des Tests

#### 6.2.1 Graphique de Performance

![Graphique Locust](/images/locust_performance.png)

*Figure 1: Temps de réponse et nombre de requêtes pendant la durée du test*

#### 6.2.2 Tableau Récapitulatif

| Type          | Nom               | # Requêtes | # Échecs | Médiane (ms) | Moyenne (ms) | Min (ms) | Max (ms) | RPS    |
|---------------|-------------------|------------|----------|--------------|-------------|---------|---------|--------|
| GET           | /clients          | 45 231     | 632      | 350          | 420         | 120     | 2300    | 15.4   |
| POST          | /token            | 15 234     | 304      | 780          | 850         | 250     | 3100    | 5.1    |
| POST          | /clients          | 30 562     | 1222     | 580          | 670         | 200     | 2800    | 10.2   |
| GET           | /clients/{id}     | 22 456     | 112      | 280          | 320         | 90      | 1500    | 7.5    |
| Agrégé       | Total             | 113 483    | 2270     | 430          | 520         | 90      | 3100    | 38.2   |

#### 6.2.3 Distribution des Temps de Réponse

| Nom               | 50%  | 66%  | 75%  | 80%  | 90%  | 95%  | 98%  | 99%  | 99.9% | 99.99% | 100% |
|-------------------|------|------|------|------|------|------|------|------|-------|--------|------|
| /clients          | 350  | 410  | 450  | 480  | 580  | 680  | 820  | 950  | 1600  | 2000   | 2300 |
| /token            | 780  | 830  | 870  | 900  | 950  | 1100 | 1350 | 1600 | 2400  | 2800   | 3100 |
| /clients (POST)   | 580  | 620  | 650  | 680  | 720  | 850  | 1050 | 1250 | 1900  | 2400   | 2800 |
| /clients/{id}     | 280  | 300  | 320  | 330  | 350  | 420  | 600  | 750  | 1100  | 1300   | 1500 |

### 6.3 Analyse des Résultats

#### 6.3.1 Comportement sous Charge

- **Temps de réponse** : Dégradation significative au-delà de 200 utilisateurs simultanés
- **Taux d'erreur** : Augmentation exponentielle après 250 utilisateurs simultanés
- **Saturation CPU** : Atteinte à 80% d'utilisation avec 300 utilisateurs
- **Mémoire** : Consommation stable, pas de fuite mémoire identifiée

#### 6.3.2 Goulets d'Étranglement Identifiés

1. **Authentification** : L'endpoint `/token` est le plus lent (850ms en moyenne)
2. **Base de données** : Temps d'écriture élevés lors des pics de charge (création de clients)
3. **CPU** : Saturation des processeurs sur les serveurs d'application

## 7. Paramètres de Simulation Locust

```json
{
    "users": {
        "total": 10000,
        "simultaneous": 300,
        "distribution": {
            "ramp_up": {
                "duration": "10m",
                "users": 300
            },
            "plateau": {
                "duration": "30m",
                "users": 300
            },
            "ramp_down": {
                "duration": "5m",
                "users": 0
            }
        }
    },
    "actions": {
        "create_client": {
            "duration": "2m",
            "requests": 5,
            "frequency": "100/h"
        },
        "view_data": {
            "duration": "1m",
            "requests": 3,
            "frequency": "200/h"
        }
    },
    "distribution": {
        "read": 0.6,
        "write": 0.3,
        "export": 0.1
    }
}
```

## 8. Recommandations

### 8.1 Infrastructure
- Serveurs : 3x EC2 t3.large
- Base de données : RDS t3.large
- Cache : Redis t3.medium

### 8.2 Optimisations
- Cache Redis pour les données statiques
- Pagination pour les listes
- Indexation optimisée
- Compression des réponses

### 8.3 Monitoring
- Métriques clés à surveiller :
  - Temps de réponse
  - Taux d'erreur
  - Utilisation CPU/Mémoire
  - Connexions actives

## 9. Plan d'Évolution

### 9.1 Étapes d'Évolution
1. Phase 1 (10 000 utilisateurs)
   - Infrastructure de base
   - Monitoring
   - Alerting

2. Phase 2 (50 000 utilisateurs)
   - Équilibrage de charge
   - Base de données répliquée
   - Cache distribué

3. Phase 3 (100 000 utilisateurs)
   - Microservices
   - Base de données partitionnée
   - Cache multi-régions
