from dataclasses import dataclass
from enum import Enum
from pprint import pprint
from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel
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


class ItemQ(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []

class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None


class UserInDB(BaseModel):
    username: str
    username2: str
    hashed_password: str
    email: str
    full_name: Optional[str] = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn) -> UserInDB:
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    user_in_db.username = 'overridden'
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

@app.post("/user2/", response_model=UserInDB)
async def create_user2(user_in: UserIn) -> UserInDB:
    user_in_db = UserInDB(**user_in.dict(), hashed_password='qazsaa', username2 = 'hejhopp')
    return user_in_db



@dataclass
class Item:
    name: str
    price: float
    description: Optional[str] = None
    tax: Optional[float] = None
@dataclass
class Item_return:
    name: str
    price: float
    description: Optional[str] = None
    tax: Optional[float] = None
@app.post("/itemsDataclass/{value}")
async def create_item(item: Item, value: int):
    '''
    Mydoc
    :param item:
    :return:
    '''
    return_item=Item_return(name='A', price=12, description='hejhopp2')
    return_item.tax=19.9
    return return_item

@app.post("/items_plain/{value}")
async def create_item(value: int) -> int:
    '''
    Mydoc
    :param item:
    :return:
    '''
    return value*10


import uvicorn

if __name__=="__main__":
    uvicorn.run("myfastapi:app",host='0.0.0.0', port=4557, reload=True, debug=True, workers=3)
