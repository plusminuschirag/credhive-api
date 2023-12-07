from pydantic import BaseModel, EmailStr, HttpUrl, validator
from datetime import date
from typing import Optional
import re


class CreditData(BaseModel):
    CIN: str
    company_name: str
    address: str
    registration_date: date
    number_of_employees: int
    raised_capital: float
    turnover: float
    net_profit: float
    contact_number: str
    contact_email: EmailStr
    company_website: HttpUrl
    loan_amount: float
    loan_interest_percentage: float
    account_status: str

    # Custom validators on top of incoming data.
    @validator("CIN")
    def cin_must_be_alphanumeric(cls, value):
        if not re.match(r"^[0-9a-zA-Z]*$", value):
            raise ValueError("CIN must be alphanumeric")
        return value

    @validator("registration_date")
    def date_must_be_past(cls, value):
        if value > date.today():
            raise ValueError("Registration date must not be in the future.")
        return value

    @validator(
        "number_of_employees",
        "raised_capital",
        "turnover",
        "net_profit",
        "loan_amount",
        "loan_interest_percentage",
        pre=True,
    )
    def must_not_be_negative(cls, value):
        if value < 0:
            raise ValueError("Value must not be negative.")
        return value


class PutCreditData(BaseModel):
    company_name: Optional[str] = None
    address: Optional[str] = None
    registration_date: Optional[date] = None
    number_of_employees: Optional[int] = None
    raised_capital: Optional[float] = None
    turnover: Optional[float] = None
    net_profit: Optional[float] = None
    contact_number: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    company_website: Optional[HttpUrl] = None
    loan_amount: Optional[float] = None
    loan_interest_percentage: Optional[float] = None
    account_status: Optional[str] = None

    @validator("registration_date", pre=True, always=True)
    def date_must_be_past_or_none(cls, value):
        if value is not None and value > date.today():
            raise ValueError("Registration date must not be in the future or None.")
        return value

    @validator(
        "number_of_employees",
        "raised_capital",
        "turnover",
        "net_profit",
        "loan_amount",
        "loan_interest_percentage",
        pre=True,
        always=True,
    )
    def must_not_be_negative_or_none(cls, value):
        if value is not None and value < 0:
            raise ValueError("Value must not be negative or None.")
        return value
