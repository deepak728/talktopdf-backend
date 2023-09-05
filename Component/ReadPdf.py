from langchain.document_loaders import PyPDFLoader

async def readPdf(path):
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()
    print(pages)
    return pages

