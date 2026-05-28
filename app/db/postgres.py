import psycopg2


def get_connection():
    return psycopg2.connect(
        host="postgres",
        database="jobs_db",
        user="admin",
        password="admin",
        port=5432
    )