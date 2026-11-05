Recruitment & Placement Management System (RPMS)

Project Overview

RPMS is a Python and MySQL-based application designed to manage recruitment and placement activities.

It provides a console-based system for managing candidates, companies, jobs, skills, applications, interviews, interview feedback, offers, placements, and reports.

An HTML/CSS prototype is also included to demonstrate the user interface.

Technologies Used

- Python
- MySQL
- MySQL Connector
- HTML
- CSS
- Visual Studio Code
- MySQL Workbench

Architecture

The backend follows a layered architecture:

Main Application → Service Layer → DAO Layer → MySQL Database

- Model: Stores application data using Python classes.
- DAO: Handles database operations and SQL queries.
- Service: Manages business logic, validations, and application workflows.
- Util: Contains database connection and utility functions.
- Exception: Contains custom exception classes.
- App: Contains application-related components.

Main Modules

1. Candidate Management
2. Company Management
3. Job Management
4. Skills Management
5. Application Management
6. Interview Management
7. Offer Management
8. Placement Management
9. Reports Management

Features

1. Candidate Management

- Add, view, search, and update candidates.
- Manage candidate profile information.
- Store date of birth, gender, college, university, qualification, and passing year.
- Maintain percentage, CGPA, and backlog details.
- Store primary technology and location preferences.

2. Company Management

- Add and view companies.
- Update company information.
- Delete companies with linked-record validation.
- Maintain company contact details and company type.

3. Job Management

- Add, view, and update job openings.
- Manage job status: DRAFT, OPEN, CLOSED, and CANCELLED.
- Configure job openings, package, location, and application deadline.
- Define qualification and eligibility requirements.
- Prevent deletion of jobs linked to other records.

4. Skills Management

- Add and view skills.
- Update skill information.
- Activate and deactivate skills.
- Prevent duplicate skill names.
- Map skills to candidates and jobs.

5. Candidate Skills and Job Skills Mapping

- Assign skills to candidates.
- Maintain proficiency levels: BASIC, INTERMEDIATE, and ADVANCED.
- Store years of experience.
- Mark primary candidate skills.
- Define mandatory and optional job skills.
- Set minimum skill proficiency requirements.

6. Eligibility Checking

- Check candidate eligibility for job applications.
- Validate qualification requirements.
- Check minimum percentage and passing year.
- Validate maximum backlog limits.
- Check job status and application deadline.
- Verify mandatory skills and minimum proficiency levels.
- Display eligibility status and reasons.
- Recheck application eligibility.

7. Application Management

- Add and view applications.
- Update application status.
- Withdraw applications.
- Prevent duplicate applications for the same candidate and job.
- Maintain application eligibility information.

8. Application History Tracking

- Save initial application history.
- Track application status changes.
- Record previous and new application status.
- Store remarks and user information.
- Maintain history during application withdrawal.

9. Interview Management

- Schedule interview rounds.
- Manage round number and interview type.
- Set interview date and time.
- Support ONLINE, OFFLINE, and TELEPHONIC modes.
- Store interviewer and meeting/location details.
- Update interview status.
- Track completed, rescheduled, cancelled, and no-show interviews.

10. Interview Feedback

- Record technical rating.
- Record communication rating.
- Record problem-solving rating.
- Store overall rating.
- Record recommendation and remarks.
- Maintain feedback submission details.
- Prevent duplicate feedback for the same interview.

11. Offer Management

- Add and view offers.
- Update offer information and status.
- Delete offers with placement validation.
- Track offer acceptance and rejection.
- Synchronize offer status with application workflow.
- Maintain application history for relevant status changes.

12. Placement Management

- Add and view placement records.
- Manage joining status and placement status.
- Track expected and actual joining dates.
- Store designation and final package details.
- Validate accepted offers.
- Update candidate placement status.

13. Reports Management

The system provides the following reports:

- Recruitment Summary
- Selected Candidates
- Candidates by Technology
- Open Jobs
- Applications by Status
- Company-wise Recruitment
- Placed Candidates
- Unplaced Candidates

14. Additional Features

- Activity logging.
- Custom exception handling.
- Database connectivity using MySQL Connector.
- Duplicate record prevention.
- Input validation.
- Layered Model–DAO–Service architecture.

Project Structure

Recruitment-Placement-System/
│
├── backend/
│   ├── model/
│   ├── dao/
│   ├── service/
│   ├── util/
│   ├── exception/
│   ├── app/
│   ├── activity_log.txt
│   └── main.py
│
├── css/
│   └── style.css
│
├── sql/
│   └── RPMS_Database_Schema.sql
│
├── Screenshots/
├── venv/
│
├── login.html
├── dashboard.html
├── candidates.html
├── candidate-form.html
├── candidate-details.html
├── companies.html
├── jobs.html
├── job-form.html
├── applications.html
├── interviews.html
├── placement-process.html
├── reports.html
│
├── RPMS_ER_Diagram.mwb
├── RPMS_ER_Diagram.png
├── TEST_CASES.md
├── requirements.txt
└── README.md

Database

- Database Name: "rpms_db"
- Database: MySQL
- Database Schema: "sql/RPMS_Database_Schema.sql"

Import the SQL schema into MySQL Workbench when setting up a new database.

For an existing database, do not execute destructive setup scripts. Preserve existing records.

How to Run

Step 1: Open the Project

Open the project folder in Visual Studio Code.

Step 2: Open Terminal

Open the integrated terminal.

Step 3: Activate Virtual Environment

Windows CMD:

venv\Scripts\activate.bat

Step 4: Install Required Packages

pip install -r requirements.txt

Step 5: Configure Database Connection

Configure your MySQL username and password in:

backend/util/db_connection.py

Step 6: Open Backend Folder

cd backend

Step 7: Run the Application

python main.py

The RPMS Main Menu will appear.

Testing Summary

The following tests have been performed:

- Python syntax compilation.
- MySQL database connection testing.
- Main Menu and all nine module menu testing.
- Candidate Add, View, Search, and Update testing.
- Company Add, View, and Update testing.
- Job Add, View, Update, Status Update, and Delete testing.
- Application Add testing.
- Application status update testing.
- Application history tracking.
- Application eligibility checking and rechecking.
- Application withdrawal testing.
- Skills listing and duplicate skill validation.

Additional module workflows, including interview feedback, offers, placements, and reports, should be verified as part of final testing.

Detailed test cases are documented in "TEST_CASES.md".

Project Deliverables

- Python source code.
- MySQL database schema.
- Editable ER Diagram (MWB and PNG).
- HTML/CSS UI prototype.
- Test cases.
- Application screenshots.
- Project documentation.

Project Type

Student Project – Python + MySQL

Project Name: RPMS
Full Name: Recruitment & Placement Management System