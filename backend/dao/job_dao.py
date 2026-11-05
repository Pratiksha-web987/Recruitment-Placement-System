from util.db_connection import create_connection
from model.job import Job


class JobDAO:

    def add_job(self, job):
        db = None
        cursor = None

        try:
            db = create_connection()

            if db is None:
                return None

            cursor = db.cursor()

            query = """
                INSERT INTO jobs
                (
                    job_code, company_id, job_title, employment_type,
                    location, openings, min_package_lpa, max_package_lpa,
                    min_percentage, min_passing_year, max_passing_year,
                    max_backlogs, experience_min_years, qualification_rule,
                    posted_date, application_deadline, created_by
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
            """

            values = (
                job.job_code,
                job.company_id,
                job.job_title,
                job.employment_type,
                job.location,
                job.openings,
                job.min_package_lpa,
                job.max_package_lpa,
                job.min_percentage,
                job.min_passing_year,
                job.max_passing_year,
                job.max_backlogs,
                job.experience_min_years,
                job.qualification_rule,
                job.posted_date,
                job.application_deadline,
                job.created_by
            )

            cursor.execute(query, values)
            db.commit()

            job.job_id = cursor.lastrowid
            return job.job_id

        except Exception:
            if db:
                db.rollback()
            raise

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def view_jobs(self):
        db = None
        cursor = None

        try:
            db = create_connection()

            if db is None:
                return []

            cursor = db.cursor()

            cursor.execute("""
                SELECT job_id, job_code, company_id, job_title,
                       employment_type, location, openings,
                       min_package_lpa, max_package_lpa,
                       min_percentage, min_passing_year,
                       max_passing_year, max_backlogs,
                       experience_min_years, qualification_rule,
                       posted_date, application_deadline,
                       created_by, status
                FROM jobs
                ORDER BY job_id
            """)

            rows = cursor.fetchall()

            return [
                Job(
                    job_code=row[1],
                    company_id=row[2],
                    job_title=row[3],
                    employment_type=row[4],
                    location=row[5],
                    openings=row[6],
                    min_package_lpa=row[7],
                    max_package_lpa=row[8],
                    min_percentage=row[9],
                    min_passing_year=row[10],
                    max_passing_year=row[11],
                    max_backlogs=row[12],
                    experience_min_years=row[13],
                    qualification_rule=row[14] or "",
                    posted_date=row[15],
                    application_deadline=row[16],
                    created_by=row[17],
                    job_id=row[0],
                    status=row[18]
                )
                for row in rows
            ]

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def get_job_by_id(self, job_id):
        db = None
        cursor = None

        try:
            db = create_connection()

            if db is None:
                return None

            cursor = db.cursor()

            cursor.execute("""
                SELECT job_id, job_code, company_id, job_title,
                       employment_type, location, openings,
                       min_package_lpa, max_package_lpa,
                       min_percentage, min_passing_year,
                       max_passing_year, max_backlogs,
                       experience_min_years, qualification_rule,
                       posted_date, application_deadline,
                       created_by, status
                FROM jobs
                WHERE job_id = %s
            """, (job_id,))

            row = cursor.fetchone()

            if row is None:
                return None

            return Job(
                job_code=row[1],
                company_id=row[2],
                job_title=row[3],
                employment_type=row[4],
                location=row[5],
                openings=row[6],
                min_package_lpa=row[7],
                max_package_lpa=row[8],
                min_percentage=row[9],
                min_passing_year=row[10],
                max_passing_year=row[11],
                max_backlogs=row[12],
                experience_min_years=row[13],
                qualification_rule=row[14] or "",
                posted_date=row[15],
                application_deadline=row[16],
                created_by=row[17],
                job_id=row[0],
                status=row[18]
            )

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def update_job(self, job):
        db = None
        cursor = None

        try:
            db = create_connection()

            if db is None:
                return False

            cursor = db.cursor()

            cursor.execute("""
                SELECT job_id
                FROM jobs
                WHERE job_id = %s
            """, (job.job_id,))

            if cursor.fetchone() is None:
                return False

            cursor.execute("""
                UPDATE jobs
                SET job_title = %s,
                    location = %s,
                    openings = %s,
                    min_package_lpa = %s,
                    max_package_lpa = %s,
                    application_deadline = %s
                WHERE job_id = %s
            """, (
                job.job_title,
                job.location,
                job.openings,
                job.min_package_lpa,
                job.max_package_lpa,
                job.application_deadline,
                job.job_id
            ))

            db.commit()
            return True

        except Exception:
            if db:
                db.rollback()
            raise

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    def update_job_status(self, job_id, status):
        db = None
        cursor = None

        try:
            db = create_connection()

            if db is None:
                return False

            cursor = db.cursor()

            cursor.execute(
                "SELECT job_id FROM jobs WHERE job_id = %s",
                (job_id,)
            )

            if cursor.fetchone() is None:
                return False

            cursor.execute("""
                UPDATE jobs
                SET status = %s
                WHERE job_id = %s
            """, (status, job_id))

            db.commit()
            return True

        except Exception:
            if db:
                db.rollback()
            raise

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def delete_job(self, job_id):
        db = None
        cursor = None

        try:
            db = create_connection()

            if db is None:
                return False

            cursor = db.cursor()

            # Check linked applications.
            cursor.execute("""
                SELECT application_id
                FROM applications
                WHERE job_id = %s
                LIMIT 1
            """, (job_id,))

            if cursor.fetchone() is not None:
                return "LINKED"

            # Check linked placements.
            cursor.execute("""
                SELECT placement_id
                FROM placements
                WHERE job_id = %s
                LIMIT 1
            """, (job_id,))

            if cursor.fetchone() is not None:
                return "LINKED"

            # Check linked job skills.
            cursor.execute("""
                SELECT job_id
                FROM job_skills
                WHERE job_id = %s
                LIMIT 1
            """, (job_id,))

            if cursor.fetchone() is not None:
                return "LINKED"

            cursor.execute("""
                DELETE FROM jobs
                WHERE job_id = %s
            """, (job_id,))

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