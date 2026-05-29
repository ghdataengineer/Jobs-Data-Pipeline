from psycopg2.extras import execute_values
from app.db.postgres import get_connection


class CompanyRepository:

    @staticmethod
    def insert_companies(companies):

        if not companies:
            return 0

        conn = get_connection()
        cur = conn.cursor()

        try:
            values = []

            for company in companies:

                name = company.get("name")

                if not name:
                    continue

                logo_url = company.get("logo_url")
                website = company.get("website")
                url = company.get("url")

                # =========================
                # SANITIZAÇÃO ROBUSTA
                # =========================
                logo_url = CompanyRepository._normalize_field(logo_url)
                website = CompanyRepository._normalize_field(website)
                url = CompanyRepository._normalize_field(url)

                values.append((
                    name,
                    logo_url,
                    website,
                    url
                ))

            if not values:
                return 0

            execute_values(
                cur,
                """
                INSERT INTO dim_company (
                    name,
                    logo_url,
                    website,
                    url
                )
                VALUES %s
                ON CONFLICT (name) DO NOTHING
                """,
                values
            )

            conn.commit()

            print(f"[COMPANY] Inserted: {len(values)}")

            return len(values)

        except Exception as e:
            conn.rollback()
            print(f"[COMPANY] Error: {e}")
            raise

        finally:
            cur.close()
            conn.close()

    # =========================================
    # NORMALIZAÇÃO SEGURA
    # =========================================
    @staticmethod
    def _normalize_field(value):

        if isinstance(value, dict):
            return value.get("url") or value.get("value") or None

        if isinstance(value, list):
            return value[0] if value else None

        return value