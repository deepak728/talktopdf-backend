import psycopg2
from configs.db_config import DB_PARAMS


def save_chunk_to_db(chunk, path):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    find_SQL = "select id from uploaded_pdf where path = %s"
    insert_query = "INSERT INTO chunks (pdf_id, chunk) VALUES (%s, %s)"
    try:
        cursor.execute(find_SQL, (path,))
        conn.commit()
        pdf_id = cursor.fetchone()[0]
        if pdf_id == None:
            return None

        cursor.execute(insert_query, (pdf_id, chunk))
        conn.commit()
    except psycopg2.Error as e:
        print("Error while saving chunk to db", e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
