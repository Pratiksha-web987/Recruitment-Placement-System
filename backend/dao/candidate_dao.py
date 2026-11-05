from util.db_connection import create_connection
from model.candidate import Candidate


class CandidateDAO:

    def _map_candidate(self, row):
        if row is None:
            return None

        return Candidate(
            candidate_id=row[0],
            candidate_code=row[1],
            full_name=row[2],
            email=row[3],
            mobile=row[4],
            qualification=row[5],
            passing_year=row[6],
            percentage=float(row[7] or 0),
            backlog_count=row[8],
            primary_technology=row[9] or "",
            profile_status=row[10],
            placement_status=row[11]
        )

    def add_candidate(self, candidate):
        db = None
        cursor = None

        try:
            db = create_connection()
            if db is None:
                return None

            cursor = db.cursor()

            query = """
                INSERT INTO candidates
                (candidate_code, full_name, email, mobile,
                 qualification, passing_year, percentage,
                 backlog_count, primary_technology,
                 profile_status, placement_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,
                        'ACTIVE', 'NOT_PLACED')
            """

            values = (
                candidate.candidate_code,
                candidate.full_name,
                candidate.email,
                candidate.mobile,
                candidate.qualification,
                candidate.passing_year,
                candidate.percentage,
                candidate.backlog_count,
                candidate.primary_technology
            )

            cursor.execute(query, values)
            db.commit()

            candidate.candidate_id = cursor.lastrowid
            return candidate.candidate_id

        except Exception:
            if db:
                db.rollback()
            raise

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def view_candidates(self):
        db = None
        cursor = None

        try:
            db = create_connection()
            if db is None:
                return []

            cursor = db.cursor()

            query = """
                SELECT candidate_id, candidate_code, full_name,
                       email, mobile, qualification, passing_year,
                       percentage, backlog_count, primary_technology,
                       profile_status, placement_status
                FROM candidates
                ORDER BY candidate_id
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            return [self._map_candidate(row) for row in rows]

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def get_candidate_by_id(self, candidate_id):
        return self._find_one(
            "WHERE candidate_id = %s", (candidate_id,)
        )

    def find_by_email(self, email):
        return self._find_one("WHERE email = %s", (email,))

    def find_by_mobile(self, mobile):
        return self._find_one("WHERE mobile = %s", (mobile,))

    def find_by_technology(self, technology):
        db = None
        cursor = None

        try:
            db = create_connection()
            if db is None:
                return []

            cursor = db.cursor()

            query = """
                SELECT candidate_id, candidate_code, full_name,
                       email, mobile, qualification, passing_year,
                       percentage, backlog_count, primary_technology,
                       profile_status, placement_status
                FROM candidates
                WHERE primary_technology = %s
                ORDER BY full_name
            """

            cursor.execute(query, (technology,))
            rows = cursor.fetchall()

            return [self._map_candidate(row) for row in rows]

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def _find_one(self, condition, values):
        db = None
        cursor = None

        try:
            db = create_connection()
            if db is None:
                return None

            cursor = db.cursor()

            query = """
                SELECT candidate_id, candidate_code, full_name,
                       email, mobile, qualification, passing_year,
                       percentage, backlog_count, primary_technology,
                       profile_status, placement_status
                FROM candidates
            """ + condition

            cursor.execute(query, values)
            row = cursor.fetchone()

            return self._map_candidate(row)

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def update_candidate_mobile(self, candidate_id, new_mobile):
        db = None
        cursor = None

        try:
            db = create_connection()
            if db is None:
                return False

            cursor = db.cursor()

            query = """
                UPDATE candidates
                SET mobile = %s
                WHERE candidate_id = %s
            """

            cursor.execute(query, (new_mobile, candidate_id))
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

    def get_candidate_profile(self, candidate_id):
        db = None
        cursor = None

        try:
            db = create_connection()

            if db is None:
                return None

            cursor = db.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    candidate_id, candidate_code, full_name,
                    email, mobile, date_of_birth, gender,
                    qualification, college, university,
                    passing_year, percentage, cgpa,
                    backlog_count, primary_technology,
                    current_location, preferred_location,
                    profile_status, placement_status
                FROM candidates
                WHERE candidate_id = %s
            """, (candidate_id,))

            return cursor.fetchone()

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def update_candidate_profile(
        self, candidate_id, mobile, date_of_birth, gender,
        college, university, passing_year, percentage,
        cgpa, backlog_count, primary_technology,
        current_location, preferred_location
    ):
        db = None
        cursor = None

        try:
            db = create_connection()

            if db is None:
                return False

            cursor = db.cursor()

            cursor.execute("""
                UPDATE candidates
                SET
                    mobile = %s,
                    date_of_birth = %s,
                    gender = %s,
                    college = %s,
                    university = %s,
                    passing_year = %s,
                    percentage = %s,
                    cgpa = %s,
                    backlog_count = %s,
                    primary_technology = %s,
                    current_location = %s,
                    preferred_location = %s
                WHERE candidate_id = %s
            """, (
                mobile,
                date_of_birth,
                gender,
                college,
                university,
                passing_year,
                percentage,
                cgpa,
                backlog_count,
                primary_technology,
                current_location,
                preferred_location,
                candidate_id
            ))

            db.commit()
            return cursor.rowcount >= 0

        except Exception:
            if db:
                db.rollback()
            raise

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()            

    def delete_candidate(self, candidate_id):
        db = None
        cursor = None

        try:
            db = create_connection()
            if db is None:
                return False

            cursor = db.cursor()

            query = """
                DELETE FROM candidates
                WHERE candidate_id = %s
            """

            cursor.execute(query, (candidate_id,))
            db.commit()

            return cursor.rowcount > 0

        except Exception as error:
            if db:
                db.rollback()

            # Foreign key restriction: candidate has linked records.
            if getattr(error, "errno", None) == 1451:
                return "LINKED"

            raise

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()