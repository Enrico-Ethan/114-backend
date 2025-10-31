from typing import Annotated, List, Union

from fastapi import Body, Cookie, FastAPI, Form, Path
from pydantic import BaseModel, Field

class item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title= "The descruotuib if the items", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None
    tags: List[str] = []

app = FastAPI()

@app.post("/login")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    return {"username": username}

@app.get("/")
async def root():
    return{"message: Hello World!"}

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id":item_id}

'''
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

fake_items_db = [
    {"item_name" : "Foo"},             
    {"item_name": "Bar"},
    {"item_name": "Baz"} 
]
'''
@app.get("/items/")
async def read_item(ads_id: Annotated[str | None, Cookie()]) -> list[item]:
        return {"ads_id": ads_id}


'''
@app.post("/items/")
async def create_item(item: item):
    item_dict = item.model_dump() #item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
'''

@app.post("/items/")
async def create_item(item: item) -> item:
    return item

'''
@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated [int, path(title = "THe ID of the item to get", ge = 0, le = 1000)],
    q: str | None = None,
    item : Item | None = None,  
):
    result = {"item_id": item_id}
    if q:
        result.update({"q":q})
    return result
    if item:
            results.update({"items": item})
    return results
'''



@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results

