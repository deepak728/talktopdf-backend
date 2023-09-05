from fastapi import FastAPI
from pydantic import BaseModel
from Component.ReadPdf import readPdf


app = FastAPI()

class PathData(BaseModel):
    path: str
@app.get("/test")
async def test():
    return "this IS A TEST API"

@app.post("/uploadPdf")
async def uploadPdf(data: PathData):
    path = data.path
    content = await readPdf(path)
    return content

