import pandas as pd
import matplotlib.pyplot as plt
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import GPT2TokenizerFast

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
def count_tokens(pdfPage : str) ->int:
    return len(tokenizer.encode(pdfPage))

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 512,
    chunk_overlap  = 24,
    length_function = count_tokens)

async def readPdf(path):
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()
    print(pages)
    return await createChunks(pages)

def plot_tokens(chunks):
    token_counts =[]
    for chunk in chunks:
        token_counts.append(count_tokens(chunk.page_content))

    df = pd.DataFrame({'Token Count': token_counts})
    df.hist(bins=40, )
    plt.hist(df['Token Count'], bins=40, alpha=0.7, color='b', edgecolor='black')

    plt.show()

async def createChunks(pages):
    chunks = text_splitter.create_documents([pages[0].page_content])

    for chunk in chunks:
        temp = chunk.page_content.replace("\n", "\n")
        print(temp)
        print("")
    #plot_tokens(chunks)
    return chunks