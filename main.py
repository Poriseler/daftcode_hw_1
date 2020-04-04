from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
app.patients_number = 0

class Patient(BaseModel):
    name: str
    surename: str

class Response(BaseModel):
    id: int
    patient: Patient

@app.post("/patient", response_model=Response)
def receive_patient(pt: Patient):
    app.patients_number += 1
    return Response(id=app.patients_number, patient=pt)

@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get('/method/')
def method_type():
    return {"method": "GET"}

@app.delete('/method/')
def method_type():
    return {"method": "DELETE"}

@app.put('/method/')
def method_type():
    return {"method": "PUT"}

@app.post('/method/')
def method_type():
    return {"method": "POST"}
