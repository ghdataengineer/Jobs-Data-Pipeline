import time
import psycopg2

from app.db.postgres import get_connection


def wait_for_db():
    print("⏳ Aguardando Postgres subir...")

    while True:
        try:
            conn = get_connection()
            conn.close()
            print("✅ Postgres disponível!")
            break
        except Exception:
            print("⏳ Ainda não disponível, tentando novamente...")
            time.sleep(2)