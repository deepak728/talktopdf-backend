import psycopg2
from psycopg2 import sql

from configs.db_config import DB_PARAMS


def get_db_connection():
    return psycopg2.connect(**DB_PARAMS)


def save_chunk_to_db(chunk, path):
    conn = get_db_connection()
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


async def save_summary_to_db(chunk_text, chunk_id, pdf_id):
    print(f"Saving this summary in db : {chunk_text}")
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO chunk_summary (pdf_id, chunk_id, summary)
    VALUES (%s, %s, %s) returning id;
    """

    try:
        cursor.execute(insert_query, (pdf_id, chunk_id, chunk_text))
        conn.commit()
        summary_id = cursor.fetchone()[0]

        return summary_id
    except psycopg2.Error as e:
        print("Error while saving chunk summary to db :", e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_pdf(pdf_id):
    conn = get_db_connection()
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


async def chunks_count(pdf_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    count_chunks_sql = "select count(*) from chunks where pdf_id =%s"

    try:
        cursor.execute(count_chunks_sql, (pdf_id,))
        conn.commit()
        chunks_count = cursor.fetchone()[0]

        return chunks_count
    except psycopg2.Error as e:
        print("Error while deleting data to db", e)
        return 0
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


async def fetch_summaries_batch(pdf_id, batch_size):
    def fetch_batch(cursor, pdf_id, batch_size, offset):
        fetch_sql = sql.SQL(
            "SELECT summary FROM chunk_summary WHERE pdf_id = %s ORDER BY id LIMIT %s OFFSET %s"
        )
        cursor.execute(fetch_sql, (pdf_id, batch_size, offset))
        return cursor.fetchall()

    def generate_concatenated_summaries(cursor, pdf_id, batch_size):
        offset = 0
        while True:
            batch = fetch_batch(cursor, pdf_id, batch_size, offset)
            if not batch:
                break
            concatenated_summary = ". ".join(row[0] for row in batch)
            concatenated_summary = concatenated_summary + "."
            yield concatenated_summary
            offset += len(batch)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        concatenated_summaries_generator = generate_concatenated_summaries(
            cursor, pdf_id, batch_size
        )
        return list(concatenated_summaries_generator)
    except psycopg2.Error as e:
        print("Error while fetching summaries from db", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
