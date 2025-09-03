from pydantic import BaseModel, Field
from typing import Annotated

class Aadhaar_Details(BaseModel):
        '''
        Pydantic class for Data Validity
        '''
        aadhaar_number: Annotated[str,Field(...,description="extract the 12-digit Aadhaar number (without spaces/hyphens or extra characters)")]
        name: Annotated[str,Field(...,description="full name of the cardholder")]
        father_husband_name: Annotated[str,Field(...,description="father's or husband's name if visible")]
        date_of_birth: Annotated[str,Field(...,description="date of birth in DD/MM/YYYY format")]
        gender: Annotated[str,Field(...,description="One of : Male, Female,Transgender")]
        address: Annotated[str,Field(...,description="complete address including house number, street, area, city, state")]
        pincode: Annotated[str,Field(...,description="pincode")]
        issue_date: Annotated[str,Field(...,description="issue date if visible")]