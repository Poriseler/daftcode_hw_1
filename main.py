from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
app.patients_number = -1
dict_of_patients = {}

class Patient(BaseModel):
    name: str
    surename: str

class Response(BaseModel):
    id: int
    patient: Patient

@app.get('/post/{pk}')
def patient_detail(pk: int):
    if pk not in dict_of_patients:
        raise HTTPException(status_code=204, detail="No such patient")
    return dict_of_patients[pk]

@app.post("/patient", response_model=Response)
def receive_patient(pt: Patient):
    app.patients_number += 1
    dict_of_patients[app.patients_number] = pt
    return Response(id=app.patients_number, patient=pt)       
        
#@app.post("/patient", response_model=Response)
#def receive_patient(pt: Patient):
 #   app.patients_number += 1
 #   return Response(id=app.patients_number, patient=pt)

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
