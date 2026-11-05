from util.db_connection import create_connection
from model.placement import Placement


class PlacementDAO:

    def add_placement(self, placement):
        db = create_connection()

        if db is None:
            return None

        cursor = db.cursor()

        try:
            cursor.execute("""
                SELECT candidate_id
                FROM candidates
                WHERE candidate_id = %s
                FOR UPDATE
            """, (placement.candidate_id,))

            if cursor.fetchone() is None:
                return "INVALID_CANDIDATE"

            cursor.execute("""
                SELECT o.offer_id
                FROM offers o
                JOIN applications a
                    ON o.application_id = a.application_id
                JOIN jobs j
                    ON a.job_id = j.job_id
                WHERE o.offer_id = %s
                  AND a.candidate_id = %s
                  AND j.company_id = %s
                  AND j.job_id = %s
                  AND o.offer_status = 'ACCEPTED'
            """, (
                placement.offer_id,
                placement.candidate_id,
                placement.company_id,
                placement.job_id
            ))

            if cursor.fetchone() is None:
                return "INVALID_OFFER"

            cursor.execute("""
                SELECT placement_id
                FROM placements
                WHERE candidate_id = %s
                  AND placement_status <> 'CANCELLED'
            """, (placement.candidate_id,))

            if cursor.fetchone() is not None:
                return "EXISTING_PLACEMENT"

            cursor.execute("""
                INSERT INTO placements
                (
                    candidate_id, company_id, job_id, offer_id,
                    designation, final_package_lpa,
                    expected_joining_date, actual_joining_date,
                    joining_status, placement_status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                placement.candidate_id,
                placement.company_id,
                placement.job_id,
                placement.offer_id,
                placement.designation,
                placement.final_package_lpa,
                placement.expected_joining_date,
                placement.actual_joining_date,
                placement.joining_status,
                placement.placement_status
            ))

            placement_id = cursor.lastrowid

            if placement.placement_status != "CANCELLED":
                cursor.execute("""
                    UPDATE candidates
                    SET placement_status = 'PLACED'
                    WHERE candidate_id = %s
                """, (placement.candidate_id,))

            db.commit()
            return placement_id

        except Exception:
            db.rollback()
            raise

        finally:
            cursor.close()
            db.close()

    def view_placements(self):
        db = create_connection()

        if db is None:
            return []

        cursor = db.cursor()

        try:
            cursor.execute("""
                SELECT p.placement_id, c.full_name,
                       co.company_name, j.job_title,
                       p.designation, p.final_package_lpa,
                       p.expected_joining_date,
                       p.actual_joining_date,
                       p.joining_status, p.placement_status
                FROM placements p
                JOIN candidates c
                    ON p.candidate_id = c.candidate_id
                JOIN companies co
                    ON p.company_id = co.company_id
                JOIN jobs j
                    ON p.job_id = j.job_id
                ORDER BY p.placement_id
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            db.close()

    def get_placement_by_id(self, placement_id):
        db = create_connection()

        if db is None:
            return None

        cursor = db.cursor()

        try:
            cursor.execute("""
                SELECT candidate_id, company_id, job_id,
                       joining_status, placement_status
                FROM placements
                WHERE placement_id = %s
            """, (placement_id,))

            return cursor.fetchone()

        finally:
            cursor.close()
            db.close()

    def update_placement(
        self, placement_id, joining_status,
        placement_status, actual_date
    ):
        db = create_connection()

        if db is None:
            return False

        cursor = db.cursor()

        try:
            cursor.execute("""
                SELECT candidate_id
                FROM placements
                WHERE placement_id = %s
                FOR UPDATE
            """, (placement_id,))

            record = cursor.fetchone()

            if record is None:
                return False

            candidate_id = record[0]

            cursor.execute("""
                UPDATE placements
                SET joining_status = %s,
                    placement_status = %s,
                    actual_joining_date = %s
                WHERE placement_id = %s
            """, (
                joining_status,
                placement_status,
                actual_date,
                placement_id
            ))

            cursor.execute("""
                SELECT COUNT(*)
                FROM placements
                WHERE candidate_id = %s
                  AND placement_status <> 'CANCELLED'
            """, (candidate_id,))

            placement_count = cursor.fetchone()[0]

            candidate_status = (
                "PLACED" if placement_count > 0 else "NOT_PLACED"
            )

            cursor.execute("""
                UPDATE candidates
                SET placement_status = %s
                WHERE candidate_id = %s
            """, (candidate_status, candidate_id))

            db.commit()
            return True

        except Exception:
            db.rollback()
            raise

        finally:
            cursor.close()
            db.close()

    def delete_placement(self, placement_id):
        db = create_connection()

        if db is None:
            return False

        cursor = db.cursor()

        try:
            cursor.execute("""
                SELECT candidate_id
                FROM placements
                WHERE placement_id = %s
                FOR UPDATE
            """, (placement_id,))

            record = cursor.fetchone()

            if record is None:
                return False

            candidate_id = record[0]

            cursor.execute("""
                DELETE FROM placements
                WHERE placement_id = %s
            """, (placement_id,))

            deleted = cursor.rowcount > 0

            if deleted:
                cursor.execute("""
                    SELECT placement_id
                    FROM placements
                    WHERE candidate_id = %s
                      AND placement_status <> 'CANCELLED'
                    LIMIT 1
                """, (candidate_id,))

                remaining_placement = cursor.fetchone()

                new_status = (
                    "PLACED" if remaining_placement else "NOT_PLACED"
                )

                cursor.execute("""
                    UPDATE candidates
                    SET placement_status = %s
                    WHERE candidate_id = %s
                """, (new_status, candidate_id))

            db.commit()
            return deleted

        except Exception:
            db.rollback()
            raise

        finally:
            cursor.close()
            db.close()