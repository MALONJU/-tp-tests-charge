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
