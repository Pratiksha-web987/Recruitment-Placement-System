from dataclasses import dataclass


@dataclass
class Job:
    job_code: str
    company_id: int
    job_title: str
    employment_type: str
    location: str
    openings: int
    min_package_lpa: float = None
    max_package_lpa: float = None
    min_percentage: float = None
    min_passing_year: int = None
    max_passing_year: int = None
    max_backlogs: int = 0
    experience_min_years: float = 0.0
    qualification_rule: str = ""
    posted_date: str = None
    application_deadline: str = None
    created_by: int = None
    job_id: int = None
    status: str = "OPEN"