from dataclasses import dataclass
from typing import Optional


@dataclass
class Interview:
    application_id: int
    round_number: int
    round_type: str
    scheduled_date: str
    scheduled_time: str
    mode: str
    interviewer_name: Optional[str] = None
    meeting_or_location: Optional[str] = None
    interview_id: Optional[int] = None
    status: str = "SCHEDULED"