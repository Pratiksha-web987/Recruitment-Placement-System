from util.db_connection import create_connection


class SkillDAO:

    def add_skill(self, skill):
        connection = create_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO skills (skill_name, category)
                VALUES (%s, %s)
                """,
                (skill.skill_name, skill.category)
            )
            connection.commit()
            return True

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def view_skills(self):
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT skill_id, skill_name, category, is_active
                FROM skills
                ORDER BY skill_id ASC
            """)
            return cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

    def update_skill(self, skill_id, skill_name, category):
        connection = create_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                UPDATE skills
                SET skill_name = %s, category = %s
                WHERE skill_id = %s
            """, (skill_name, category, skill_id))

            connection.commit()
            return cursor.rowcount > 0

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def deactivate_skill(self, skill_id):
        connection = create_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                UPDATE skills
                SET is_active = 0
                WHERE skill_id = %s
            """, (skill_id,))

            connection.commit()
            return cursor.rowcount > 0

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def activate_skill(self, skill_id):
        connection = create_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                UPDATE skills
                SET is_active = 1
                WHERE skill_id = %s
            """, (skill_id,))

            connection.commit()
            return cursor.rowcount > 0

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def add_candidate_skill(
        self, candidate_id, skill_id, proficiency_level,
        years_experience, is_primary
    ):
        connection = create_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO candidate_skills
                (candidate_id, skill_id, proficiency_level,
                 years_experience, is_primary)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                candidate_id, skill_id, proficiency_level,
                years_experience, is_primary
            ))

            connection.commit()
            return True

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def view_candidate_skills(self, candidate_id):
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT cs.candidate_skill_id, cs.candidate_id,
                       s.skill_id, s.skill_name,
                       cs.proficiency_level, cs.years_experience,
                       cs.is_primary
                FROM candidate_skills cs
                JOIN skills s ON cs.skill_id = s.skill_id
                WHERE cs.candidate_id = %s
                ORDER BY cs.is_primary DESC, s.skill_id ASC
            """, (candidate_id,))

            return cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

    def remove_candidate_skill(self, candidate_skill_id):
        connection = create_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                DELETE FROM candidate_skills
                WHERE candidate_skill_id = %s
            """, (candidate_skill_id,))

            connection.commit()
            return cursor.rowcount > 0

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def add_job_skill(
        self, job_id, skill_id, minimum_level, mandatory_flag
    ):
        connection = create_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO job_skills
                (job_id, skill_id, minimum_level, mandatory_flag)
                VALUES (%s, %s, %s, %s)
            """, (job_id, skill_id, minimum_level, mandatory_flag))

            connection.commit()
            return True

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def view_job_skills(self, job_id):
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT js.job_skill_id, js.job_id,
                       s.skill_id, s.skill_name,
                       js.minimum_level, js.mandatory_flag
                FROM job_skills js
                JOIN skills s ON js.skill_id = s.skill_id
                WHERE js.job_id = %s
                ORDER BY js.mandatory_flag DESC, s.skill_id ASC
            """, (job_id,))

            return cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

    def remove_job_skill(self, job_skill_id):
        connection = create_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                DELETE FROM job_skills
                WHERE job_skill_id = %s
            """, (job_skill_id,))

            connection.commit()
            return cursor.rowcount > 0

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()