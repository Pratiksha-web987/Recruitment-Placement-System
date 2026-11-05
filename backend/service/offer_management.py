from model.offer import Offer
from dao.offer_dao import OfferDAO
from util.activity_logger import log_activity


offer_dao = OfferDAO()


# ==========================================
# ADD OFFER
# ==========================================

def add_offer():

    try:
        print("\n========== ADD NEW OFFER ==========")

        application_id = int(input("Enter Application ID: "))
        offer_code = input("Enter Offer Code: ").strip()
        designation = input("Enter Designation: ").strip()
        package = float(input("Enter Offered Package (LPA): "))
        offer_date = input("Enter Offer Date (YYYY-MM-DD): ").strip()
        joining_date = input(
            "Enter Expected Joining Date (YYYY-MM-DD): "
        ).strip()
        remarks = input("Enter Remarks (Optional): ").strip()

        if not offer_code or not designation:
            print("Offer Code and Designation are required!")
            return

        if package <= 0:
            print("Package must be greater than zero!")
            return

        changed_by = int(
            input("Enter Your User ID (for application history): ")
        )

        offer = Offer(
            offer_code=offer_code,
            application_id=application_id,
            designation=designation,
            offered_package_lpa=package,
            offer_date=offer_date,
            expected_joining_date=joining_date,
            remarks=remarks or None
        )

        result = offer_dao.add_offer(offer, changed_by)

        if result == "NOT_FOUND":
            print("Application ID Not Found!")

        elif result == "NOT_SELECTED":
            print("Offer can only be created for SELECTED applications!")

        elif result is None:
            print("Database connection failed!")

        else:
            log_activity(
                f"Offer Created: {offer_code} (ID: {result}), "
                f"Application ID: {application_id}"
            )

            log_activity(
                f"Application Status Updated: Application ID "
                f"{application_id} (SELECTED -> OFFERED)"
            )

            print("\nOffer Added Successfully!")
            print("Offer ID:", result)
            print("Application History Saved Successfully.")

    except ValueError as error:
        print("Please enter valid values:", error)

    except Exception as error:
        print("Offer Add Failed:", error)


# ==========================================
# VIEW ALL OFFERS
# ==========================================

def view_offers():

    try:
        records = offer_dao.view_offers()

        print("\n========== OFFER LIST ==========")

        if not records:
            print("No Offers Found!")
            return

        for row in records:
            print("\nOffer ID:", row[0])
            print("Offer Code:", row[1])
            print("Candidate:", row[2])
            print("Job:", row[3])
            print("Designation:", row[4])
            print("Package:", row[5], "LPA")
            print("Offer Date:", row[6])
            print("Joining Date:", row[7])
            print("Offer Status:", row[8])
            print("-" * 40)

    except Exception as error:
        print("Offer View Failed:", error)


# ==========================================
# UPDATE OFFER
# ==========================================

def update_offer():

    statuses = {
        "1": "OFFERED",
        "2": "ACCEPTED",
        "3": "REJECTED"
    }

    try:
        offer_id = int(input("\nEnter Offer ID to Update: "))

        offer = offer_dao.get_offer_by_id(offer_id)

        if offer is None:
            print("Offer ID Not Found!")
            return

        offer_code = offer[1]
        current_status = offer[3]
        current_designation = offer[4]

        print("\n1. Update Designation")
        print("2. Update Package")
        print("3. Update Expected Joining Date")
        print("4. Update Offer Status")
        print("5. Update Remarks")

        choice = input("Enter your choice: ").strip()

        changed_by = None

        if choice == "1":
            value = input("Enter New Designation: ").strip()

            if not value:
                print("Designation cannot be empty!")
                return

            field = "designation"
            log_message = (
                f"Offer Updated: {offer_code} "
                f"(Designation: {current_designation} -> {value}) "
                f"(ID: {offer_id})"
            )

        elif choice == "2":
            value = float(input("Enter New Package (LPA): "))

            if value <= 0:
                print("Package must be greater than zero!")
                return

            field = "package"
            log_message = (
                f"Offer Updated: {offer_code} "
                f"(Package changed to {value} LPA) (ID: {offer_id})"
            )

        elif choice == "3":
            value = input(
                "Enter New Joining Date (YYYY-MM-DD): "
            ).strip()

            if not value:
                print("Joining Date cannot be empty!")
                return

            field = "joining_date"
            log_message = (
                f"Offer Updated: {offer_code} "
                f"(Joining Date changed to {value}) (ID: {offer_id})"
            )

        elif choice == "4":
            print("\n1. OFFERED")
            print("2. ACCEPTED")
            print("3. REJECTED")

            status_choice = input("Select New Status: ").strip()

            if status_choice not in statuses:
                print("Invalid Status!")
                return

            value = statuses[status_choice]
            field = "status"

            changed_by = int(
                input("Enter Your User ID (for application history): ")
            )

            log_message = (
                f"Offer Status Updated: {offer_code} "
                f"({current_status} -> {value}) (ID: {offer_id})"
            )

        elif choice == "5":
            value = input("Enter New Remarks: ")
            field = "remarks"

            log_message = (
                f"Offer Updated: {offer_code} "
                f"(Remarks Updated) (ID: {offer_id})"
            )

        else:
            print("Invalid Choice!")
            return

        updated = offer_dao.update_offer(
            offer_id, field, value, changed_by
        )

        if updated:
            log_activity(log_message)

            if choice == "4":
                print("\nOffer Status Updated Successfully!")
                print("Application History updated if application status changed.")
            else:
                print("\nOffer Updated Successfully!")

        else:
            print("Offer could not be updated.")

    except ValueError as error:
        print("Please enter valid values:", error)

    except Exception as error:
        print("Offer Update Failed:", error)


# ==========================================
# DELETE OFFER
# ==========================================

def delete_offer():

    try:
        offer_id = int(input("\nEnter Offer ID to Delete: "))

        offer = offer_dao.get_offer_by_id(offer_id)

        if offer is None:
            print("Offer ID Not Found!")
            return

        confirm = input(
            "Are you sure you want to delete? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Delete Cancelled!")
            return

        changed_by = int(
            input("Enter Your User ID (for application history): ")
        )

        result = offer_dao.delete_offer(offer_id, changed_by)

        if result == "NOT_FOUND":
            print("Offer ID Not Found!")

        elif result == "LINKED":
            print(
                "Cannot Delete! This Offer is already linked to a Placement."
            )

        elif result:
            log_activity(
                f"Offer Deleted: {result[1]} (ID: {offer_id}), "
                f"Application ID: {result[0]}"
            )

            print("Offer Deleted Successfully!")
            print("Application History Saved if its status changed.")

        else:
            print("Offer could not be deleted.")

    except ValueError as error:
        print("Please enter valid values:", error)

    except Exception as error:
        print("Offer Delete Failed:", error)


# ==========================================
# OFFER MANAGEMENT MAIN MENU
# ==========================================

def main_menu():

    while True:
        print("\n========== OFFER MANAGEMENT ==========")
        print("1. Add Offer")
        print("2. View All Offers")
        print("3. Update Offer")
        print("4. Delete Offer")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_offer()

        elif choice == "2":
            view_offers()

        elif choice == "3":
            update_offer()

        elif choice == "4":
            delete_offer()

        elif choice == "0":
            break

        else:
            print("Invalid Choice! Please try again.")


if __name__ == "__main__":
    main_menu()