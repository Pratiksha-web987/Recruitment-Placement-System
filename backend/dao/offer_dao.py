from util.db_connection import create_connection
from model.offer import Offer


class OfferDAO:

    def add_offer(self, offer, changed_by):
        db = create_connection()

        if db is None:
            return None

        cursor = db.cursor()

        try:
            cursor.execute("""
                SELECT application_status
                FROM applications
                WHERE application_id = %s
                FOR UPDATE
            """, (offer.application_id,))

            application = cursor.fetchone()

            if application is None:
                return "NOT_FOUND"

            if application[0] != "SELECTED":
                return "NOT_SELECTED"

            cursor.execute("""
                INSERT INTO offers
                (
                    offer_code, application_id, designation,
                    offered_package_lpa, offer_date,
                    expected_joining_date, offer_status, remarks
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                offer.offer_code,
                offer.application_id,
                offer.designation,
                offer.offered_package_lpa,
                offer.offer_date,
                offer.expected_joining_date,
                offer.offer_status,
                offer.remarks
            ))

            offer_id = cursor.lastrowid

            cursor.execute("""
                UPDATE applications
                SET application_status = 'OFFERED'
                WHERE application_id = %s
            """, (offer.application_id,))

            cursor.execute("""
                INSERT INTO application_history
                (
                    application_id, old_status, new_status,
                    remarks, changed_by
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                offer.application_id,
                "SELECTED",
                "OFFERED",
                "Offer created.",
                changed_by
            ))

            db.commit()
            return offer_id

        except Exception:
            db.rollback()
            raise

        finally:
            cursor.close()
            db.close()

    def view_offers(self):
        db = create_connection()

        if db is None:
            return []

        cursor = db.cursor()

        try:
            cursor.execute("""
                SELECT
                    o.offer_id,
                    o.offer_code,
                    c.full_name,
                    j.job_title,
                    o.designation,
                    o.offered_package_lpa,
                    o.offer_date,
                    o.expected_joining_date,
                    o.offer_status
                FROM offers o
                JOIN applications a
                    ON o.application_id = a.application_id
                JOIN candidates c
                    ON a.candidate_id = c.candidate_id
                JOIN jobs j
                    ON a.job_id = j.job_id
                ORDER BY o.offer_id
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            db.close()

    def get_offer_by_id(self, offer_id):
        db = create_connection()

        if db is None:
            return None

        cursor = db.cursor()

        try:
            cursor.execute("""
                SELECT offer_id, offer_code, application_id,
                       offer_status, designation
                FROM offers
                WHERE offer_id = %s
            """, (offer_id,))

            return cursor.fetchone()

        finally:
            cursor.close()
            db.close()

    def update_offer(self, offer_id, field, value, changed_by=None):
        allowed_fields = {
            "designation": "designation",
            "package": "offered_package_lpa",
            "joining_date": "expected_joining_date",
            "status": "offer_status",
            "remarks": "remarks"
        }

        if field not in allowed_fields:
            return False

        db = create_connection()

        if db is None:
            return False

        cursor = db.cursor()

        try:
            cursor.execute("""
                SELECT application_id, offer_status
                FROM offers
                WHERE offer_id = %s
                FOR UPDATE
            """, (offer_id,))

            offer = cursor.fetchone()

            if offer is None:
                return False

            application_id = offer[0]
            old_offer_status = offer[1]
            column = allowed_fields[field]

            cursor.execute(
                f"""
                UPDATE offers
                SET {column} = %s
                WHERE offer_id = %s
                """,
                (value, offer_id)
            )

            updated = cursor.rowcount > 0

            if field == "status" and value != old_offer_status:

                cursor.execute("""
                    SELECT application_status
                    FROM applications
                    WHERE application_id = %s
                    FOR UPDATE
                """, (application_id,))

                application = cursor.fetchone()

                if application is None:
                    db.rollback()
                    return False

                old_application_status = application[0]
                new_application_status = old_application_status

                if value == "REJECTED":
                    new_application_status = "REJECTED"

                elif value in ("OFFERED", "ACCEPTED"):
                    if old_application_status == "REJECTED":
                        new_application_status = "OFFERED"

                if new_application_status != old_application_status:

                    if changed_by is None:
                        raise ValueError(
                            "User ID is required for application history."
                        )

                    cursor.execute("""
                        UPDATE applications
                        SET application_status = %s
                        WHERE application_id = %s
                    """, (new_application_status, application_id))

                    cursor.execute("""
                        INSERT INTO application_history
                        (
                            application_id, old_status, new_status,
                            remarks, changed_by
                        )
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        application_id,
                        old_application_status,
                        new_application_status,
                        f"Application status changed after offer status "
                        f"changed from {old_offer_status} to {value}.",
                        changed_by
                    ))

            db.commit()
            return updated

        except Exception:
            db.rollback()
            raise

        finally:
            cursor.close()
            db.close()

    def delete_offer(self, offer_id, changed_by):
        db = create_connection()

        if db is None:
            return False

        cursor = db.cursor()

        try:
            cursor.execute("""
                SELECT application_id, offer_code
                FROM offers
                WHERE offer_id = %s
                FOR UPDATE
            """, (offer_id,))

            offer = cursor.fetchone()

            if offer is None:
                return "NOT_FOUND"

            cursor.execute("""
                SELECT placement_id
                FROM placements
                WHERE offer_id = %s
                LIMIT 1
            """, (offer_id,))

            if cursor.fetchone():
                return "LINKED"

            application_id = offer[0]

            cursor.execute("""
                SELECT application_status
                FROM applications
                WHERE application_id = %s
                FOR UPDATE
            """, (application_id,))

            application = cursor.fetchone()

            if application is None:
                return "NOT_FOUND"

            old_application_status = application[0]

            cursor.execute("""
                DELETE FROM offers
                WHERE offer_id = %s
            """, (offer_id,))

            if old_application_status in ("OFFERED", "REJECTED"):
                cursor.execute("""
                    UPDATE applications
                    SET application_status = 'SELECTED'
                    WHERE application_id = %s
                """, (application_id,))

                cursor.execute("""
                    INSERT INTO application_history
                    (
                        application_id, old_status, new_status,
                        remarks, changed_by
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    application_id,
                    old_application_status,
                    "SELECTED",
                    "Offer deleted.",
                    changed_by
                ))

            db.commit()
            return offer

        except Exception:
            db.rollback()
            raise

        finally:
            cursor.close()
            db.close()