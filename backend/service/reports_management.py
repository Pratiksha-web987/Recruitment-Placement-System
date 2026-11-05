from dao.report_dao import ReportDAO
from model.report import Report


report_dao = ReportDAO()


def display_report(report):
    if report is None:
        print("Unable to generate report. Check database connection.")
        return

    print(f"\n========== {report.title} ==========")

    if isinstance(report.data, dict):
        if not report.data:
            print("No Records Found.")
            return

        for title, value in report.data.items():
            print(f"{title}: {value}")

    elif isinstance(report.data, int):
        print("Total Selected Candidates:", report.data)

    elif not report.data:
        print("No Records Found.")

    else:
        for record in report.data:
            print("----------------------------------------")
            print(record)


def show_summary_report():
    data = report_dao.get_summary_report()
    display_report(Report("RPMS SUMMARY REPORT", data))


def show_selected_candidates():
    data = report_dao.get_selected_candidates()

    if data is not None:
        print("\n========== SELECTED CANDIDATES REPORT ==========")
        print("Total Selected Candidates:", data)
    else:
        print("Unable to generate report. Check database connection.")


def show_candidates_by_technology():
    data = report_dao.get_candidates_by_technology()

    if data is None:
        print("Unable to generate report.")
        return

    print("\n========== CANDIDATES BY TECHNOLOGY ==========")

    if not data:
        print("No Records Found.")
        return

    for technology, total in data:
        print(f"{technology}: {total}")


def show_open_jobs():
    data = report_dao.get_open_jobs()

    if data is None:
        print("Unable to generate report.")
        return

    print("\n========== OPEN JOBS REPORT ==========")

    if not data:
        print("No Open Jobs Found.")
        return

    for job_code, title, company, location, openings, deadline in data:
        print("----------------------------------------")
        print("Job Code:", job_code)
        print("Job Title:", title)
        print("Company:", company)
        print("Location:", location)
        print("Openings:", openings)
        print("Application Deadline:", deadline)


def show_applications_by_status():
    data = report_dao.get_applications_by_status()

    if data is None:
        print("Unable to generate report.")
        return

    print("\n========== APPLICATIONS BY STATUS ==========")

    if not data:
        print("No Records Found.")
        return

    for status, total in data:
        print(f"{status}: {total}")


def show_company_wise_placements():
    data = report_dao.get_company_wise_placements()

    if data is None:
        print("Unable to generate report.")
        return

    print("\n========== COMPANY-WISE PLACEMENT REPORT ==========")

    if not data:
        print("No Company Records Found.")
        return

    for company, total in data:
        print(f"{company}: {total}")


def show_placed_candidates():
    data = report_dao.get_placed_candidates()

    if data is None:
        print("Unable to generate report.")
        return

    print("\n========== PLACED CANDIDATES REPORT ==========")

    if not data:
        print("No Placed Candidates Found.")
        return

    for code, name, company, designation, package in data:
        print("----------------------------------------")
        print("Candidate Code:", code)
        print("Candidate Name:", name)
        print("Company:", company)
        print("Designation:", designation)
        print("Package:", package, "LPA")


def show_unplaced_candidates():
    data = report_dao.get_unplaced_candidates()

    if data is None:
        print("Unable to generate report.")
        return

    print("\n========== UNPLACED CANDIDATES REPORT ==========")

    if not data:
        print("No Unplaced Candidates Found.")
        return

    for code, name, qualification, technology, percentage in data:
        print("----------------------------------------")
        print("Candidate Code:", code)
        print("Candidate Name:", name)
        print("Qualification:", qualification)
        print("Technology:", technology)
        print("Percentage:", percentage)


def main_menu():

    while True:
        print("\n========== REPORTS MANAGEMENT ==========")
        print("1. Summary Report")
        print("2. Selected Candidates Report")
        print("3. Candidates by Technology")
        print("4. Open Jobs Report")
        print("5. Applications by Status")
        print("6. Company-wise Placement Report")
        print("7. Placed Candidates Report")
        print("8. Unplaced Candidates Report")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_summary_report()
        elif choice == "2":
            show_selected_candidates()
        elif choice == "3":
            show_candidates_by_technology()
        elif choice == "4":
            show_open_jobs()
        elif choice == "5":
            show_applications_by_status()
        elif choice == "6":
            show_company_wise_placements()
        elif choice == "7":
            show_placed_candidates()
        elif choice == "8":
            show_unplaced_candidates()
        elif choice == "0":
            break
        else:
            print("Invalid Choice! Please try again.")


if __name__ == "__main__":
    main_menu()