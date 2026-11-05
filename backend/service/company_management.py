from model.company import Company
from dao.company_dao import CompanyDAO
from util.activity_logger import log_activity


company_dao = CompanyDAO()


# 1. ADD COMPANY
def add_company():
    print("\n===== ADD NEW COMPANY =====")

    try:
        company = Company(
            company_code=input("Enter Company Code: ").strip(),
            company_name=input("Enter Company Name: ").strip(),
            industry=input("Enter Industry: ").strip(),
            website=input("Enter Website: ").strip(),
            location=input("Enter Location: ").strip(),
            company_type=input("Enter Company Type: ").strip(),
            hr_name=input("Enter HR Name: ").strip(),
            hr_email=input("Enter HR Email: ").strip(),
            hr_mobile=input("Enter HR Mobile: ").strip()
        )

        if not company.company_code or not company.company_name:
            print("Company Code and Company Name are required!")
            return

        company_id = company_dao.add_company(company)

        if company_id is None:
            print("Database connection failed.")
            return

        log_activity(
            f"Company Created: {company.company_name} "
            f"(ID: {company_id}, Code: {company.company_code})"
        )

        print("\nCompany Added Successfully!")
        print("Company ID:", company_id)

    except Exception as error:
        print("Company Add Failed:", error)


# 2. VIEW COMPANIES
def view_companies():
    try:
        companies = company_dao.view_companies()

        print("\n===== COMPANY LIST =====")

        if not companies:
            print("No Companies Found.")
            return

        for company in companies:
            print("\n----------------------------")
            print("Company ID:", company.company_id)
            print("Company Code:", company.company_code)
            print("Company Name:", company.company_name)
            print("Industry:", company.industry)
            print("Website:", company.website)
            print("Location:", company.location)
            print("Company Type:", company.company_type)
            print("HR Name:", company.hr_name)
            print("HR Email:", company.hr_email)
            print("HR Mobile:", company.hr_mobile)
            print("Status:", company.status)

    except Exception as error:
        print("Company View Failed:", error)


# 3. UPDATE COMPANY
def update_company():
    try:
        company_id = int(input("Enter Company ID to Update: "))

        existing_company = company_dao.get_company_by_id(company_id)

        if existing_company is None:
            print("Company Not Found!")
            return

        old_name = existing_company.company_name

        print("\nEnter New Company Details:")

        company = Company(
            company_id=company_id,
            company_code=existing_company.company_code,
            company_name=input("Enter Company Name: ").strip(),
            industry=input("Enter Industry: ").strip(),
            website=input("Enter Website: ").strip(),
            location=input("Enter Location: ").strip(),
            company_type=input("Enter Company Type: ").strip(),
            hr_name=input("Enter HR Name: ").strip(),
            hr_email=input("Enter HR Email: ").strip(),
            hr_mobile=input("Enter HR Mobile: ").strip(),
            status=existing_company.status
        )

        if not company.company_name:
            print("Company Name is required!")
            return

        updated = company_dao.update_company(company)

        if updated:
            log_activity(
                f"Company Updated: {old_name} -> "
                f"{company.company_name} (ID: {company_id})"
            )
            print("Company Updated Successfully!")
        else:
            print("Company Update Failed.")

    except ValueError:
        print("Please Enter a Valid Company ID!")

    except Exception as error:
        print("Company Update Failed:", error)


# 4. DELETE COMPANY
def delete_company():
    try:
        company_id = int(input("Enter Company ID to Delete: "))

        company = company_dao.get_company_by_id(company_id)

        if company is None:
            print("Company Not Found!")
            return

        print("\nCompany Name:", company.company_name)

        confirm = input(
            "Are you sure? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Delete Cancelled!")
            return

        result = company_dao.delete_company(company_id)

        if result == "LINKED":
            print(
                "Cannot Delete Company! Jobs or Placements "
                "are linked to this company."
            )

        elif result:
            log_activity(
                f"Company Deleted: {company.company_name} "
                f"(ID: {company_id})"
            )
            print("Company Deleted Successfully!")

        else:
            print("Company could not be deleted.")

    except ValueError:
        print("Please Enter a Valid Company ID!")

    except Exception as error:
        print("Company Delete Failed:", error)

# 5. COMPANY MANAGEMENT MENU
def main_menu():
    while True:
        print("\n===== RPMS COMPANY MANAGEMENT =====")
        print("1. Add Company")
        print("2. View Companies")
        print("3. Update Company")
        print("4. Delete Company")
        print("0. Back to Main Menu")

        choice = input("Enter Your Choice: ").strip()

        if choice == "1":
            add_company()

        elif choice == "2":
            view_companies()

        elif choice == "3":
            update_company()

        elif choice == "4":
            delete_company()

        elif choice == "0":
            break

        else:
            print("Invalid Choice! Please Try Again!")


if __name__ == "__main__":
    main_menu()