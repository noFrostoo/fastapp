# main.py
from typing import Dict, List
from fastapi import FastAPI, Request, Query, Depends, HTTPException, status, Response, Cookie
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import RedirectResponse
import secrets
from hashlib import sha256
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.counter = 0
paitiens = []
security = HTTPBasic()
app.secret_key = "I love cookies and wired things come to play with me"
tookens = []

@app.get("/")
def hello_world():
    return {"message": "Witam na tym stosie"}

@app.get("/welcome")
def hello_world():
    return {"message": "Witam na tym stosie"}


@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello {name}"}


@app.get("/method")
def method_get():
    return {"method": "GET"}


@app.post("/method")
def method_post():
    return {"method": "POST"}


@app.put("/method")
def method_put():
    return {"method": "PUT"}


@app.delete("/method")
def method_delete():
    return {"method": "DELETE"}


@app.get('/counter')
def counter():
    app.counter += 1
    return str(app.counter)


class GiveMeSomethingRq(BaseModel):
    first_key: str


class GiveMeName(BaseModel):
    name: str
    surename: str


class ResponeName(BaseModel):
    id: int
    patient: Dict


class GiveMeSomethingResp(BaseModel):
    received: Dict
    constant_data: str = "python jest super"


@app.post("/dej/mi/coś", response_model=GiveMeSomethingResp)
def receive_something(rq: GiveMeSomethingRq):
    return GiveMeSomethingResp(received=rq.dict())


@app.post("/patient", response_model=ResponeName)
def receive_name(rq: GiveMeName):
    app.counter += 1
    paitiens.append(ResponeName(patient=rq.dict(), id=app.counter - 1).dict())
    return ResponeName(patient=rq.dict(), id=app.counter - 1)


@app.get("/patient/{pk}")
def find_patien(pk: int):
    for p in paitiens:
        try:
            if p['id'] == pk:
                return p['patient']
        except Exception:
            raise HTTPException(status_code=204, detail="Item not found")
    raise HTTPException(status_code=204, detail="Item not found")
    
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.post("/login")
def logiing_in(response: Response, username: str = Depends(get_current_username)):
    session_token = sha256(bytes(f"{username}{app.secret_key}")).hexdigest()
    respone = RedirectResponse("/Welcome")
    response.set_cookie(key="session_token", value=session_token)
    tookens.append(session_token)
    return response

@app.post("/logout")
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("Authorization", domain="localtest.me")
    return response
    
