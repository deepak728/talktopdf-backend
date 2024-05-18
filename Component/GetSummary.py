from Dao import PDF, Chunks
from Component import ReadAndSavePdf


async def get_summary(path):
    row_id = await ReadAndSavePdf.read_and_save_pdf(path)
    return row_id
