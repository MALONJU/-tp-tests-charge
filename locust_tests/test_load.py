from locust import HttpUser, task, between
import json

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        # Authentification
        response = self.client.post(
            "/token",
            data={"username": "test", "password": "test"}
        )
        self.token = response.json()["access_token"]
        
    @task(3)
    def get_clients(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/clients", headers=headers)
    
    @task(2)
    def create_client(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post(
            "/clients",
            json={
                "name": "Test Client",
                "email": "test@example.com",
                "phone": "+33123456789",
                "address": {
                    "street": "123 Rue Test",
                    "city": "Paris",
                    "zip": "75000",
                    "country": "France"
                }
            },
            headers=headers
        )
    
    @task(1)
    def update_client(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        # Créer un client si nécessaire
        response = self.client.post(
            "/clients",
            json={
                "name": "Test Client",
                "email": "test@example.com",
                "phone": "+33123456789",
                "address": {
                    "street": "123 Rue Test",
                    "city": "Paris",
                    "zip": "75000",
                    "country": "France"
                }
            },
            headers=headers
        )
        client_id = response.json()["id"]
        
        # Mettre à jour le client
        self.client.put(
            f"/clients/{client_id}",
            json={
                "name": "Test Client Updated",
                "email": "test_updated@example.com",
                "phone": "+33123456789",
                "address": {
                    "street": "123 Rue Test Updated",
                    "city": "Paris",
                    "zip": "75000",
                    "country": "France"
                }
            },
            headers=headers
        )
