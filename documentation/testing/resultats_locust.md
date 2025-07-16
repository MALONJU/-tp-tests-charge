# 6. Résultats des Tests avec Locust

Ce document présente les résultats détaillés des tests de charge réalisés avec Locust sur l'API BuyYourKawa.

## 6.1 Script Utilisé (`locustfile.py`)

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

## 6.2 Configuration du Test

Le test a été configuré avec les paramètres suivants :

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
    }
}
```

## 6.3 Résultats des Tests

### 6.3.1 Graphique de Performance

![Graphique Locust](/images/locust_performance.png)

*Figure 1: Temps de réponse et nombre de requêtes pendant la durée du test*

### 6.3.2 Tableau Récapitulatif

| Type          | Nom               | # Requêtes | # Échecs | Médiane (ms) | Moyenne (ms) | Min (ms) | Max (ms) | RPS    |
|---------------|-------------------|------------|----------|--------------|-------------|---------|---------|--------|
| POST          | /token            | 300        | 300      | 19           | 24.58       | 5       | 75      | 10.0   |
| Agrégé        | Total             | 300        | 300      | 19           | 24.58       | 5       | 75      | 10.0   |

### 6.3.3 Distribution des Temps de Réponse

| Nom               | 50%  | 66%  | 75%  | 80%  | 90%  | 95%  | 98%  | 99%  | 99.9% | 99.99% | 100% |
|-------------------|------|------|------|------|------|------|------|------|-------|--------|------|
| /token            | 19   | 25   | 30   | 35   | 45   | 53   | 65   | 74   | 75    | 75     | 75   |

## 6.4 Analyse des Résultats

### 6.4.1 Points Forts

- L'API est capable de gérer 300 utilisateurs simultanés en termes de traitement
- Les temps de réponse pour `/token` sont exceptionnels (19ms en médiane)
- La cohérence des temps de réponse est excellente (faible écart entre min/max)

### 6.4.2 Points Faibles

- L'échec d'authentification est total (100% des requêtes échouent)
- Les autres endpoints ne sont pas testés en raison de l'échec d'authentification
- Problème critique au niveau de l'authentification qui empêche l'exécution complète des tests

## 6.5 Rapport d'Exécution

Le test a été exécuté avec une simulation de 300 utilisateurs simultanés.

Les métriques importantes montrent :
- **Débit** : 10 requêtes par seconde
- **Temps de réponse moyen** : 24.58ms
- **Taux d'erreur global** : 100% (300 erreurs sur 300 requêtes)

### 6.5.1 Types d'Erreurs Rencontrées

| Code Erreur | Description | Occurrence | Endpoint principal |
|-------------|-------------|------------|-------------------|
| 401         | Non autorisé | 300 | `/token` |
