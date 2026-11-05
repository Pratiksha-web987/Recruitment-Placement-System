class CandidateNotFoundError(Exception):
    """Raised when a candidate is not found."""
    pass


class JobNotFoundError(Exception):
    """Raised when a job is not found."""
    pass


class DuplicateApplicationError(Exception):
    """Raised when a candidate applies for the same job again."""
    pass


class CandidateNotEligibleError(Exception):
    """Raised when a candidate is not eligible for a job."""
    pass