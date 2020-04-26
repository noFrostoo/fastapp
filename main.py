# main.py
from typing import Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

app.counter = 0
paitiens = []

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
