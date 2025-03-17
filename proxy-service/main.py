from fastapi import FastAPI
import random

app = FastAPI()

PROXIES = [
   
"http://118.85.208.193:80",
"http://41.223.26.11:8080",
"http://111.119.187.178:6000",
"http://111.119.187.178:80",
"http://111.119.187.178:8080",
   
]

@app.get("/get-proxy")
def get_proxy():
    return {"proxy": random.choice(PROXIES)}
