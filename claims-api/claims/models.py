import datetime as dt
from typing import Annotated, List

from pydantic import BaseModel, StringConstraints


ICDCode = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True, to_upper=True, pattern=r"^[A-Z][A-Z0-9]+$"
    ),
]


class Claim(BaseModel):
    id: str
    icd_code: str
    claim_date: dt.date
    claim_value: float
    claim_provider: str


class GetClaimsResponse(BaseModel):
    claims: List[Claim]
