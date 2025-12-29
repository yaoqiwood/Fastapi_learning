import random
from typing import Annotated
from fastapi import FastAPI, Path, Query
from pydantic import AfterValidator

from constants.modelName import ModelName
from models.Item import Item


app = FastAPI()


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/items/readitem/{item_id}")
async def read_item_new(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.get("/items/read_item_new/{item_id}")
async def read_item_another(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    print(q)
    if q:
        item.update({"q": q})
        print(item)
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name == ModelName.resnet:
        return {"model_name": model_name, "message": "It's a ResNet"}
    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.post("/items/create")
async def create_item(item: Item):
    return item


@app.post("/items/create_item_another")
async def create_item_another(item: Item):
    item_dict = item.model_dump()
    print(item_dict)
    return item_dict


@app.post("/items/create_item_another/{item_id}")
async def create_item_another_1(item: Item, item_id: int):
    item_dict = item.model_dump()
    print(item_dict)
    return {"item_id": item_id, **item_dict}


@app.put("/items/update/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


@app.get("/items/get/")
async def get_item(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/get_new/")
async def get_new_item(
    q: str | None = Query(default=None, min_length=3, max_length=50)
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/get_list/")
async def get_list(q: Annotated[list[str] | None, Query()] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/get_list_another/")
async def get_list_another(q: list[str] | None = Query()):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/read_items_another/")
async def read_items_another(
    q: Annotated[
        list[int],
        Query(
            title="这个是用来测试输入 带int的列表的",
            description="请输入至少3个字符进行搜索",
        ),
    ] = [],
):
    query_items = {"q": q}
    return query_items


@app.get("/items/read_items_with_alias/")
async def read_items_with_alias(
    q: Annotated[
        list[str] | None,
        Query(
            alias="item-query",
            include_in_schema=False,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError("错了")
    return id


@app.get("/items/check_valid_id/")
async def read_items_check_valid_id(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "item": item}


@app.get("/newItem/{item_id}")
async def read_item_newItem(
    *, item_id: int = Path(title="The ID of the item to get", eq=1), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


if __name__ == "__main__":
    pass
