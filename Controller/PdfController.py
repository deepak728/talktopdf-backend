import importlib

from fastapi import FastAPI
from pydantic import BaseModel

from Component import ReadAndSavePdf, GetSummary

app = FastAPI()


class PathData(BaseModel):
    path: str


@app.get("/test")
async def test():
    return "this IS A TEST API"


@app.post("/uploadPdf")
async def uploadPdf(data: PathData):
    path = data.path
    content = await ReadAndSavePdf.read_and_save_pdf(path)
    return content


@app.post("/getSummary")
async def getSummary(data: PathData):
    path = data.path
    content = await GetSummary.get_summary(path)
    return content
