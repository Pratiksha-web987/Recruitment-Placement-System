from util.db_connection import create_connection


class ReportDAO:

    def get_summary_report(self):
        db = create_connection()
        if db is None:
            return None

        cursor = None
        try:
            cursor = db.cursor()

            queries = [
                ("Total Candidates", "SELECT COUNT(*) FROM candidates"),
                ("Total Companies", "SELECT COUNT(*) FROM companies"),
                ("Total Jobs", "SELECT COUNT(*) FROM jobs"),
                ("Total Applications", "SELECT COUNT(*) FROM applications"),
                ("Total Interviews", "SELECT COUNT(*) FROM interview_rounds"),
                ("Total Placements", "SELECT COUNT(*) FROM placements")
            ]

            report = {}

            for title, query in queries:
                cursor.execute(query)
                report[title] = cursor.fetchone()[0]

            return report

        except Exception as e:
            print("Summary Report Error:", e)
            return None

        finally:
            if cursor:
                cursor.close()
            db.close()

    def get_selected_candidates(self):
        db = create_connection()
        if db is None:
            return None

        cursor = None
        try:
            cursor = db.cursor()

            cursor.execute("""
                SELECT COUNT(DISTINCT candidate_id)
                FROM applications
                WHERE application_status IN ('SELECTED', 'OFFERED')
            """)

            return cursor.fetchone()[0]

        except Exception as e:
            print("Selected Candidates Report Error:", e)
            return None

        finally:
            if cursor:
                cursor.close()
            db.close()

    def get_candidates_by_technology(self):
        db = create_connection()
        if db is None:
            return None

        cursor = None
        try:
            cursor = db.cursor()

            cursor.execute("""
                SELECT COALESCE(primary_technology, 'Not Specified'),
                       COUNT(*)
                FROM candidates
                GROUP BY primary_technology
                ORDER BY COUNT(*) DESC
            """)

            return cursor.fetchall()

        except Exception as e:
            print("Technology Report Error:", e)
            return None

        finally:
            if cursor:
                cursor.close()
            db.close()

    def get_open_jobs(self):
        db = create_connection()
        if db is None:
            return None

        cursor = None
        try:
            cursor = db.cursor()

            cursor.execute("""
                SELECT j.job_code, j.job_title, c.company_name,
                       j.location, j.openings, j.application_deadline
                FROM jobs j
                JOIN companies c ON j.company_id = c.company_id
                WHERE j.status = 'OPEN'
                ORDER BY j.application_deadline
            """)

            return cursor.fetchall()

        except Exception as e:
            print("Open Jobs Report Error:", e)
            return None

        finally:
            if cursor:
                cursor.close()
            db.close()

    def get_applications_by_status(self):
        db = create_connection()
        if db is None:
            return None

        cursor = None
        try:
            cursor = db.cursor()

            cursor.execute("""
                SELECT application_status, COUNT(*)
                FROM applications
                GROUP BY application_status
                ORDER BY application_status
            """)

            return cursor.fetchall()

        except Exception as e:
            print("Application Status Report Error:", e)
            return None

        finally:
            if cursor:
                cursor.close()
            db.close()

    def get_company_wise_placements(self):
        db = create_connection()
        if db is None:
            return None

        cursor = None
        try:
            cursor = db.cursor()

            cursor.execute("""
                SELECT c.company_name, COUNT(p.placement_id)
                FROM companies c
                LEFT JOIN placements p
                    ON c.company_id = p.company_id
                    AND p.placement_status IN ('ACTIVE', 'COMPLETED')
                GROUP BY c.company_id, c.company_name
                ORDER BY COUNT(p.placement_id) DESC
            """)

            return cursor.fetchall()

        except Exception as e:
            print("Company-wise Placement Report Error:", e)
            return None

        finally:
            if cursor:
                cursor.close()
            db.close()

    def get_placed_candidates(self):
        db = create_connection()
        if db is None:
            return None

        cursor = None
        try:
            cursor = db.cursor()

            cursor.execute("""
                SELECT DISTINCT c.candidate_code, c.full_name,
                       co.company_name, p.designation,
                       p.final_package_lpa
                FROM placements p
                JOIN candidates c
                    ON p.candidate_id = c.candidate_id
                JOIN companies co
                    ON p.company_id = co.company_id
                WHERE p.placement_status IN ('ACTIVE', 'COMPLETED')
                ORDER BY c.full_name
            """)

            return cursor.fetchall()

        except Exception as e:
            print("Placed Candidates Report Error:", e)
            return None

        finally:
            if cursor:
                cursor.close()
            db.close()

    def get_unplaced_candidates(self):
        db = create_connection()
        if db is None:
            return None

        cursor = None
        try:
            cursor = db.cursor()

            cursor.execute("""
                SELECT c.candidate_code, c.full_name,
                       c.qualification, c.primary_technology,
                       c.percentage
                FROM candidates c
                WHERE c.profile_status = 'ACTIVE'
                  AND NOT EXISTS (
                    SELECT 1
                    FROM placements p
                    WHERE p.candidate_id = c.candidate_id
                      AND p.placement_status IN ('ACTIVE', 'COMPLETED')
                  )
                ORDER BY c.full_name
            """)

            return cursor.fetchall()

        except Exception as e:
            print("Unplaced Candidates Report Error:", e)
            return None

        finally:
            if cursor:
                cursor.close()
            db.close()