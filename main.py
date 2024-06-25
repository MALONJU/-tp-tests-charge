# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from prometheus_client import Counter, generate_latest
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
REQUEST_COUNT = Counter('request_count', 'Total number of requests')

# Mock database
clients_db = []
users_db = {
    "user": {
        "username": "user",
        "password": "password"
    }
}

def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if not user or user["password"] != password:
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Client Service API"}

@app.post("/clients", response_model=Client)
def create_client(client: Client, token: str = Depends(oauth2_scheme)):
    REQUEST_COUNT.inc()
    current_user = get_current_user(token)
    client.id = str(uuid.uuid4())
    client.created_at = datetime.now()
    client.updated_at = datetime.now()
    clients_db.append(client)
    return client

@app.get("/clients", response_model=List[Client])
def get_clients(token: str = Depends(oauth2_scheme)):
    REQUEST_COUNT.inc()
    current_user = get_current_user(token)
    return clients_db

@app.get("/clients/{client_id}", response_model=Client)
def get_client(client_id: str, token: str = Depends(oauth2_scheme)):
    REQUEST_COUNT.inc()
    current_user = get_current_user(token)
    client = next((c for c in clients_db if c.id == client_id), None)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@app.put("/clients/{client_id}", response_model=Client)
def update_client(client_id: str, client: Client, token: str = Depends(oauth2_scheme)):
    REQUEST_COUNT.inc()
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
    REQUEST_COUNT.inc()
    current_user = get_current_user(token)
    global clients_db
    clients_db = [c for c in clients_db if c.id != client_id]
    return {"message": "Client deleted successfully"}

@app.get("/metrics")
def metrics():
    return generate_latest()
