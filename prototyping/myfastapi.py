from enum import Enum
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='MavicMax', version='1.0')


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    print("QQQ", item_id, item.name)
    return {"item_name": item.name, "item_id": item_id}

@app.put("/items2/{item_id}")
def update_item2(item_id: int, mynumber:float, mystring:str):
    print("QQQ", item_id, mynumber, mystring)
    return {"item_name": mynumber, "item_id": item_id}

@app.put("/items3/{item_id}")
def update_item2(item_id: int, mynumber:float, mystring:str):
    print("QQQ", item_id, mynumber, mystring)
    r = {'a':'123', 'b':456}
    return r


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

import uvicorn

if __name__=="__main__":
    uvicorn.run("myfastapi:app",host='0.0.0.0', port=4557, reload=True, debug=True, workers=3)
