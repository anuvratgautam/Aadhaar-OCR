from OCR import AadhaarExtractor,MembershipFormExtractor
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from typing import Annotated

app = FastAPI()

@app.post('/adhaar')
async def extract_aadhaar(phone:Annotated[int,Form(..., description='Enter Your Number')], front_image: Annotated[UploadFile, File(...,description='Front Image')], back_image: Annotated[UploadFile,File(...,description='Back Image')] ):
    """
    This function prompts the user for the file paths of the front and back
    Aadhaar card images, creates an Aadhaar object, and calls the
    read_aadhaar method to extract the information.
    """
    try:
        aadhaar_extractor = AadhaarExtractor(user_aadhaar_image_front=front_image.file, user_aadhaar_image_back=back_image.file)
        result = aadhaar_extractor.read_aadhaar()
        
        result['phone_number'] = phone

        return result
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"An error occurred: {e}")

@app.post('/member-form')
async def extract_membership_form(form_image: Annotated[UploadFile, File(...,description='Form Image')]):
    '''
    This functions prompts the user for the form image , forms a Membership_Form object 
    and extracts the user information
    '''
    try: 
        form_extractor = MembershipFormExtractor(form_image.file)
        result =  form_extractor.read_form()

        return result
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'An Error Occured: {e}')
