from datetime import datetime

from model.job import Job
from dao.job_dao import JobDAO
from exception.custom_exceptions import JobNotFoundError
from util.activity_logger import log_activity


job_dao = JobDAO()


def valid_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False


def validate_job(job):
    if job.company_id <= 0 or job.created_by <= 0:
        return "Company ID and User ID must be positive."

    if not job.job_code or not job.job_title or not job.location:
        return "Job Code, Job Title and Location are required."

    if job.employment_type not in (
        "FULL_TIME", "PART_TIME", "INTERNSHIP"
    ):
        return "Invalid Employment Type."

    if job.openings <= 0:
        return "Number of openings must be greater than zero."

    if job.min_package_lpa < 0 or job.max_package_lpa < 0:
        return "Package cannot be negative."

    if (
        job.min_package_lpa > 0
        and job.max_package_lpa > 0
        and job.max_package_lpa < job.min_package_lpa
    ):
        return "Maximum package cannot be less than minimum package."

    if not 0 <= job.min_percentage <= 100:
        return "Minimum percentage must be between 0 and 100."

    if job.min_passing_year < 0 or job.max_passing_year < 0:
        return "Passing year cannot be negative."

    if (
        job.min_passing_year > 0
        and job.max_passing_year > 0
        and job.max_passing_year < job.min_passing_year
    ):
        return "Maximum passing year cannot be less than minimum year."

    if job.max_backlogs < 0:
        return "Maximum backlogs cannot be negative."

    if job.experience_min_years < 0:
        return "Experience cannot be negative."

    if not valid_date(job.posted_date):
        return "Invalid Posted Date. Use YYYY-MM-DD."

    if not valid_date(job.application_deadline):
        return "Invalid Application Deadline. Use YYYY-MM-DD."

    if job.application_deadline < job.posted_date:
        return "Application deadline cannot be before posted date."

    return None


# ==========================================
# ADD JOB
# ==========================================

def add_job():
    print("\n===== ADD NEW JOB =====")

    try:
        job = Job(
            company_id=int(input("Enter Company ID: ")),
            job_code=input("Enter Job Code: ").strip(),
            job_title=input("Enter Job Title: ").strip(),
            employment_type=input(
                "Employment Type (FULL_TIME/PART_TIME/INTERNSHIP): "
            ).strip().upper(),
            location=input("Enter Location: ").strip(),
            openings=int(input("Enter Number of Openings: ")),
            min_package_lpa=float(
                input("Enter Minimum Package (LPA): ") or 0
            ),
            max_package_lpa=float(
                input("Enter Maximum Package (LPA): ") or 0
            ),
            min_percentage=float(
                input("Enter Minimum Percentage: ") or 0
            ),
            min_passing_year=int(
                input("Enter Minimum Passing Year (or 0): ") or 0
            ),
            max_passing_year=int(
                input("Enter Maximum Passing Year (or 0): ") or 0
            ),
            max_backlogs=int(input("Enter Maximum Backlogs: ")),
            experience_min_years=float(
                input("Enter Minimum Experience: ") or 0
            ),
            qualification_rule=input(
                "Enter Qualification Rule: "
            ).strip(),
            posted_date=input(
                "Enter Posted Date (YYYY-MM-DD): "
            ).strip(),
            application_deadline=input(
                "Enter Application Deadline (YYYY-MM-DD): "
            ).strip(),
            created_by=int(input("Enter Created By User ID: "))
        )

        error = validate_job(job)

        if error:
            print(error)
            return

        job_id = job_dao.add_job(job)

        if job_id is None:
            print("Database connection failed.")
            return

        print("Job Added Successfully!")
        print("Job ID:", job_id)

        log_activity(
            f"Job Created: {job.job_title} (ID: {job_id})"
        )

    except ValueError:
        print("Please Enter Valid Numeric Values!")

    except Exception as error:
        print("Error:", error)


# ==========================================
# VIEW JOBS
# ==========================================

def view_jobs():
    print("\n========== JOB LIST ==========")

    try:
        jobs = job_dao.view_jobs()

        if not jobs:
            print("No Jobs Found!")
            return

        for job in jobs:
            print("--------------------------------")
            print("Job ID:", job.job_id)
            print("Job Code:", job.job_code)
            print("Job Title:", job.job_title)
            print("Company ID:", job.company_id)
            print("Employment Type:", job.employment_type)
            print("Location:", job.location)
            print("Openings:", job.openings)
            print("Minimum Package:", job.min_package_lpa)
            print("Maximum Package:", job.max_package_lpa)
            print("Minimum Percentage:", job.min_percentage)
            print("Passing Year:", job.min_passing_year, "-", job.max_passing_year)
            print("Maximum Backlogs:", job.max_backlogs)
            print("Minimum Experience:", job.experience_min_years)
            print("Posted Date:", job.posted_date)
            print("Deadline:", job.application_deadline)
            print("Status:", job.status)

    except Exception as error:
        print("Error:", error)


# ==========================================
# UPDATE JOB
# ==========================================

def update_job():
    print("\n===== UPDATE JOB =====")

    try:
        job_id = int(input("Enter Job ID to Update: "))

        if job_id <= 0:
            print("Job ID must be positive.")
            return

        old_job = job_dao.get_job_by_id(job_id)

        if old_job is None:
            raise JobNotFoundError(f"Job ID {job_id} not found.")

        print("Current Job Title:", old_job.job_title)

        old_title = old_job.job_title

        old_job.job_title = input(
            "Enter New Job Title: "
        ).strip()

        old_job.location = input(
            "Enter New Location: "
        ).strip()

        old_job.openings = int(
            input("Enter New Openings: ")
        )

        old_job.min_package_lpa = float(
            input("Enter New Minimum Package: ") or 0
        )

        old_job.max_package_lpa = float(
            input("Enter New Maximum Package: ") or 0
        )

        old_job.application_deadline = input(
            "Enter New Deadline (YYYY-MM-DD): "
        ).strip()

        if not old_job.job_title or not old_job.location:
            print("Job Title and Location cannot be empty.")
            return

        if old_job.openings <= 0:
            print("Openings must be greater than zero.")
            return

        if (
            old_job.min_package_lpa < 0
            or old_job.max_package_lpa < 0
        ):
            print("Package cannot be negative.")
            return

        if (
            old_job.min_package_lpa > 0
            and old_job.max_package_lpa > 0
            and old_job.max_package_lpa < old_job.min_package_lpa
        ):
            print("Maximum package cannot be less than minimum package.")
            return

        if not valid_date(old_job.application_deadline):
            print("Invalid Deadline. Use YYYY-MM-DD.")
            return

        if (
            valid_date(str(old_job.posted_date))
            and old_job.application_deadline < str(old_job.posted_date)
        ):
            print("Deadline cannot be before posted date.")
            return

        if job_dao.update_job(old_job):
            print("Job Updated Successfully!")

            log_activity(
                f"Job Updated: {old_title} -> "
                f"{old_job.job_title} (ID: {job_id})"
            )
        else:
            print("Job could not be updated.")

    except ValueError:
        print("Please Enter Valid Numeric Values!")

    except JobNotFoundError as error:
        print("Custom Exception:", error)

    except Exception as error:
        print("Error:", error)

def update_job_status():
    print("\n===== UPDATE JOB STATUS =====")

    try:
        job_id = int(input("Enter Job ID: "))

        print("\nValid Statuses:")
        print("1. DRAFT")
        print("2. OPEN")
        print("3. CLOSED")
        print("4. CANCELLED")

        status_choice = input("Choose Status: ").strip()

        status_map = {
            "1": "DRAFT",
            "2": "OPEN",
            "3": "CLOSED",
            "4": "CANCELLED"
        }

        if status_choice not in status_map:
            print("Invalid Status Choice!")
            return

        status = status_map[status_choice]

        updated = job_dao.update_job_status(job_id, status)

        if updated:
            print("Job Status Updated Successfully!")

            log_activity(
                f"Job Status Updated: Job ID {job_id}, Status {status}"
            )
        else:
            print("Job ID not found.")

    except ValueError:
        print("Please enter a valid Job ID.")

    except Exception as error:
        print("Job Status Update Failed:", error)


# ==========================================
# DELETE JOB
# ==========================================

def delete_job():
    print("\n===== DELETE JOB =====")

    try:
        job_id = int(input("Enter Job ID to Delete: "))

        if job_id <= 0:
            print("Job ID must be positive.")
            return

        job = job_dao.get_job_by_id(job_id)

        if job is None:
            raise JobNotFoundError(f"Job ID {job_id} not found.")

        print("Job Title:", job.job_title)

        confirm = input(
            "Are you sure? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Delete Cancelled!")
            return

        result = job_dao.delete_job(job_id)

        if result == "LINKED":
            print(
                "Cannot Delete Job! Applications, Placements or "
                "Job Skills are linked to this Job."
            )

        elif result:
            print("Job Deleted Successfully!")

            log_activity(
                f"Job Deleted: {job.job_title} (ID: {job_id})"
            )

        else:
            print("Job could not be deleted.")

    except ValueError:
        print("Please Enter a Valid Job ID!")

    except JobNotFoundError as error:
        print("Custom Exception:", error)

    except Exception as error:
        print("Error:", error)


# ==========================================
# JOB MANAGEMENT MAIN MENU
# ==========================================

def main_menu():

    while True:
        print("\n===== RPMS JOB MANAGEMENT =====")
        print("1. Add Job")
        print("2. View Jobs")
        print("3. Update Job")
        print("4. Delete Job")
        print("5. Update Job Status")
        print("0. Back to Main Menu")

        choice = input("Enter Your Choice: ").strip()

        if choice == "1":
            add_job()

        elif choice == "2":
            view_jobs()

        elif choice == "3":
            update_job()

        elif choice == "4":
            delete_job()

        elif choice == "5":
          update_job_status()

        elif choice == "0":
            break

        else:
            print("Invalid Choice!")


if __name__ == "__main__":
    main_menu()