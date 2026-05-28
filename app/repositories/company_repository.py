from app.db.postgres import get_connection


class CompanyRepository:

    @staticmethod
    def insert_companies(companies):

        conn = get_connection()
        cur = conn.cursor()

        for company in companies:

            name = company.get("name")
            logo_url = company.get("logo_url")
            website = company.get("website")
            url = company.get("url")

            # 🔥 SANITIZAÇÃO (resolve seu erro)
            if isinstance(logo_url, dict):
                logo_url = logo_url.get("url")

            if isinstance(website, dict):
                website = website.get("value")

            if isinstance(url, dict):
                url = url.get("url")

            cur.execute("""
                INSERT INTO dim_company (name, logo_url, website, url)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (name) DO NOTHING
            """, (
                name,
                logo_url,
                website,
                url
            ))

        conn.commit()
        cur.close()
        conn.close()