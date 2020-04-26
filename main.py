from fastapi import FastAPI, HTTPException, Response, Cookie, Depends, status, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import RedirectResponse
import secrets
from hashlib import sha256

app = FastAPI()
app.patients_number = 1
app.dict_of_patients = {}
security = HTTPBasic()
app.secret_key = "very constatn and random secret, best 64 characters"
app.sessions = {}
app.users={"trudnY": "PaC13Nt"}
templates = Jinja2Templates(directory="templates")

class Patient(BaseModel):
    name: str
    surename: str

class PatientResponse(BaseModel):
    id: int
    patient: Patient
        
        

 
def is_cookie(s_token: str = Cookie(None)):
    if s_token not in app.sessions:
        s_token = None
    return s_token

def check_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    s_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
    app.sessions[s_token] = credentials.username
    return s_token



#@app.get('/patient/{pk}')
#def patient_detail(pk: int, response: Response, s_token: str = Depends(is_cookie)):
#    if s_token is None:
 #       response.status_code = status.HTTP_401_UNAUTHORIZED
  #      return "You are not allowed to be here!"
  #  if pk not in dict_of_patients:
   #     raise HTTPException(status_code=204, detail="No such patient")
  #  return dict_of_patients[pk]

#@app.post("/patient", response_model=PatientResponse)
#def receive_patient(pt: Patient, response: Response, s_token: str = Depends(is_cookie)):
 #   if s_token is None:
  #      response.status_code = status.HTTP_401_UNAUTHORIZED
  #      return "You are not allowed to be here!"
  #  dict_of_patients[app.patients_number] = pt
  #  app.patients_number += 1
  #  return Response(id=app.patients_number-1, patient=pt)       
        
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

@app.post("/patient")
def receive_patient(PatientData: Patient, response: Response, s_token: str = Depends(is_cookie)):
    if s_token is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "You are not allowed to be here!"
    id = app.patients_number
    app.dict_of_patients[id] = PatientData.dict()
    response.headers["Location"] = f"/patient/{id}"
    response.status_code = status.HTTP_302_FOUND
    app.patients_number += 1
   

@app.get("/patient")
def show_everyone(response: Response, s_token: str = Depends(is_cookie)):
    if s_token is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "You are not allowed to be here!"
    #response.status_code = status.HTTP_302_FOUND
    return app.dict_of_patients

@app.get("/patient/{id}")
def show_one(id: int, response: Response, s_token: str = Depends(is_cookie)):
    if s_token is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "You are not allowed to be here!"
    if id in app.dict_of_patients:
        return app.dict_of_patients[id]
    else:
        response.status_code = status.HTTP_204_NO_CONTENT

@app.delete("/patient/{id}")
def kill_him(id: int, response: Response, s_token: str = Depends(is_cookie)):
    if s_token is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "You are not allowed to be here!"
    app.dict_of_patients.pop(id, None)
    response.status_code = status.HTTP_204_NO_CONTENT
    #response.status_code = status.HTTP_302_FOUND


@app.get('/')
def welcome():
    return "Hello on '/' subpage! (Still during coronavirus pandemic :()"

@app.get('/welcome')
def welcome_on_welcome(request: Request, response: Response, s_token: str = Depends(is_cookie)):
    if s_token is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "You are not allowed to be here!"
    user = app.sessions[s_token]
    return templates.TemplateResponse("welcome.html", {"request": request, "user": user})
 
@app.post("/login")
def login(response: Response, s_token: str = Depends(check_user)):
    response.status_code = status.HTTP_302_FOUND
    response.headers["Location"] = "/welcome"
    response.set_cookie(key="s_token", value=s_token)
    
    
@app.post("/logout")
def logout(response: Response, s_token: str = Depends(is_cookie)):
    if s_token is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "You are not allowed to be here!"
    
    response.headers["Location"] = "/"
    response.status_code = status.HTTP_302_FOUND
    app.sessions.pop(s_token)





