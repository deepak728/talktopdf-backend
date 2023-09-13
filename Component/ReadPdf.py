import pandas as pd
import matplotlib.pyplot as plt
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import GPT2TokenizerFast
from configs.db_config import DB_PARAMS
import psycopg2


tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
DB_PARAMS["dbname"] = "talk_to_pdf"


async def readPdf(path):
    await savePdfToDB(path)
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()
    print(pages)
    return await createChunks(pages)


async def savePdfToDB(path):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    insert_sql = "INSERT INTO uploaded_pdf (path) VALUES (%s);"
    try:
        cursor.execute(insert_sql, (path,))
        conn.commit()
    except psycopg2.Error as e:
        print("Error while saving to db", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def count_tokens(pdfPage: str) -> int:
    return len(tokenizer.encode(pdfPage))


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=251, chunk_overlap=24, length_function=count_tokens
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


async def createChunks(pages):
    chunks = text_splitter.create_documents([pages[0].page_content])

    for chunk in chunks:
        temp = chunk.page_content.replace("\n", "\n")
        print(temp)
        print("")
    # await plot_tokens(chunks)
    return chunks
