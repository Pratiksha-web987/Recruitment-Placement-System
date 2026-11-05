from util.db_connection import create_connection


class InterviewFeedbackDAO:

    def add_feedback(self, interview_id, technical, communication,
                     problem_solving, overall, recommendation,
                     remarks, submitted_by):

        db = create_connection()
        if db is None:
            return None

        cursor = db.cursor()

        try:
            cursor.execute("""
                SELECT interview_id
                FROM interview_rounds
                WHERE interview_id = %s
            """, (interview_id,))

            if cursor.fetchone() is None:
                return "INTERVIEW_NOT_FOUND"

            cursor.execute("""
                SELECT feedback_id
                FROM interview_feedback
                WHERE interview_id = %s
            """, (interview_id,))

            if cursor.fetchone():
                return "FEEDBACK_EXISTS"

            cursor.execute("""
                INSERT INTO interview_feedback
                (
                    interview_id, technical_rating,
                    communication_rating, problem_solving_rating,
                    overall_rating, recommendation, remarks,
                    submitted_by
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                interview_id, technical, communication,
                problem_solving, overall, recommendation,
                remarks, submitted_by
            ))

            feedback_id = cursor.lastrowid
            db.commit()
            return feedback_id

        except Exception:
            db.rollback()
            raise

        finally:
            cursor.close()
            db.close()

    def view_feedback(self):
        db = create_connection()
        if db is None:
            return []

        cursor = db.cursor()

        try:
            cursor.execute("""
                SELECT
                    f.feedback_id,
                    f.interview_id,
                    c.full_name,
                    f.technical_rating,
                    f.communication_rating,
                    f.problem_solving_rating,
                    f.overall_rating,
                    f.recommendation,
                    f.remarks,
                    f.submitted_by,
                    f.submitted_at
                FROM interview_feedback f
                JOIN interview_rounds i
                    ON f.interview_id = i.interview_id
                JOIN applications a
                    ON i.application_id = a.application_id
                JOIN candidates c
                    ON a.candidate_id = c.candidate_id
                ORDER BY f.submitted_at DESC
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            db.close()