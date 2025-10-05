from locust import HttpUser, task, between
import random

# Lista de usuarios de prueba que existen en la base de datos
USERS = [
    {"username": "admin", "password": "lab78"},
]

class DjangoUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Cada usuario virtual solo se va a autenticar una sola vez al iniciar"""
        user = random.choice(USERS)
        response = self.client.post("/api/token/", json=user)

        if response.status_code == 200:
            token = response.json().get("access")
            # Guardamos el token en los headers para futuras peticiones
            self.client.headers = {"Authorization": f"Bearer {token}"}
            print(f"Usuario autenticado: {user['username']}")
        else:
            print(f"Error al autenticar ({response.status_code}): {response.text}")

    @task
    def get_papers(self):
        """Prueba de carga sobre /api/papers/"""
        self.client.get("/api/papers/")
