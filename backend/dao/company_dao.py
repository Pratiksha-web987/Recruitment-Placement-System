from util.db_connection import create_connection
from model.company import Company


class CompanyDAO:

    def add_company(self, company):
        db = None
        cursor = None

        try:
            db = create_connection()
            if db is None:
                return None

            cursor = db.cursor()

            query = """
                INSERT INTO companies
                (company_code, company_name, industry, website,
                 location, company_type, hr_name, hr_email, hr_mobile)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                company.company_code, company.company_name,
                company.industry, company.website, company.location,
                company.company_type, company.hr_name,
                company.hr_email, company.hr_mobile
            )

            cursor.execute(query, values)
            db.commit()

            company.company_id = cursor.lastrowid
            return company.company_id

        except Exception:
            if db:
                db.rollback()
            raise

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def view_companies(self):
        db = None
        cursor = None

        try:
            db = create_connection()
            if db is None:
                return []

            cursor = db.cursor()

            query = """
                SELECT company_id, company_code, company_name,
                       industry, website, location, company_type,
                       hr_name, hr_email, hr_mobile, status
                FROM companies
                ORDER BY company_id
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            companies = []

            for row in rows:
                companies.append(
                    Company(
                        company_code=row[1],
                        company_name=row[2],
                        industry=row[3] or "",
                        website=row[4] or "",
                        location=row[5] or "",
                        company_type=row[6] or "",
                        hr_name=row[7] or "",
                        hr_email=row[8] or "",
                        hr_mobile=row[9] or "",
                        company_id=row[0],
                        status=row[10]
                    )
                )

            return companies

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def get_company_by_id(self, company_id):
        db = None
        cursor = None

        try:
            db = create_connection()
            if db is None:
                return None

            cursor = db.cursor()

            query = """
                SELECT company_id, company_code, company_name,
                       industry, website, location, company_type,
                       hr_name, hr_email, hr_mobile, status
                FROM companies
                WHERE company_id = %s
            """

            cursor.execute(query, (company_id,))
            row = cursor.fetchone()

            if row is None:
                return None

            return Company(
                company_code=row[1],
                company_name=row[2],
                industry=row[3] or "",
                website=row[4] or "",
                location=row[5] or "",
                company_type=row[6] or "",
                hr_name=row[7] or "",
                hr_email=row[8] or "",
                hr_mobile=row[9] or "",
                company_id=row[0],
                status=row[10]
            )

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def update_company(self, company):
        db = None
        cursor = None

        try:
            db = create_connection()
            if db is None:
                return False

            cursor = db.cursor()

            query = """
                UPDATE companies
                SET company_name = %s,
                    industry = %s,
                    website = %s,
                    location = %s,
                    company_type = %s,
                    hr_name = %s,
                    hr_email = %s,
                    hr_mobile = %s
                WHERE company_id = %s
            """

            values = (
                company.company_name, company.industry,
                company.website, company.location,
                company.company_type, company.hr_name,
                company.hr_email, company.hr_mobile,
                company.company_id
            )

            cursor.execute(query, values)
            db.commit()

            return cursor.rowcount > 0

        except Exception:
            if db:
                db.rollback()
            raise

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def delete_company(self, company_id):
        db = None
        cursor = None

        try:
            db = create_connection()

            if db is None:
                return False

            cursor = db.cursor()

            # Check linked jobs
            cursor.execute("""
                SELECT job_id
                FROM jobs
                WHERE company_id = %s
                LIMIT 1
            """, (company_id,))

            if cursor.fetchone() is not None:
                return "LINKED"

            # Check linked placements
            cursor.execute("""
                SELECT placement_id
                FROM placements
                WHERE company_id = %s
                LIMIT 1
            """, (company_id,))

            if cursor.fetchone() is not None:
                return "LINKED"

            cursor.execute("""
                DELETE FROM companies
                WHERE company_id = %s
            """, (company_id,))

            deleted = cursor.rowcount > 0
            db.commit()

            return deleted

        except Exception:
            if db:
                db.rollback()
            raise

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()