
from fastapi import FastAPI
from Controller.PdfController import app as pdf_app

app = FastAPI()
app.mount("/pdf", pdf_app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
