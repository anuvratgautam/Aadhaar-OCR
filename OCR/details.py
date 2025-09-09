from pydantic import BaseModel, Field
from typing import Annotated, Optional

class Aadhaar_Details(BaseModel):
        '''
        Pydantic class for aadhaar card data validity
        '''
        aadhaar_number: Annotated[str,Field(...,description="extract the 12-digit Aadhaar number (without spaces/hyphens or extra characters)")]
        name: Annotated[str,Field(...,description="full name of the cardholder")]
        father_husband_name: Annotated[str,Field(...,description="father's or husband's name if visible")]
        date_of_birth: Annotated[str,Field(...,description="date of birth in DD/MM/YYYY format")]
        gender: Annotated[str,Field(...,description="One of : Male, Female,Transgender")]
        address: Annotated[str,Field(...,description="complete address including house number, street, area, city, state")]
        pincode: Annotated[str,Field(...,description="pincode")]
        issue_date: Annotated[str,Field(...,description="issue date if visible")]

class Membership_Form(BaseModel):
        '''
        Pydantic class for membership form data_validity
        '''
        # Applicant info
        applicant_name: Annotated[str, Field(description="Full name of the applicant")]
        date_of_birth: Annotated[str, Field(description="Applicant's date of birth in DD/MM/YYYY format")]
        age: Optional[Annotated[int, Field(description="Applicant's age in years")]] = None
        pan_number: Optional[Annotated[str, Field(description="Applicant's PAN number")]] = None
        aadhaar_card: Optional[Annotated[str, Field(description="12-digit Aadhaar number")]] = None
        father_or_spouse_name: Optional[Annotated[str, Field(description="Father's or Husband's name (S/O, W/O, D/O)")]] = None
        address: Optional[Annotated[str, Field(description="Complete residential address")]] = None
        phone_mobile_no: Optional[Annotated[str, Field(description="Mobile/phone number(s)")]] = None
        email_id: Optional[Annotated[str, Field(description="Email ID of applicant")]] = None
        occupation: Optional[Annotated[str, Field(description="Occupation of the applicant")]] = None
        nationality: Optional[Annotated[str, Field(description="Nationality of the applicant")]] = None

        # Nominee details
        nominee_name: Optional[Annotated[str, Field(description="Name of the nominee")]] = None
        nominee_date_of_birth: Optional[Annotated[str, Field(description="Nominee's date of birth in DD/MM/YYYY format")]] = None
        nominee_age: Optional[Annotated[int, Field(description="Nominee's age in years")]] = None
        nominee_sex: Optional[Annotated[str, Field(description="Nominee's sex: M/F")]] = None
        nominee_relationship: Optional[Annotated[str, Field(description="Relationship of nominee with applicant")]] = None

        # Bank details
        bank_name: Optional[Annotated[str, Field(description="Name and branch of the bank")]] = None
        bank_account_no: Optional[Annotated[str, Field(description="Bank account number")]] = None
        ifsc_code: Optional[Annotated[str, Field(description="IFSC code of the bank")]] = None

        # Payment details
        amount_paid: Optional[Annotated[float, Field(description="Membership amount paid in numbers")]] = None
        amount_in_words: Optional[Annotated[str, Field(description="Membership amount in words")]] = None

        # Introducer details
        introducer_name: Optional[Annotated[str, Field(description="Name of the introducer")]] = None
        introducer_code_no: Optional[Annotated[str, Field(description="Introducer's code number")]] = None

        # Signature presence flags
        introducer_signature_present: Optional[Annotated[bool, Field(description="True if introducer's signature is present, False if absent")]] = None
        member_signature_present: Optional[Annotated[bool, Field(description="True if member's signature is present, False if absent")]] = None
        official_signature_present: Optional[Annotated[bool, Field(description="True if official's signature is present, False if absent")]] = None

