import pandas as pd
import matplotlib.pyplot as plt
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import GPT2TokenizerFast
from configs.db_config import DB_PARAMS
from Dao import PDF, Chunks
from Component import OpenAPI


tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
DB_PARAMS["dbname"] = "talk_to_pdf"


async def read_and_save_pdf(path):
    row_id = await PDF.find_pdf(path)
    if row_id is not None:
        return row_id

    row_id = await PDF.savePdfToDB(path)
    print(f"row_id : {row_id}")
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()

    await save_content_to_db(pages, path)
    # print(pages)
    return row_id


def count_tokens(pdfPage: str) -> int:
    return len(tokenizer.encode(pdfPage))


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
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
            print(f"\nchunk_content: {chunk_text}\n")

            chunk_id, pdf_id = Chunks.save_chunk_to_db(chunk_text, path)
            print(f"chunk_id {chunk_id}, pdf_id {pdf_id}")

            chunk_summary = await OpenAPI.get_summary(chunk_text)
            chunk_summary_id = await Chunks.save_summary_to_db(
                chunk_summary, chunk_id, pdf_id
            )
            print(f"chunk summary id : {chunk_summary_id}")


async def delete_pdf(path):
    pdf_id = await PDF.find_pdf(path)
    if pdf_id is None:
        print(f"Pdf does not exist")
        return False

    return Chunks.delete_pdf(pdf_id)
