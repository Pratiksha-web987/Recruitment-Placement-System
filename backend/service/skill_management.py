from model.skill import Skill
from dao.skill_dao import SkillDAO


dao = SkillDAO()

LEVELS = ("BASIC", "INTERMEDIATE", "ADVANCED")


def add_skill():
    print("\n========== ADD SKILL ==========")

    name = input("Enter Skill Name: ").strip()
    category = input("Enter Category (optional): ").strip()

    if not name:
        print("Skill name is required.")
        return

    try:
        skill = Skill(
            skill_name=name,
            category=category if category else None
        )

        dao.add_skill(skill)
        print("Skill added successfully.")

    except Exception as e:
        print("Unable to add skill:", e)


def view_skills():
    print("\n========== SKILLS LIST ==========")

    try:
        skills = dao.view_skills()

        if not skills:
            print("No skills found.")
            return

        for skill in skills:
            status = "ACTIVE" if skill["is_active"] else "INACTIVE"

            print(
                f'ID: {skill["skill_id"]} | '
                f'Name: {skill["skill_name"]} | '
                f'Category: {skill["category"]} | '
                f'Status: {status}'
            )

    except Exception as e:
        print("Unable to view skills:", e)


def update_skill():
    view_skills()

    try:
        skill_id = int(input("\nEnter Skill ID: "))
        name = input("Enter New Skill Name: ").strip()
        category = input("Enter New Category: ").strip()

        if not name:
            print("Skill name is required.")
            return

        if dao.update_skill(
            skill_id, name, category if category else None
        ):
            print("Skill updated successfully.")
        else:
            print("Skill ID not found.")

    except ValueError:
        print("Please enter a valid Skill ID.")

    except Exception as e:
        print("Unable to update skill:", e)


def change_skill_status():
    view_skills()

    try:
        skill_id = int(input("\nEnter Skill ID: "))
        choice = input("1. Activate  2. Deactivate: ").strip()

        if choice == "1":
            result = dao.activate_skill(skill_id)
        elif choice == "2":
            result = dao.deactivate_skill(skill_id)
        else:
            print("Invalid choice.")
            return

        print("Skill status updated." if result else "Skill ID not found.")

    except ValueError:
        print("Please enter a valid Skill ID.")

    except Exception as e:
        print("Unable to change skill status:", e)


def manage_candidate_skills():
    try:
        candidate_id = int(input("\nEnter Candidate ID: "))
        print("\n1. Add Candidate Skill")
        print("2. View Candidate Skills")
        print("3. Remove Candidate Skill")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            view_skills()

            skill_id = int(input("Enter Skill ID: "))
            level = input(
                "Proficiency (BASIC/INTERMEDIATE/ADVANCED): "
            ).strip().upper()

            if level not in LEVELS:
                print("Invalid proficiency level.")
                return

            experience = float(input("Years of Experience: "))

            if experience < 0 or experience > 999.9:
                print("Experience must be between 0 and 999.9.")
                return

            primary = input("Is Primary Skill? (Y/N): ").strip().upper()

            if primary not in ("Y", "N"):
                print("Enter Y or N.")
                return

            if primary == "Y":
                print(
                    "Note: Set only one primary skill per candidate."
                )

            dao.add_candidate_skill(
                candidate_id,
                skill_id,
                level,
                experience,
                1 if primary == "Y" else 0
            )

            print("Candidate skill added successfully.")

        elif choice == "2":
            skills = dao.view_candidate_skills(candidate_id)

            if not skills:
                print("No skills assigned.")
                return

            for item in skills:
                print(
                    f'Candidate Skill ID: {item["candidate_skill_id"]} | '
                    f'{item["skill_name"]} | '
                    f'{item["proficiency_level"]} | '
                    f'{item["years_experience"]} years | '
                    f'Primary: {item["is_primary"]}'
                )

        elif choice == "3":
            skills = dao.view_candidate_skills(candidate_id)

            for item in skills:
                print(
                    f'{item["candidate_skill_id"]}. '
                    f'{item["skill_name"]}'
                )

            skill_row_id = int(
                input("Enter Candidate Skill ID to remove: ")
            )

            if dao.remove_candidate_skill(skill_row_id):
                print("Candidate skill removed.")
            else:
                print("Candidate skill record not found.")

        else:
            print("Invalid choice.")

    except ValueError:
        print("Please enter valid numeric values.")

    except Exception as e:
        print("Unable to manage candidate skills:", e)


def manage_job_skills():
    try:
        job_id = int(input("\nEnter Job ID: "))
        print("\n1. Add Job Skill")
        print("2. View Job Skills")
        print("3. Remove Job Skill")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            view_skills()

            skill_id = int(input("Enter Skill ID: "))
            level = input(
                "Minimum Level (BASIC/INTERMEDIATE/ADVANCED): "
            ).strip().upper()

            if level and level not in LEVELS:
                print("Invalid proficiency level.")
                return

            mandatory = input(
                "Mandatory Skill? (Y/N): "
            ).strip().upper()

            if mandatory not in ("Y", "N"):
                print("Enter Y or N.")
                return

            dao.add_job_skill(
                job_id,
                skill_id,
                level if level else None,
                1 if mandatory == "Y" else 0
            )

            print("Job skill added successfully.")

        elif choice == "2":
            skills = dao.view_job_skills(job_id)

            if not skills:
                print("No skills assigned to this job.")
                return

            for item in skills:
                print(
                    f'Job Skill ID: {item["job_skill_id"]} | '
                    f'{item["skill_name"]} | '
                    f'Minimum: {item["minimum_level"]} | '
                    f'Mandatory: {item["mandatory_flag"]}'
                )

        elif choice == "3":
            skills = dao.view_job_skills(job_id)

            for item in skills:
                print(
                    f'{item["job_skill_id"]}. '
                    f'{item["skill_name"]}'
                )

            row_id = int(input("Enter Job Skill ID to remove: "))

            if dao.remove_job_skill(row_id):
                print("Job skill removed.")
            else:
                print("Job skill record not found.")

        else:
            print("Invalid choice.")

    except ValueError:
        print("Please enter valid numeric values.")

    except Exception as e:
        print("Unable to manage job skills:", e)


def main_menu():
    while True:
        print("\n========== SKILLS MANAGEMENT ==========")
        print("1. Add Skill")
        print("2. View Skills")
        print("3. Update Skill")
        print("4. Activate / Deactivate Skill")
        print("5. Manage Candidate Skills")
        print("6. Manage Job Skills")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_skill()
        elif choice == "2":
            view_skills()
        elif choice == "3":
            update_skill()
        elif choice == "4":
            change_skill_status()
        elif choice == "5":
            manage_candidate_skills()
        elif choice == "6":
            manage_job_skills()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")