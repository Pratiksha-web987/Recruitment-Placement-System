from datetime import date
from util.db_connection import create_connection
from model.application import Application


class ApplicationDAO:

    def check_eligibility(self, candidate_id, job_id):
        from datetime import date

        db = None
        cursor = None

        try:
            db = create_connection()

            if db is None:
                return "PENDING", "Database connection failed"

            cursor = db.cursor(dictionary=True)
            # Check Candidate separately
            cursor.execute("""
                SELECT candidate_id
                FROM candidates
                WHERE candidate_id = %s
            """, (candidate_id,))

            if not cursor.fetchone():
                return "PENDING", "Candidate not found"

            # Check Job separately
            cursor.execute("""
                SELECT job_id
                FROM jobs
                WHERE job_id = %s
            """, (job_id,))

            if not cursor.fetchone():
                return "PENDING", "Job not found"

            cursor.execute("""
                SELECT
                    c.qualification, c.passing_year,
                    c.percentage, c.backlog_count,
                    c.profile_status,
                    j.min_percentage, j.min_passing_year,
                    j.max_passing_year, j.max_backlogs,
                    j.qualification_rule, j.status AS job_status,
                    j.application_deadline
                FROM candidates c
                JOIN jobs j ON j.job_id = %s
                WHERE c.candidate_id = %s
            """, (job_id, candidate_id))

            data = cursor.fetchone()

            if not data:
                return "PENDING", "Candidate or Job not found"

            reasons = []

            # Candidate and Job status
            if data["profile_status"] != "ACTIVE":
                reasons.append("Candidate is not active")

            if data["job_status"] != "OPEN":
                reasons.append("Job is not open")

            # Application deadline
            deadline = data["application_deadline"]

            if deadline and deadline < date.today():
                reasons.append("Application deadline has passed")

            # Qualification check
            qualification = (data["qualification"] or "").upper()
            rule = data["qualification_rule"] or ""

            allowed = [
                item.strip().upper()
                for item in rule.split("/")
                if item.strip()
            ]

            if allowed and qualification not in allowed:
                reasons.append("Qualification does not match")

            # Percentage check
            percentage = data["percentage"]
            minimum = data["min_percentage"]

            if minimum is not None and (
                percentage is None or percentage < minimum
            ):
                reasons.append("Minimum percentage not satisfied")

            # Passing year check
            passing_year = data["passing_year"]

            if (
                data["min_passing_year"] is not None
                or data["max_passing_year"] is not None
            ):
                if passing_year is None:
                    reasons.append("Passing year is not available")
                else:
                    if (
                        data["min_passing_year"] is not None
                        and passing_year < data["min_passing_year"]
                    ):
                        reasons.append("Passing year is below minimum")

                    if (
                        data["max_passing_year"] is not None
                        and passing_year > data["max_passing_year"]
                    ):
                        reasons.append("Passing year exceeds maximum")

            # Backlog check
            backlog_count = data["backlog_count"] or 0

            if (
                data["max_backlogs"] is not None
                and backlog_count > data["max_backlogs"]
            ):
                reasons.append("Backlog limit exceeded")

            # Mandatory Skills Matching
            cursor.execute("""
                SELECT
                    s.skill_name,
                    js.minimum_level,
                    cs.proficiency_level
                FROM job_skills js
                JOIN skills s
                    ON s.skill_id = js.skill_id
                    AND s.is_active = 1
                LEFT JOIN candidate_skills cs
                    ON cs.skill_id = js.skill_id
                    AND cs.candidate_id = %s
                WHERE js.job_id = %s
                  AND js.mandatory_flag = 1
            """, (candidate_id, job_id))

            required_skills = cursor.fetchall()

            level_rank = {
                "BASIC": 1,
                "INTERMEDIATE": 2,
                "ADVANCED": 3
            }

            for skill in required_skills:
                skill_name = skill["skill_name"]
                minimum_level = skill["minimum_level"]
                candidate_level = skill["proficiency_level"]

                if candidate_level is None:
                    reasons.append(
                        f"Mandatory skill missing: {skill_name}"
                    )
                    continue

                if minimum_level is not None:
                    required_rank = level_rank.get(
                        minimum_level.upper()
                    )

                    candidate_rank = level_rank.get(
                        candidate_level.upper()
                    )

                    if (
                        required_rank is None
                        or candidate_rank is None
                        or candidate_rank < required_rank
                    ):
                        reasons.append(
                            f"Insufficient proficiency in {skill_name}"
                        )

            if reasons:
                return "NOT_ELIGIBLE", "; ".join(reasons)

            return "ELIGIBLE", "All eligibility criteria satisfied"

        finally:
            if cursor:
                cursor.close()

            if db:
                db.close()
    def add_application(self, application, changed_by):
        db = None
        cursor = None

        try:
            db = create_connection()
            if db is None:
                return None

            cursor = db.cursor()

            cursor.execute("""
                SELECT application_id
                FROM applications
                WHERE candidate_id = %s AND job_id = %s
            """, (application.candidate_id, application.job_id))

            if cursor.fetchone():
                return "DUPLICATE"

            cursor.execute("""
                INSERT INTO applications
                (
                    application_code, candidate_id, job_id,
                    eligibility_status, eligibility_reason,
                    application_status, source,
                    assigned_recruiter_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                application.application_code,
                application.candidate_id,
                application.job_id,
                application.eligibility_status,
                application.eligibility_reason,
                application.application_status,
                application.source,
                application.assigned_recruiter_id
            ))

            application_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO application_history
                (
                    application_id, old_status, new_status,
                    remarks, changed_by
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                application_id,
                None,
                "APPLIED",
                "Application created",
                changed_by
            ))

            db.commit()

            application.application_id = application_id
            return application_id

        except Exception:
            if db:
                db.rollback()
            raise

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    def view_applications(self):
        db = None
        cursor = None

        try:
            db = create_connection()
            if db is None:
                return []

            cursor = db.cursor()

            cursor.execute("""
                SELECT a.application_id, a.application_code,
                       c.full_name, j.job_title,
                       a.eligibility_status, a.application_status,
                       a.applied_at
                FROM applications a
                JOIN candidates c ON a.candidate_id = c.candidate_id
                JOIN jobs j ON a.job_id = j.job_id
                ORDER BY a.application_id
            """)

            return cursor.fetchall()

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def get_application_by_id(self, application_id):
        db = None
        cursor = None

        try:
            db = create_connection()
            if db is None:
                return None

            cursor = db.cursor()

            cursor.execute("""
                SELECT application_code, application_status
                FROM applications
                WHERE application_id = %s
            """, (application_id,))

            return cursor.fetchone()

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def update_application_status(
        self, application_id, new_status, changed_by
    ):
        db = None
        cursor = None

        try:
            db = create_connection()

            if db is None:
                return False

            cursor = db.cursor()

            cursor.execute("""
                SELECT application_status
                FROM applications
                WHERE application_id = %s
                FOR UPDATE
            """, (application_id,))

            row = cursor.fetchone()

            if row is None:
                return False

            old_status = row[0]

            if old_status == new_status:
                return False

            cursor.execute("""
                UPDATE applications
                SET application_status = %s
                WHERE application_id = %s
            """, (new_status, application_id))

            if cursor.rowcount == 0:
                db.rollback()
                return False

            cursor.execute("""
                INSERT INTO application_history
                (
                    application_id, old_status, new_status,
                    remarks, changed_by
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                application_id,
                old_status,
                new_status,
                "Application status updated",
                changed_by
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

    def update_eligibility_result(
        self, application_id, eligibility_status, eligibility_reason=None
    ):
        db = None
        cursor = None

        if eligibility_status not in (
            "PENDING", "ELIGIBLE", "NOT_ELIGIBLE"
        ):
            raise ValueError("Invalid eligibility status.")

        try:
            db = create_connection()

            if db is None:
                return False

            cursor = db.cursor()

            # Confirm application exists
            cursor.execute("""
                SELECT application_id
                FROM applications
                WHERE application_id = %s
            """, (application_id,))

            if cursor.fetchone() is None:
                return False

            cursor.execute("""
                UPDATE applications
                SET eligibility_status = %s,
                    eligibility_reason = %s
                WHERE application_id = %s
            """, (
                eligibility_status,
                eligibility_reason,
                application_id
            ))

            db.commit()

            # Success even when the result has not changed
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

    def get_application_eligibility_details(self, application_id):
        db = None
        cursor = None

        try:
            db = create_connection()

            if db is None:
                return None

            cursor = db.cursor()

            cursor.execute("""
                SELECT candidate_id, job_id
                FROM applications
                WHERE application_id = %s
            """, (application_id,))

            return cursor.fetchone()

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def withdraw_application(self, application_id, changed_by):
        db = None
        cursor = None

        try:
            db = create_connection()

            if db is None:
                return False

            cursor = db.cursor()

            cursor.execute("""
                SELECT application_status
                FROM applications
                WHERE application_id = %s
                FOR UPDATE
            """, (application_id,))

            row = cursor.fetchone()

            if row is None:
                return False

            old_status = row[0]

            if old_status == "WITHDRAWN":
                return "ALREADY_WITHDRAWN"

            allowed_statuses = (
                "APPLIED",
                "ELIGIBILITY_VERIFIED",
                "SHORTLISTED",
                "INTERVIEW_SCHEDULED",
                "INTERVIEWED",
                "SELECTED"
            )

            if old_status not in allowed_statuses:
                return "INVALID_STATUS"

            # Do not withdraw an application with a linked offer
            cursor.execute("""
                SELECT offer_id
                FROM offers
                WHERE application_id = %s
                LIMIT 1
            """, (application_id,))

            if cursor.fetchone():
                return "HAS_OFFER"

            cursor.execute("""
                UPDATE applications
                SET application_status = 'WITHDRAWN'
                WHERE application_id = %s
            """, (application_id,))

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
                old_status,
                "WITHDRAWN",
                "Application withdrawn",
                changed_by
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
    def delete_application(self, application_id):
        db = None
        cursor = None

        try:
            db = create_connection()

            if db is None:
                return False

            cursor = db.cursor()

            cursor.execute("""
                SELECT offer_id
                FROM offers
                WHERE application_id = %s
                LIMIT 1
            """, (application_id,))

            if cursor.fetchone():
                return "HAS_OFFER"

            cursor.execute("""
                SELECT interview_id
                FROM interview_rounds
                WHERE application_id = %s
                LIMIT 1
            """, (application_id,))

            if cursor.fetchone():
                return "HAS_INTERVIEW"

            cursor.execute("""
                SELECT history_id
                FROM application_history
                WHERE application_id = %s
                LIMIT 1
            """, (application_id,))

            if cursor.fetchone():
                return "HAS_HISTORY"

            cursor.execute("""
                DELETE FROM applications
                WHERE application_id = %s
            """, (application_id,))

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