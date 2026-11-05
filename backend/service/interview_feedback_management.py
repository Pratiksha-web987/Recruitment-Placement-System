from dao.interview_feedback_dao import InterviewFeedbackDAO
from util.activity_logger import log_activity


feedback_dao = InterviewFeedbackDAO()


def add_feedback():

    try:
        print("\n========== ADD INTERVIEW FEEDBACK ==========")

        interview_id = int(input("Enter Interview ID: "))

        technical = float(input("Technical Rating (0-5): "))
        communication = float(input("Communication Rating (0-5): "))
        problem_solving = float(input("Problem Solving Rating (0-5): "))
        overall = float(input("Overall Rating (0-5): "))

        recommendation = input(
            "Enter Recommendation: "
        ).strip().upper()

        remarks = input("Enter Remarks (Optional): ").strip()

        submitted_by = int(input("Enter Submitted By User ID: "))

        ratings = [technical, communication, problem_solving, overall]

        if any(
            not (0 <= rating <= 5)
            for rating in ratings
        ):
            print("Ratings must be between 0 and 5.")
            return

        if not recommendation:
            print("Recommendation cannot be empty.")
            return

        if len(recommendation) > 30:
            print("Recommendation cannot exceed 30 characters.")
            return

        if interview_id <= 0 or submitted_by <= 0:
            print("Interview ID and User ID must be positive.")
            return

        result = feedback_dao.add_feedback(
            interview_id,
            technical,
            communication,
            problem_solving,
            overall,
            recommendation,
            remarks or None,
            submitted_by
        )

        if result == "INTERVIEW_NOT_FOUND":
            print("Interview ID Not Found.")

        elif result == "FEEDBACK_EXISTS":
            print("Feedback already exists for this interview.")

        elif result is None:
            print("Database connection failed.")

        else:
            log_activity(
                f"Interview Feedback Added: Feedback ID {result}, "
                f"Interview ID {interview_id}"
            )
            print("Feedback Added Successfully!")
            print("Feedback ID:", result)

    except ValueError:
        print("Please enter valid numeric values.")

    except Exception as error:
        print("Feedback Add Failed:", error)

def view_feedback():

    try:
        records = feedback_dao.view_feedback()

        print("\n========== INTERVIEW FEEDBACK ==========")

        if not records:
            print("No Feedback Found.")
            return

        for row in records:
            print("\nFeedback ID:", row[0])
            print("Interview ID:", row[1])
            print("Candidate:", row[2])
            print("Technical Rating:", row[3])
            print("Communication Rating:", row[4])
            print("Problem Solving Rating:", row[5])
            print("Overall Rating:", row[6])
            print("Recommendation:", row[7])
            print("Remarks:", row[8])
            print("Submitted By:", row[9])
            print("Submitted At:", row[10])
            print("-" * 40)

    except Exception as error:
        print("Feedback View Failed:", error)