from fastapi import FastAPI, HTTPException, Response, Cookie, Depends, status
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import RedirectResponse
import secrets
from hashlib import sha256

app = FastAPI()
app.patients_number = -1
dict_of_patients = {}
security = HTTPBasic()
app.secret_key = "very constatn and random secret, best 64 characters"
app.sessions = {}
app.users={"trudnY": "PaC13Nt"}

class Patient(BaseModel):
    name: str
    surename: str

class Response(BaseModel):
    id: int
    patient: Patient

@app.get('/patient/{pk}')
def patient_detail(pk: int):
    if pk not in dict_of_patients:
        raise HTTPException(status_code=204, detail="No such patient")
    return dict_of_patients[pk]

@app.post("/patient", response_model=Response)
def receive_patient(pt: Patient):
    dict_of_patients[app.patients_number] = pt
    app.patients_number += 1
    return Response(id=app.patients_number-1, patient=pt)       
        
#@app.post("/patient", response_model=Response)
#def receive_patient(pt: Patient):
 #   app.patients_number += 1
 #   return Response(id=app.patients_number, patient=pt)

#@app.get('/')
#def hello_world():
  #  return {"message": "Hello World during the coronavirus pandemic!"}

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

#adding some features

@app.get('/')
def welcome():
    return "Hello on '/' subpage! (Still during coronavirus pandemic :()"

@app.get('/welcome')
def welcome_on_welcome():
    return "Hello on 'welcome' subpage!"

@app.post("/login")
def login_to_app(response: Response, credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
	if credentials.username in app.users and credentials.password == app.users[credentials.username]:
		s_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
		response.set_cookie(key="session_token", value=s_token)
		app.tokens.append(s_token)
		response.status_code = 307
		response.headers['Location'] = "/welcome"
		return RedirectResponse(url='/welcome')
		#return response
	else:
		raise HTTPException(status_code=401, detail="Niepoprawny login lub hasło")







