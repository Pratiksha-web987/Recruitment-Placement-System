from dataclasses import dataclass


@dataclass
class Candidate:
    candidate_code: str
    full_name: str
    email: str
    mobile: str
    qualification: str
    passing_year: int

    candidate_id: int = None
    percentage: float = 0.0
    backlog_count: int = 0
    primary_technology: str = ""
    profile_status: str = "ACTIVE"
    placement_status: str = "NOT_PLACED"

    date_of_birth: str = None
    gender: str = None
    college: str = None
    university: str = None
    cgpa: float = None
    current_location: str = None
    preferred_location: str = None