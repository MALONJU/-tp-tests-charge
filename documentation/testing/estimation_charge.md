# 3. Estimation de la Charge Utilisateur

Ce document définit les hypothèses de charge pour l'API BuyYourKawa et présente le modèle de simulation utilisé pour les tests.

## 3.1 Hypothèses de Trafic

### 3.1.1 Contexte Commercial

- **Campagne marketing** : Lancement d'une promotion spéciale avec budget marketing de €50 000
- **Public cible** : PME françaises
- **Durée de la campagne** : 2 semaines
- **Canaux marketing** : Réseaux sociaux, emailing, SEA et partenariats

### 3.1.2 Objectifs de Trafic

- **Objectif global** : 10 000 utilisateurs en 24h
- **Distribution des utilisateurs** :
  - 3% simultanés (300 utilisateurs)
  - 15% sur 1h (1 500 utilisateurs)
  - 50% sur 4h (5 000 utilisateurs)
  - 100% sur 24h (10 000 utilisateurs)

### 3.1.3 Justification des Hypothèses

- Taux de conversion marketing attendu : 5% (sur 200 000 impressions)
- Segmentation du marché : 40% de visiteurs professionnels
- Analyse des campagnes précédentes : pic à 3% d'utilisateurs simultanés

## 3.2 Profil Utilisateur

### 3.2.1 Personas Principaux

1. **Gestionnaire PME**
   - Actions principales :
     - Création de compte
     - Gestion des clients
     - Consultation des données
   - Fréquence : 10 actions/heure
   - Répartition : 60% des utilisateurs

2. **Responsable Marketing**
   - Actions principales :
     - Analyse des données
     - Export de rapports
     - Configuration des paramètres
   - Fréquence : 5 actions/heure
   - Répartition : 40% des utilisateurs

### 3.2.2 Scénarios Typiques

1. **Création Client**
   - Durée moyenne : 2 minutes
   - Actions : 5 requêtes
   - Fréquence : 100/heure
   - Endpoint sollicités :
     - `/token` (1 fois)
     - `/clients` POST (1 fois)
     - `/clients` GET (2 fois)
     - `/clients/{id}` GET (1 fois)

2. **Consultation Données**
   - Durée moyenne : 1 minute
   - Actions : 3 requêtes
   - Fréquence : 200/heure
   - Endpoints sollicités :
     - `/token` (1 fois)
     - `/clients` GET (1 fois)
     - `/clients/{id}` GET (1 fois)

## 3.3 Modèle de Charge

### 3.3.1 Ramp-Up (10 minutes)

- Durée : 10 minutes
- Augmentation linéaire
- De 0 à 300 utilisateurs
- Taux : 30 utilisateurs/minute

### 3.3.2 Plateau (30 minutes)

- Durée : 30 minutes
- 300 utilisateurs simultanés
- Distribution des actions :
  - 60% Lecture
  - 30% Écriture
  - 10% Export

### 3.3.3 Ramp-Down (5 minutes)

- Durée : 5 minutes
- Décroissance linéaire
- De 300 à 0 utilisateurs
- Taux : 60 utilisateurs/minute

## 3.4 Paramètres de Simulation Locust

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

## 3.5 Projection de Charge

### 3.5.1 Métriques Clés Attendues

- **Requêtes totales** : ~120 000 sur 45 minutes
- **Pic de RPS** : 40 requêtes/seconde
- **Distribution par endpoint** :
  - `/clients` GET : 60%
  - `/clients` POST : 20% 
  - `/token` : 15%
  - `/clients/{id}` : 5%

### 3.5.2 Dimensionnement Infrastructure

Basé sur ces projections, nous recommandons l'infrastructure suivante:
- **Application** : 3 serveurs (EC2 t3.large)
- **Base de données** : Instance RDS t3.large
- **Cache** : Redis t3.medium
- **Équilibreur de charge** : Application Load Balancer standard
