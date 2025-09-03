from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import PlainTextResponse


class Characteristic(BaseModel):
    max_speed: float
    max_fuel_capacity: float

class Car(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: Characteristic

app = FastAPI()

cars: List[Car] = []

# Routes
@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    return "pong"

@app.post("/cars", status_code=201, response_model=Car)
async def create_car(car: Car):
    cars.append(car)
    return car

@app.get("/cars", response_model=List[Car])
async def get_cars():
    return cars

@app.get("/cars/{id}", response_model=Car)
async def get_car(id: str):
    for car in cars:
        if car.identifier == id:
            return car
    raise HTTPException(status_code=404, detail=f"Car with id {id} not found")


# Bonus
@app.put("/cars/{id}/characteristics", response_model=Car)
async def update_car_characteristics(id: str, characteristics: Characteristic):
    for car in cars:
        if car.identifier == id:
            car.characteristics = characteristics
            return car
    raise HTTPException(status_code=404, detail=f"Car with id {id} not found")
