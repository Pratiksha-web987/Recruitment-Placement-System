from model.interview import Interview
from dao.interview_dao import InterviewDAO
from util.activity_logger import log_activity
from service import interview_feedback_management


interview_dao = InterviewDAO()


# ==========================================
# ADD INTERVIEW
# ==========================================
def add_interview():

    try:
        application_id = int(input("Enter Application ID: "))
        round_number = int(input("Enter Round Number: "))

        round_type = input(
            "Enter Round Type (TECHNICAL/HR/APTITUDE): "
        ).strip().upper()

        scheduled_date = input(
            "Enter Scheduled Date (YYYY-MM-DD): "
        ).strip()

        scheduled_time = input(
            "Enter Scheduled Time (HH:MM:SS): "
        ).strip()

        mode = input(
            "Enter Mode (ONLINE/OFFLINE/TELEPHONIC): "
        ).strip().upper()

        if mode not in ("ONLINE", "OFFLINE", "TELEPHONIC"):
            print("Invalid interview mode.")
            return

        interviewer_name = input(
            "Enter Interviewer Name: "
        ).strip()

        meeting_or_location = input(
            "Enter Meeting Link or Location: "
        ).strip()

        changed_by = int(input("Enter Your User ID: "))

        interview = Interview(
            application_id=application_id,
            round_number=round_number,
            round_type=round_type,
            scheduled_date=scheduled_date,
            scheduled_time=scheduled_time,
            mode=mode,
            interviewer_name=interviewer_name or None,
            meeting_or_location=meeting_or_location or None
        )

        result = interview_dao.add_interview(
            interview, changed_by
        )

        if result == "NOT_FOUND":
            print("Application ID Not Found.")

        elif result == "NOT_ELIGIBLE":
            print("Application is not eligible for interview scheduling.")

        elif result is None:
            print("Database connection failed.")

        else:
            log_activity(
                f"Interview Scheduled: Interview ID {result}, "
                f"Application ID {application_id}, "
                f"Round {round_number} ({round_type})"
            )

            print("\nInterview Scheduled Successfully!")
            print("Interview ID:", result)
            print("Application Status: INTERVIEW_SCHEDULED")

    except ValueError:
        print("Please enter valid numeric values.")

    except Exception as error:
        print("Interview Scheduling Failed:", error)


# ==========================================
# VIEW INTERVIEWS
# ==========================================

def view_interviews():

    try:
        records = interview_dao.view_interviews()

        print("\n===== INTERVIEW LIST =====")

        if not records:
            print("No Interviews Found.")
            return

        for row in records:
            print("\nInterview ID:", row[0])
            print("Application ID:", row[1])
            print("Candidate:", row[2])
            print("Job:", row[3])
            print("Round:", row[4], row[5])
            print("Date:", row[6])
            print("Time:", row[7])
            print("Mode:", row[8])
            print("Interviewer:", row[9])
            print("Status:", row[10])

    except Exception as error:
        print("View Interviews Failed:", error)


# ==========================================
# UPDATE INTERVIEW
# ==========================================

def update_interview():

    statuses = {
        "1": "SCHEDULED",
        "2": "COMPLETED",
        "3": "CANCELLED",
        "4": "RESCHEDULED"
    }

    try:
        interview_id = int(input("Enter Interview ID: "))

        interview = interview_dao.get_interview_by_id(interview_id)

        if not interview:
            print("Interview ID Not Found.")
            return

        application_id = interview[0]
        current_status = interview[1]

        print("\nCurrent Interview Status:", current_status)
        print("\n1. SCHEDULED")
        print("2. COMPLETED")
        print("3. CANCELLED")
        print("4. RESCHEDULED")

        choice = input("\nSelect New Status: ").strip()

        if choice not in statuses:
            print("Invalid Status Choice.")
            return

        new_status = statuses[choice]

        changed_by = None

        if new_status == "COMPLETED":
            changed_by = int(
                input("Enter Your User ID (for application history): ")
            )

        result = interview_dao.update_interview_status(
            interview_id,
            application_id,
            new_status,
            changed_by
        )

        if not result:
            print("Interview Status Update Failed.")
            return

        if result["application_updated"]:
            log_activity(
                f"Application Status Updated: Application ID "
                f"{application_id} "
                f"(INTERVIEW_SCHEDULED -> INTERVIEWED)"
            )
            print("Application Status Updated: INTERVIEWED")
            print("Application History Saved Successfully.")

        log_activity(
            f"Interview Updated: Interview ID {interview_id}, "
            f"Application ID {application_id}, "
            f"({current_status} -> {new_status})"
        )

        print("\nInterview Updated Successfully!")
        print("Previous Status:", current_status)
        print("New Status:", new_status)

    except ValueError as error:
        print("Please enter valid values:", error)

    except Exception as error:
        print("Update Failed:", error)
# ==========================================
# DELETE INTERVIEW
# ==========================================

def delete_interview():

    try:
        interview_id = int(input("Enter Interview ID: "))

        interview = interview_dao.get_interview_by_id(interview_id)

        if not interview:
            print("Interview ID Not Found.")
            return

        application_id = interview[0]

        confirm = input(
            "Are you sure? (yes/no): "
        ).strip().lower()

        if confirm == "yes":

            result = interview_dao.delete_interview(interview_id)

            if result == "HAS_FEEDBACK":
                print(
                    "Cannot Delete Interview! Feedback is linked "
                    "to this Interview. Feedback records are preserved."
                )

            elif result:
                log_activity(
                    f"Interview Deleted: Interview ID {interview_id}, "
                    f"Application ID {application_id}"
                )
                print("Interview Deleted Successfully!")

            else:
                print("Interview ID Not Found.")

        else:
            print("Delete Cancelled.")

    except ValueError:
        print("Please enter a valid Interview ID.")

    except Exception as error:
        print("Delete Failed:", error)

# ==========================================
# INTERVIEW MANAGEMENT MENU
# ==========================================

def main_menu():

    while True:

        print("\n===== INTERVIEW MANAGEMENT =====")
        print("1. Add Interview")
        print("2. View Interviews")
        print("3. Update Interview")
        print("4. Delete Interview")
        print("5. Add Interview Feedback")
        print("6. View Interview Feedback")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_interview()

        elif choice == "2":
            view_interviews()

        elif choice == "3":
            update_interview()

        elif choice == "4":
            delete_interview()

        elif choice == "5":
            interview_feedback_management.add_feedback()

        elif choice == "6":
            interview_feedback_management.view_feedback()

        elif choice == "0":
            break

        else:
            print("Invalid Choice! Please try again.")


if __name__ == "__main__":
    main_menu()