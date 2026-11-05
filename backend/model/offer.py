from dataclasses import dataclass
from typing import Optional


@dataclass
class Offer:
    offer_code: str
    application_id: int
    designation: str
    offered_package_lpa: float
    offer_date: str
    expected_joining_date: str
    remarks: Optional[str] = None
    offer_id: Optional[int] = None
    offer_status: str = "OFFERED"