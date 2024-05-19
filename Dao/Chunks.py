import psycopg2
from configs.db_config import DB_PARAMS


def save_chunk_to_db(chunk, path):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    find_SQL = "select id from uploaded_pdf where path = %s"
    insert_query = "INSERT INTO chunks (pdf_id, chunk) VALUES (%s, %s) returning id"
    try:
        cursor.execute(find_SQL, (path,))
        conn.commit()
        pdf_id = cursor.fetchone()[0]
        if pdf_id is None:
            return None

        cursor.execute(insert_query, (pdf_id, chunk))
        conn.commit()
        chunk_id = cursor.fetchone()[0]
        return chunk_id, pdf_id
    except psycopg2.Error as e:
        print("Error while saving chunk to db", e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def save_summary_to_db(chunk_text, chunk_id, row_id):
    return None


def delete_pdf(pdf_id):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()

    delete_summary_query = "DELETE FROM chunk_summary WHERE pdf_id = %s"
    delete_chunks_query = "DELETE FROM chunks WHERE pdf_id = %s"
    delete_pdf_query = "DELETE FROM uploaded_pdf where id = %s"

    try:
        cursor.execute(delete_summary_query, (pdf_id,))
        conn.commit()

        cursor.execute(delete_chunks_query, (pdf_id,))
        conn.commit()

        cursor.execute(delete_pdf_query, (pdf_id,))
        conn.commit()

        return True
    except psycopg2.Error as e:
        print("Error while deleting data to db", e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
