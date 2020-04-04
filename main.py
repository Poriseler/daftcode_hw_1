from fastapi import FastAPI
app = FastAPI()


@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get('/method')
def method_type():
    return {"method": "GET"}

@app.delete('/method')
def method_type():
    return {"method": "DELETE"}

@app.put('/method')
def method_type():
    return {"method": "PUT"}

@app.post('/method')
def method_type():
    return {"method": "POST"}
