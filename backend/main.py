from service import candidate_management
from service import company_management
from service import job_management
from service import application_management
from service import interview_management
from service import offer_management
from service import placement_management
from service import reports_management
from service import skill_management


while True:
    print("\n========== RPMS MAIN MENU ==========")
    print("1. Candidate Management")
    print("2. Company Management")
    print("3. Job Management")
    print("4. Application Management")
    print("5. Interview Management")
    print("6. Offer Management")
    print("7. Placement Management")
    print("8. Reports Management")
    print("9. Skills Management")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        candidate_management.main_menu()

    elif choice == "2":
        company_management.main_menu()

    elif choice == "3":
        job_management.main_menu()

    elif choice == "4":
        application_management.main_menu()

    elif choice == "5":
        interview_management.main_menu()

    elif choice == "6":
        offer_management.main_menu()

    elif choice == "7":
        placement_management.main_menu()

    elif choice == "8":
        reports_management.main_menu()

    elif choice == "9":
       skill_management.main_menu()    

    elif choice == "0":
        print("RPMS Program Closed.")
        break

    else:
        print("Invalid Choice! Please try again.")