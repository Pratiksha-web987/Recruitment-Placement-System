from datetime import datetime

from model.placement import Placement
from dao.placement_dao import PlacementDAO
from util.activity_logger import log_activity


placement_dao = PlacementDAO()


def valid_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# ==========================================
# ADD PLACEMENT
# ==========================================

def add_placement():

    try:
        candidate_id = int(input("Enter Candidate ID: "))
        company_id = int(input("Enter Company ID: "))
        job_id = int(input("Enter Job ID: "))
        offer_id = int(input("Enter Offer ID: "))

        if min(candidate_id, company_id, job_id, offer_id) <= 0:
            print("All IDs must be positive numbers.")
            return

        designation = input("Enter Designation: ").strip()
        final_package = float(input("Enter Final Package (LPA): "))

        expected_date = input(
            "Enter Expected Joining Date (YYYY-MM-DD): "
        ).strip()

        actual_date = input(
            "Enter Actual Joining Date (YYYY-MM-DD) or press Enter: "
        ).strip() or None

        joining_status = input(
            "Enter Joining Status (PENDING/JOINED/NOT_JOINED): "
        ).strip().upper()

        placement_status = input(
            "Enter Placement Status (ACTIVE/COMPLETED/CANCELLED): "
        ).strip().upper()

        if not designation or final_package <= 0:
            print("Please enter a valid designation and package.")
            return

        if not valid_date(expected_date):
            print("Invalid Expected Joining Date.")
            return

        if actual_date and not valid_date(actual_date):
            print("Invalid Actual Joining Date.")
            return

        if joining_status not in ("PENDING", "JOINED", "NOT_JOINED"):
            print("Invalid Joining Status.")
            return

        if placement_status not in ("ACTIVE", "COMPLETED", "CANCELLED"):
            print("Invalid Placement Status.")
            return

        placement = Placement(
            candidate_id=candidate_id,
            company_id=company_id,
            job_id=job_id,
            offer_id=offer_id,
            designation=designation,
            final_package_lpa=final_package,
            expected_joining_date=expected_date,
            actual_joining_date=actual_date,
            joining_status=joining_status,
            placement_status=placement_status
        )

        result = placement_dao.add_placement(placement)

        if result == "INVALID_CANDIDATE":
            print("Candidate ID Not Found.")

        elif result == "INVALID_OFFER":
            print("Invalid Offer! Details do not match an accepted offer.")

        elif result == "EXISTING_PLACEMENT":
            print("This candidate already has an active placement.")

        elif result is None:
            print("Database connection failed.")

        else:
            log_activity(
                f"Placement Created: Placement ID {result}, "
                f"Candidate ID {candidate_id}, Company ID {company_id}, "
                f"Job ID {job_id}, Offer ID {offer_id}"
            )

            print("\nPlacement Added Successfully!")
            print("Placement ID:", result)

    except ValueError:
        print("Please enter valid numeric values and dates.")

    except Exception as error:
        print("Placement Add Failed:", error)


# ==========================================
# VIEW PLACEMENTS
# ==========================================

def view_placements():

    try:
        records = placement_dao.view_placements()

        print("\n===== PLACEMENT LIST =====")

        if not records:
            print("No Placements Found.")
            return

        for row in records:
            print("\nPlacement ID:", row[0])
            print("Candidate:", row[1])
            print("Company:", row[2])
            print("Job:", row[3])
            print("Designation:", row[4])
            print("Package (LPA):", row[5])
            print("Expected Joining:", row[6])
            print("Actual Joining:", row[7])
            print("Joining Status:", row[8])
            print("Placement Status:", row[9])

    except Exception as error:
        print("View Placements Failed:", error)


# ==========================================
# UPDATE PLACEMENT
# ==========================================

def update_placement():

    joining_statuses = {
        "1": "PENDING",
        "2": "JOINED",
        "3": "NOT_JOINED"
    }

    placement_statuses = {
        "1": "ACTIVE",
        "2": "COMPLETED",
        "3": "CANCELLED"
    }

    try:
        placement_id = int(input("Enter Placement ID: "))

        if placement_id <= 0:
            print("Placement ID must be positive.")
            return

        placement = placement_dao.get_placement_by_id(placement_id)

        if placement is None:
            print("Placement ID Not Found.")
            return

        current_joining_status = placement[3]
        current_placement_status = placement[4]

        print("\nCurrent Joining Status:", current_joining_status)
        print("1. PENDING")
        print("2. JOINED")
        print("3. NOT_JOINED")

        joining_choice = input(
            "Select Joining Status: "
        ).strip()

        if joining_choice not in joining_statuses:
            print("Invalid Joining Status Choice.")
            return

        new_joining_status = joining_statuses[joining_choice]

        print("\nCurrent Placement Status:", current_placement_status)
        print("1. ACTIVE")
        print("2. COMPLETED")
        print("3. CANCELLED")

        placement_choice = input(
            "Select Placement Status: "
        ).strip()

        if placement_choice not in placement_statuses:
            print("Invalid Placement Status Choice.")
            return

        new_placement_status = placement_statuses[placement_choice]

        actual_date = input(
            "Enter Actual Joining Date (YYYY-MM-DD) or press Enter: "
        ).strip() or None

        if actual_date and not valid_date(actual_date):
            print("Invalid Actual Joining Date.")
            return

        updated = placement_dao.update_placement(
            placement_id,
            new_joining_status,
            new_placement_status,
            actual_date
        )

        if updated:
            log_activity(
                f"Placement Updated: Placement ID {placement_id}, "
                f"Joining Status: {current_joining_status} -> "
                f"{new_joining_status}, "
                f"Placement Status: {current_placement_status} -> "
                f"{new_placement_status}, "
                f"Actual Joining Date: {actual_date}"
            )

            print("Placement Updated Successfully!")

        else:
            print("Placement ID Not Found.")

    except ValueError:
        print("Please enter a valid Placement ID.")

    except Exception as error:
        print("Placement Update Failed:", error)


# ==========================================
# DELETE PLACEMENT
# ==========================================

def delete_placement():

    try:
        placement_id = int(input("Enter Placement ID: "))

        if placement_id <= 0:
            print("Placement ID must be positive.")
            return

        placement = placement_dao.get_placement_by_id(placement_id)

        if placement is None:
            print("Placement ID Not Found.")
            return

        confirm = input(
            "Are you sure you want to delete? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Delete Cancelled.")
            return

        if placement_dao.delete_placement(placement_id):
            log_activity(
                f"Placement Deleted: Placement ID {placement_id}, "
                f"Candidate ID {placement[0]}, Company ID {placement[1]}, "
                f"Job ID {placement[2]}"
            )

            print("Placement Deleted Successfully!")

        else:
            print("Placement ID Not Found.")

    except ValueError:
        print("Please enter a valid Placement ID.")

    except Exception as error:
        print("Placement Delete Failed:", error)


# ==========================================
# PLACEMENT MANAGEMENT MAIN MENU
# ==========================================

def main_menu():

    while True:
        print("\n===== PLACEMENT MANAGEMENT =====")
        print("1. Add Placement")
        print("2. View Placements")
        print("3. Update Placement")
        print("4. Delete Placement")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_placement()

        elif choice == "2":
            view_placements()

        elif choice == "3":
            update_placement()

        elif choice == "4":
            delete_placement()

        elif choice == "0":
            break

        else:
            print("Invalid Choice! Please try again.")


if __name__ == "__main__":
    main_menu()