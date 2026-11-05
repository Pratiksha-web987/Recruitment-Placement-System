from dataclasses import dataclass
from typing import Optional


@dataclass
class Application:
    application_code: str
    candidate_id: int
    job_id: int
    eligibility_status: str = "PENDING"
    eligibility_reason: str = ""
    application_status: str = "APPLIED"
    source: Optional[str] = None
    assigned_recruiter_id: Optional[int] = None
    application_id: Optional[int] = None
    applied_at: Optional[str] = None