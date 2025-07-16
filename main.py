from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from prometheus_client import Counter, Histogram, generate_latest
from models import Client, Address
from typing import List
from datetime import datetime, timedelta
import uuid
import jwt

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency', ['method', 'endpoint'])
REQUEST_SUCCESS = Counter('request_success', 'Number of successful requests', ['method', 'endpoint'])
REQUEST_FAILURE = Counter('request_failure', 'Number of failed requests', ['method', 'endpoint'])


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    method = request.method
    endpoint = request.url.path
    REQUEST_COUNT.labels(method, endpoint).inc()
    with REQUEST_LATENCY.labels(method, endpoint).time():
        response = await call_next(request)
        if 200 <= response.status_code < 300:
            REQUEST_SUCCESS.labels(method, endpoint).inc()
        else:
            REQUEST_FAILURE.labels(method, endpoint).inc()
    return response


def create_access_token(data):
    pass


def authenticate_user(username, password):
    pass


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), user=None, access_token=None):
    authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/clients", response_model=Client)
def create_client(client: Client, token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    client.id = str(uuid.uuid4())
    client.created_at = datetime.now()
    client.updated_at = datetime.now()
    clients_db.append(client)
    return client


@app.get("/clients", response_model=List[Client])
def get_clients(token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    return clients_db


@app.get("/clients/{client_id}", response_model=Client)
def get_client(client_id: str, token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    client = next((c for c in clients_db if c.id == client_id), None)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@app.put("/clients/{client_id}", response_model=Client)
def update_client(client_id: str, client: Client, token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    stored_client = next((c for c in clients_db if c.id == client_id), None)
    if not stored_client:
        raise HTTPException(status_code=404, detail="Client not found")
    stored_client.name = client.name
    stored_client.email = client.email
    stored_client.phone = client.phone
    stored_client.address = client.address
    stored_client.updated_at = datetime.now()
    return stored_client


@app.delete("/clients/{client_id}")
def delete_client(client_id: str, token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    global clients_db
    clients_db = [c for c in clients_db if c.id != client_id]
    return {"message": "Client deleted successfully"}


@app.get("/metrics")
def metrics():
    return generate_latest()
