import re

from model.candidate import Candidate
from dao.candidate_dao import CandidateDAO
from exception.custom_exceptions import CandidateNotFoundError
from util.activity_logger import log_activity


candidate_dao = CandidateDAO()


def validate_candidate(candidate):
    if not candidate.candidate_code:
        print("Candidate Code is required.")
        return False

    if not candidate.full_name:
        print("Candidate Name is required.")
        return False

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", candidate.email):
        print("Please enter a valid email address.")
        return False

    if not re.fullmatch(r"[6-9]\d{9}", candidate.mobile):
        print("Mobile number must contain 10 digits and start with 6-9.")
        return False

    if not candidate.qualification:
        print("Qualification is required.")
        return False

    if candidate.passing_year <= 0:
        print("Please enter a valid passing year.")
        return False

    if not 0 <= candidate.percentage <= 100:
        print("Percentage must be between 0 and 100.")
        return False

    if candidate.backlog_count < 0:
        print("Backlog count cannot be negative.")
        return False

    if not candidate.primary_technology:
        print("Primary Technology is required.")
        return False

    return True


def add_candidate():
    print("\n===== ADD NEW CANDIDATE =====")

    try:
        candidate = Candidate(
            candidate_code=input("Enter Candidate Code: ").strip(),
            full_name=input("Enter Full Name: ").strip(),
            email=input("Enter Email: ").strip().lower(),
            mobile=input("Enter Mobile: ").strip(),
            qualification=input("Enter Qualification: ").strip(),
            passing_year=int(input("Enter Passing Year: ")),
            percentage=float(input("Enter Percentage: ")),
            backlog_count=int(input("Enter Backlog Count: ")),
            primary_technology=input("Enter Primary Technology: ").strip()
        )

        if not validate_candidate(candidate):
            return

        if candidate_dao.find_by_email(candidate.email):
            print("This email is already registered.")
            return

        if candidate_dao.find_by_mobile(candidate.mobile):
            print("This mobile number is already registered.")
            return

        candidate_id = candidate_dao.add_candidate(candidate)

        if candidate_id is None:
            print("Database connection failed.")
            return

        print("\nCandidate Added Successfully!")
        print("Candidate ID:", candidate_id)

        log_activity(
            f"Candidate Created: {candidate.full_name} (ID: {candidate_id})"
        )

    except ValueError:
        print("Please enter valid numeric values.")

    except Exception as error:
        print("Candidate Add Failed:", error)


def display_candidate(candidate):
    print("\n----------------------------")
    print("ID:", candidate.candidate_id)
    print("Code:", candidate.candidate_code)
    print("Name:", candidate.full_name)
    print("Email:", candidate.email)
    print("Mobile:", candidate.mobile)
    print("Qualification:", candidate.qualification)
    print("Passing Year:", candidate.passing_year)
    print("Percentage:", candidate.percentage)
    print("Backlog Count:", candidate.backlog_count)
    print("Primary Technology:", candidate.primary_technology)
    print("Profile Status:", candidate.profile_status)
    print("Placement Status:", candidate.placement_status)


def view_candidates():
    print("\n===== ALL CANDIDATES =====")

    try:
        candidates = candidate_dao.view_candidates()

        if not candidates:
            print("No Candidates Found.")
            return

        for candidate in candidates:
            display_candidate(candidate)

    except Exception as error:
        print("Candidate View Failed:", error)


def search_candidate():
    print("\n===== SEARCH CANDIDATE =====")
    print("1. Search by Candidate ID")
    print("2. Search by Email")
    print("3. Search by Mobile")
    print("4. Search by Technology")

    choice = input("Enter your choice: ").strip()

    try:
        if choice == "1":
            candidate = candidate_dao.get_candidate_by_id(
                int(input("Enter Candidate ID: "))
            )

            if candidate:
                display_candidate(candidate)
            else:
                print("Candidate Not Found.")

        elif choice == "2":
            email = input("Enter Email: ").strip().lower()
            candidate = candidate_dao.find_by_email(email)

            if candidate:
                display_candidate(candidate)
            else:
                print("Candidate Not Found.")

        elif choice == "3":
            mobile = input("Enter Mobile: ").strip()
            candidate = candidate_dao.find_by_mobile(mobile)

            if candidate:
                display_candidate(candidate)
            else:
                print("Candidate Not Found.")

        elif choice == "4":
            technology = input("Enter Technology: ").strip()
            candidates = candidate_dao.find_by_technology(technology)

            if candidates:
                for candidate in candidates:
                    display_candidate(candidate)
            else:
                print("No Candidates Found for this Technology.")

        else:
            print("Invalid Choice.")

    except ValueError:
        print("Please enter a valid Candidate ID.")

    except Exception as error:
        print("Candidate Search Failed:", error)


def update_candidate():
    print("\n===== UPDATE CANDIDATE PROFILE =====")

    try:
        candidate_id = int(input("Enter Candidate ID: "))

        candidate = candidate_dao.get_candidate_by_id(candidate_id)

        if candidate is None:
            raise CandidateNotFoundError(
                f"Candidate ID {candidate_id} not found."
            )

        print("Candidate Name:", candidate.full_name)

        mobile = input("New Mobile Number: ").strip()

        if not re.fullmatch(r"[6-9]\d{9}", mobile):
            print("Mobile must be a valid 10-digit number.")
            return

        existing = candidate_dao.find_by_mobile(mobile)

        if existing and existing.candidate_id != candidate_id:
            print("Mobile number already registered.")
            return

        date_of_birth = input(
            "Date of Birth (YYYY-MM-DD, blank if unknown): "
        ).strip() or None

        if date_of_birth:
            from datetime import datetime
            try:
                datetime.strptime(date_of_birth, "%Y-%m-%d")
            except ValueError:
                print("Invalid date. Use YYYY-MM-DD.")
                return

        gender = input("Gender (Male/Female/Other, optional): ").strip() or None
        college = input("College (optional): ").strip() or None
        university = input("University (optional): ").strip() or None

        passing_year = int(input("Passing Year: "))

        if passing_year <= 0 or passing_year > 9999:
            print("Invalid passing year.")
            return

        percentage_text = input(
            "Percentage (blank if unknown): "
        ).strip()

        percentage = (
            float(percentage_text) if percentage_text else None
        )

        if percentage is not None and not 0 <= percentage <= 100:
            print("Percentage must be between 0 and 100.")
            return

        cgpa_text = input("CGPA (blank if unknown): ").strip()
        cgpa = float(cgpa_text) if cgpa_text else None

        if cgpa is not None and not 0 <= cgpa <= 99.99:
            print("Invalid CGPA.")
            return

        backlog_count = int(input("Backlog Count: "))

        if backlog_count < 0:
            print("Backlog count cannot be negative.")
            return

        primary_technology = input(
            "Primary Technology (optional): "
        ).strip() or None

        current_location = input(
            "Current Location (optional): "
        ).strip() or None

        preferred_location = input(
            "Preferred Location (optional): "
        ).strip() or None

        updated = candidate_dao.update_candidate_profile(
            candidate_id,
            mobile,
            date_of_birth,
            gender,
            college,
            university,
            passing_year,
            percentage,
            cgpa,
            backlog_count,
            primary_technology,
            current_location,
            preferred_location
        )

        if updated:
            print("Candidate Profile Updated Successfully!")

            log_activity(
                f"Candidate Profile Updated: "
                f"{candidate.full_name} (ID: {candidate_id})"
            )
        else:
            print("Candidate profile could not be updated.")

    except ValueError:
        print("Please enter valid numeric values.")

    except CandidateNotFoundError as error:
        print("Custom Exception:", error)

    except Exception as error:
        print("Candidate Update Failed:", error)
        
def delete_candidate():
    print("\n===== DELETE CANDIDATE =====")

    try:
        candidate_id = int(input("Enter Candidate ID to delete: "))
        candidate = candidate_dao.get_candidate_by_id(candidate_id)

        if candidate is None:
            raise CandidateNotFoundError(
                f"Candidate ID {candidate_id} not found."
            )

        print("Candidate Name:", candidate.full_name)

        confirm = input(
            "Are you sure you want to delete? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Delete Cancelled.")
            return

        result = candidate_dao.delete_candidate(candidate_id)

        if result == "LINKED":
            print(
                "Candidate cannot be deleted because related "
                "applications or other records exist."
            )

        elif result:
            print("Candidate Deleted Successfully!")
            log_activity(
                f"Candidate Deleted: {candidate.full_name} "
                f"(ID: {candidate_id})"
            )

        else:
            print("Candidate could not be deleted.")

    except ValueError:
        print("Please enter a valid Candidate ID.")

    except CandidateNotFoundError as error:
        print("Custom Exception:", error)

    except Exception as error:
        print("Candidate Delete Failed:", error)

def main_menu():
    while True:
        print("\n===== CANDIDATE MANAGEMENT =====")
        print("1. Add Candidate")
        print("2. View Candidates")
        print("3. Search Candidate")
        print("4. Update Candidate")
        print("5. Delete Candidate")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_candidate()
        elif choice == "2":
            view_candidates()
        elif choice == "3":
            search_candidate()
        elif choice == "4":
            update_candidate()
        elif choice == "5":
            delete_candidate()
        elif choice == "0":
            print("Returning...")
            break
        else:
            print("Invalid Choice!")


if __name__ == "__main__":
    main_menu()