from dataclasses import dataclass
from typing import Optional


@dataclass
class Placement:
    candidate_id: int
    company_id: int
    job_id: int
    offer_id: int
    designation: str
    final_package_lpa: float
    expected_joining_date: str
    actual_joining_date: Optional[str] = None
    joining_status: str = "PENDING"
    placement_status: str = "ACTIVE"
    placement_id: Optional[int] = None