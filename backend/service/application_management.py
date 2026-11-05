from model.application import Application
from dao.application_dao import ApplicationDAO
from util.activity_logger import log_activity
from exception.custom_exceptions import (
    DuplicateApplicationError,
    CandidateNotEligibleError
)


application_dao = ApplicationDAO()


def check_eligibility(candidate_id, job_id):
    try:
        return application_dao.check_eligibility(
            candidate_id, job_id
        )
    except Exception as error:
        print("Eligibility Error:", error)
        return "PENDING", "Eligibility check failed"

def recheck_application_eligibility():
    try:
        application_id = int(input("Enter Application ID: "))

        record = application_dao.get_application_by_id(application_id)

        if not record:
            print("Application ID Not Found.")
            return

        details = application_dao.get_application_eligibility_details(
            application_id
        )

        if not details:
            print("Application Details Not Found.")
            return

        candidate_id, job_id = details

        eligibility_status, eligibility_reason = check_eligibility(
            candidate_id, job_id
        )

        # Do not save failed checks as eligibility results
        if eligibility_status == "PENDING":
            print("Eligibility Check Could Not Be Completed.")
            print("Reason:", eligibility_reason)
            return

        updated = application_dao.update_eligibility_result(
            application_id,
            eligibility_status,
            eligibility_reason
        )

        if updated:
            print("\nEligibility Rechecked Successfully!")
            print("Status:", eligibility_status)
            print("Reason:", eligibility_reason)

            log_activity(
                f"Application Eligibility Rechecked: "
                f"Application ID {application_id}, "
                f"Status {eligibility_status}"
            )
        else:
            print("Application ID Not Found.")

    except ValueError:
        print("Please enter a valid Application ID.")

    except Exception as error:
        print("Eligibility Recheck Failed:", error)

def add_application():
    try:
        candidate_id = int(input("Enter Candidate ID: "))
        job_id = int(input("Enter Job ID: "))

        application_code = input(
            "Enter Application Code: "
        ).strip()

        source = input("Enter Source (optional): ").strip() or None

        recruiter_input = input(
            "Enter Recruiter ID (optional): "
        ).strip()

        recruiter_id = int(recruiter_input) if recruiter_input else None

        changed_by = int(input("Enter Your User ID: "))

        if not application_code:
            print("Application Code is required.")
            return

        eligibility_status, eligibility_reason = check_eligibility(
            candidate_id, job_id
        )

        if eligibility_status != "ELIGIBLE":
            raise CandidateNotEligibleError(
                f"Application Cannot Be Added! "
                f"Status: {eligibility_status}. "
                f"Reason: {eligibility_reason}"
            )

        application = Application(
            application_code=application_code,
            candidate_id=candidate_id,
            job_id=job_id,
            eligibility_status=eligibility_status,
            eligibility_reason=eligibility_reason,
            application_status="APPLIED",
            source=source,
            assigned_recruiter_id=recruiter_id
        )

        result = application_dao.add_application(
            application, changed_by
        )

        if result == "DUPLICATE":
            raise DuplicateApplicationError(
                "This candidate has already applied for this job."
            )

        if result is None:
            print("Database connection failed.")
            return

        print("\nApplication Added Successfully!")
        print("Application ID:", result)
        print("Eligibility:", eligibility_status)
        print("Reason:", eligibility_reason)
        print("Application Status: APPLIED")
        print("Application History Saved Successfully!")

        log_activity(
            f"Application Created: {application_code} (ID: {result})"
        )

    except ValueError:
        print("Please enter valid numeric IDs.")
    except DuplicateApplicationError as error:
        print("Custom Exception:", error)
    except CandidateNotEligibleError as error:
        print("Custom Exception:", error)
    except Exception as error:
        print("Application Add Failed:", error)

def view_applications():
    try:
        records = application_dao.view_applications()

        print("\n===== APPLICATION LIST =====")

        if not records:
            print("No Applications Found.")
            return

        for row in records:
            print("\nApplication ID:", row[0])
            print("Application Code:", row[1])
            print("Candidate:", row[2])
            print("Job:", row[3])
            print("Eligibility:", row[4])
            print("Status:", row[5])
            print("Applied At:", row[6])

    except Exception as error:
        print("View Applications Failed:", error)


def update_application():
    allowed_transitions = {
        "APPLIED": [
            "ELIGIBILITY_VERIFIED",
            "SHORTLISTED",
            "REJECTED",
            "WITHDRAWN"
        ],
        "ELIGIBILITY_VERIFIED": [
            "SHORTLISTED",
            "REJECTED",
            "WITHDRAWN"
        ],
        "SHORTLISTED": [
            "INTERVIEW_SCHEDULED",
            "REJECTED",
            "WITHDRAWN"
        ],
        "INTERVIEW_SCHEDULED": [
            "INTERVIEWED",
            "REJECTED",
            "WITHDRAWN"
        ],
        "INTERVIEWED": [
            "SELECTED",
            "REJECTED",
            "WITHDRAWN"
        ],
        "SELECTED": [
            "REJECTED",
            "WITHDRAWN"
        ]
    }

    try:
        application_id = int(input("Enter Application ID: "))

        record = application_dao.get_application_by_id(application_id)

        if not record:
            print("Application ID Not Found.")
            return

        application_code, current_status = record

        print("\nCurrent Status:", current_status)

        if current_status not in allowed_transitions:
            print("This status is managed by another module.")
            return

        available = allowed_transitions[current_status]

        print("\nAvailable Next Statuses:")

        for index, status in enumerate(available, start=1):
            print(f"{index}. {status}")

        choice = input("Select New Status: ").strip()

        if not choice.isdigit() or not 1 <= int(choice) <= len(available):
            print("Invalid Status Choice.")
            return

        new_status = available[int(choice) - 1]

        changed_by = int(input("Enter Your User ID: "))

        updated = application_dao.update_application_status(
            application_id,
            new_status,
            changed_by
        )

        if updated:
            log_activity(
                f"Application Status Updated: {application_code} "
                f"({current_status} -> {new_status}) "
                f"(ID: {application_id})"
            )

            print("Application Status Updated Successfully!")
            print("Application History Saved Successfully!")

        else:
            print("Application Status Update Failed.")

    except ValueError:
        print("Please enter valid numeric IDs.")

    except Exception as error:
        print("Update Failed:", error)
def delete_application():
    try:
        application_id = int(input("Enter Application ID: "))

        record = application_dao.get_application_by_id(application_id)

        if not record:
            print("Application ID Not Found.")
            return

        application_code, current_status = record

        if current_status == "WITHDRAWN":
            print("This application is already withdrawn.")
            return

        confirm = input(
            "Are you sure you want to withdraw this application? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Withdrawal Cancelled.")
            return

        changed_by = int(input("Enter Your User ID: "))

        result = application_dao.withdraw_application(
            application_id,
            changed_by
        )

        if result == "HAS_OFFER":
            print(
                "Cannot withdraw: An offer is linked to this application."
            )

        elif result == "ALREADY_WITHDRAWN":
            print("Application is already withdrawn.")

        elif result == "INVALID_STATUS":
            print("Application cannot be withdrawn in its current status.")

        elif result:
            print("\nApplication Withdrawn Successfully!")
            print("Application History Saved Successfully!")

            log_activity(
                f"Application Withdrawn: {application_code} "
                f"(ID: {application_id})"
            )

        else:
            print("Application Withdrawal Failed.")

    except ValueError:
        print("Please enter valid numeric IDs.")

    except Exception as error:
        print("Application Withdrawal Failed:", error)
def main_menu():
    while True:
        print("\n===== APPLICATION MANAGEMENT =====")
        print("1. Add Application")
        print("2. View Applications")
        print("3. Update Application Status")
        print("4. Withdraw Application")
        print("5. Recheck Application Eligibility")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_application()
        elif choice == "2":
            view_applications()
        elif choice == "3":
            update_application()
        elif choice == "4":
            delete_application()
        elif choice == "5":
            recheck_application_eligibility()
        elif choice == "0":
            break
        else:
            print("Invalid Choice! Please try again.")


if __name__ == "__main__":
    main_menu()