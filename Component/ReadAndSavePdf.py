import pandas as pd
import matplotlib.pyplot as plt
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import GPT2TokenizerFast
from configs.db_config import DB_PARAMS
from Dao import UploadPDF, Chunks


tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
DB_PARAMS["dbname"] = "talk_to_pdf"


async def readPdf(path):
    row_id = await UploadPDF.savePdfToDB(path)
    print(f"row_id : {row_id}")
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()

    await save_content_to_db(pages, path)
    # print(pages)
    return pages


def count_tokens(pdfPage: str) -> int:
    return len(tokenizer.encode(pdfPage))


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0,
    length_function=count_tokens,
)


async def plot_tokens(chunks):
    token_counts = []
    for chunk in chunks:
        token_counts.append(count_tokens(chunk.page_content))

    df = pd.DataFrame({"Token Count": token_counts})
    df.hist(
        bins=40,
    )
    plt.hist(df["Token Count"], bins=40, alpha=0.7, color="b", edgecolor="black")

    plt.show()


async def save_content_to_db(pages, path):
    for page in pages:
        chunks = text_splitter.split_text(page.page_content)
        # print(chunks)
        for chunk in chunks:
            chunk_text = (
                chunk.page_content if hasattr(chunk, "page_content") else str(chunk)
            )
            print(f"chunk_content: {chunk_text}")
            print("")
            Chunks.save_chunk_to_db(chunk_text, path)
