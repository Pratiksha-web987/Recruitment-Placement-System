from dataclasses import dataclass


@dataclass
class Company:
    company_code: str
    company_name: str
    industry: str = ""
    website: str = ""
    location: str = ""
    company_type: str = ""
    hr_name: str = ""
    hr_email: str = ""
    hr_mobile: str = ""
    company_id: int = None
    status: str = "ACTIVE"