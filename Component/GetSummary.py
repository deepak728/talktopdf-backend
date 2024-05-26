from Dao import PDF, Chunks
from Component import ReadAndSavePdf, OpenAPI


async def get_summary(path, words):
    pdf_id = await ReadAndSavePdf.read_and_save_pdf(path)
    level = 3
    pdf_summary = await compute_summary(pdf_id, words, level)

    return pdf_summary


async def compute_summary(pdf_id, words, level):
    chunk_count = await Chunks.chunks_count(pdf_id)
    print(f"Chunk count {chunk_count}")

    batch_size = chunk_count / level

    chunk_summary_list = await Chunks.fetch_summaries_batch(pdf_id, batch_size)
    concatenated_summary = " ".join(chunk_summary_list)

    print(f"chunk summary {concatenated_summary}")
    final_summary = await OpenAPI.get_summary_with_word_limit(
        concatenated_summary, words
    )
    print(f"final summary within {words} words: {final_summary}")

    return final_summary
