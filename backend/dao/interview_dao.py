from util.db_connection import create_connection
from model.interview import Interview


class InterviewDAO:

    def add_interview(self, interview, changed_by=None):
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
            """, (interview.application_id,))

            application = cursor.fetchone()

            if not application:
                return "NOT_FOUND"

            old_status = application[0]

            if old_status not in (
                "SHORTLISTED", "INTERVIEW_SCHEDULED"
            ):
                return "NOT_ELIGIBLE"

            cursor.execute("""
                INSERT INTO interview_rounds
                (
                    application_id, round_number, round_type,
                    scheduled_date, scheduled_time, mode,
                    interviewer_name, meeting_or_location, status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                interview.application_id,
                interview.round_number,
                interview.round_type,
                interview.scheduled_date,
                interview.scheduled_time,
                interview.mode,
                interview.interviewer_name,
                interview.meeting_or_location,
                interview.status
            ))

            interview_id = cursor.lastrowid

            if old_status == "SHORTLISTED":
                if changed_by is None:
                    raise ValueError(
                        "User ID is required for application history."
                    )

                cursor.execute("""
                    UPDATE applications
                    SET application_status = 'INTERVIEW_SCHEDULED'
                    WHERE application_id = %s
                """, (interview.application_id,))

                cursor.execute("""
                    INSERT INTO application_history
                    (
                        application_id,
                        old_status,
                        new_status,
                        remarks,
                        changed_by
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    interview.application_id,
                    "SHORTLISTED",
                    "INTERVIEW_SCHEDULED",
                    "Interview scheduled.",
                    changed_by
                ))

            db.commit()
            return interview_id

        except Exception:
            db.rollback()
            raise

        finally:
            cursor.close()
            db.close()
    def view_interviews(self):
        db = create_connection()
        if db is None:
            return []

        cursor = db.cursor()

        try:
            cursor.execute("""
                SELECT i.interview_id,
                       i.application_id,
                       c.full_name,
                       j.job_title,
                       i.round_number,
                       i.round_type,
                       i.scheduled_date,
                       i.scheduled_time,
                       i.mode,
                       i.interviewer_name,
                       i.status
                FROM interview_rounds i
                JOIN applications a
                    ON i.application_id = a.application_id
                JOIN candidates c
                    ON a.candidate_id = c.candidate_id
                JOIN jobs j
                    ON a.job_id = j.job_id
                ORDER BY i.scheduled_date, i.scheduled_time
            """)
            return cursor.fetchall()

        finally:
            cursor.close()
            db.close()

    def get_interview_by_id(self, interview_id):
        db = create_connection()
        if db is None:
            return None

        cursor = db.cursor()

        try:
            cursor.execute("""
                SELECT application_id, status
                FROM interview_rounds
                WHERE interview_id = %s
            """, (interview_id,))

            return cursor.fetchone()

        finally:
            cursor.close()
            db.close()

    def update_interview_status(
        self, interview_id, application_id, new_status, changed_by=None
    ):
        db = create_connection()
        if db is None:
            return None

        cursor = db.cursor()

        try:
            # Update interview round status.
            cursor.execute("""
                UPDATE interview_rounds
                SET status = %s
                WHERE interview_id = %s
                  AND application_id = %s
            """, (new_status, interview_id, application_id))

            if cursor.rowcount == 0:
                db.rollback()
                return None

            application_updated = False

            if new_status == "COMPLETED":
                # Check whether all rounds are completed.
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM interview_rounds
                    WHERE application_id = %s
                      AND status <> 'COMPLETED'
                """, (application_id,))

                pending_rounds = cursor.fetchone()[0]

                if pending_rounds == 0:
                    # Get previous application status.
                    cursor.execute("""
                        SELECT application_status
                        FROM applications
                        WHERE application_id = %s
                        FOR UPDATE
                    """, (application_id,))

                    application = cursor.fetchone()

                    if (
                        application
                        and application[0] == "INTERVIEW_SCHEDULED"
                    ):
                        if changed_by is None:
                            raise ValueError(
                                "User ID is required for application history."
                            )

                        cursor.execute("""
                            UPDATE applications
                            SET application_status = 'INTERVIEWED'
                            WHERE application_id = %s
                              AND application_status = 'INTERVIEW_SCHEDULED'
                        """, (application_id,))

                        application_updated = cursor.rowcount > 0

                        if application_updated:
                            cursor.execute("""
                                INSERT INTO application_history
                                (
                                    application_id,
                                    old_status,
                                    new_status,
                                    remarks,
                                    changed_by
                                )
                                VALUES (%s, %s, %s, %s, %s)
                            """, (
                                application_id,
                                "INTERVIEW_SCHEDULED",
                                "INTERVIEWED",
                                "All interview rounds completed.",
                                changed_by
                            ))

            db.commit()

            return {
                "interview_updated": True,
                "application_updated": application_updated
            }

        except Exception:
            db.rollback()
            raise

        finally:
            cursor.close()
            db.close()

    def delete_interview(self, interview_id):
        db = create_connection()
        if db is None:
            return False

        cursor = db.cursor()

        try:
            # Preserve feedback records; do not delete linked interviews.
            cursor.execute("""
                SELECT feedback_id
                FROM interview_feedback
                WHERE interview_id = %s
                LIMIT 1
            """, (interview_id,))

            if cursor.fetchone() is not None:
                return "HAS_FEEDBACK"

            cursor.execute("""
                DELETE FROM interview_rounds
                WHERE interview_id = %s
            """, (interview_id,))

            deleted = cursor.rowcount > 0
            db.commit()
            return deleted

        except Exception:
            db.rollback()
            raise

        finally:
            cursor.close()
            db.close()