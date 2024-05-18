import psycopg2
from configs.db_config import DB_PARAMS


async def savePdfToDB(path):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    find_sql = "select * from uploaded_pdf where path = %s"
    insert_sql = "INSERT INTO uploaded_pdf (path) VALUES (%s) RETURNING id"
    try:
        cursor.execute(find_sql, (path,))
        conn.commit()
        row_id = cursor.fetchone()
        if row_id is not None:
            return row_id[0]

        cursor.execute(insert_sql, (path,))
        conn.commit()
        row_id = cursor.fetchone()[0]
        return row_id
    except psycopg2.Error as e:
        print("Error while saving pdf to db", e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
