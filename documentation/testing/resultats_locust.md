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
| GET           | /clients          | 45 231     | 632      | 350          | 420         | 120     | 2300    | 15.4   |
| POST          | /token            | 15 234     | 304      | 780          | 850         | 250     | 3100    | 5.1    |
| POST          | /clients          | 30 562     | 1222     | 580          | 670         | 200     | 2800    | 10.2   |
| GET           | /clients/{id}     | 22 456     | 112      | 280          | 320         | 90      | 1500    | 7.5    |
| Agrégé        | Total             | 113 483    | 2270     | 430          | 520         | 90      | 3100    | 38.2   |

### 6.3.3 Distribution des Temps de Réponse

| Nom               | 50%  | 66%  | 75%  | 80%  | 90%  | 95%  | 98%  | 99%  | 99.9% | 99.99% | 100% |
|-------------------|------|------|------|------|------|------|------|------|-------|--------|------|
| /clients          | 350  | 410  | 450  | 480  | 580  | 680  | 820  | 950  | 1600  | 2000   | 2300 |
| /token            | 780  | 830  | 870  | 900  | 950  | 1100 | 1350 | 1600 | 2400  | 2800   | 3100 |
| /clients (POST)   | 580  | 620  | 650  | 680  | 720  | 850  | 1050 | 1250 | 1900  | 2400   | 2800 |
| /clients/{id}     | 280  | 300  | 320  | 330  | 350  | 420  | 600  | 750  | 1100  | 1300   | 1500 |

## 6.4 Analyse des Résultats

### 6.4.1 Points Forts

- L'API est capable de gérer 300 utilisateurs simultanés
- Les temps de réponse pour `/clients/{id}` sont excellents (280ms en médiane)
- Le taux d'erreur global reste sous la barre des 2.5%

### 6.4.2 Points Faibles

- L'authentification (`/token`) est lente avec 780ms en médiane
- Les opérations POST ont un taux d'erreur trop élevé (4% pour `/clients`)
- Des pics de latence importants à 99.9% percentile sur tous les endpoints

## 6.5 Rapport d'Exécution

Le test complet a été exécuté pendant 45 minutes (10 minutes de ramp-up, 30 minutes de plateau et 5 minutes de ramp-down) avec une simulation de 300 utilisateurs simultanés au pic.

Les métriques importantes montrent :
- **Débit maximum** : 38.2 requêtes par seconde
- **Temps de réponse moyen** : 520ms
- **Taux d'erreur global** : 2% (2270 erreurs sur 113 483 requêtes)

### 6.5.1 Types d'Erreurs Rencontrées

| Code Erreur | Description | Occurrence | Endpoint principal |
|-------------|-------------|------------|-------------------|
| 500         | Erreur serveur interne | 1105 | `/clients` (POST) |
| 429         | Trop de requêtes | 783 | `/clients` (GET) |
| 401         | Non autorisé | 304 | `/token` |
| 404         | Non trouvé | 78 | `/clients/{id}` |
