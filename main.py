from fastapi import FastAPI

from constants.modelName import ModelName


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


if __name__ == "__main__":
    pass
