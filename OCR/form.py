#Module imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import base64

from .details import Membership_Form

load_dotenv()

class MembershipFormExtractor:

    def __init__(self,form) -> None:
        self.form = form 
        self.model =  ChatOpenAI(model='gpt-5')
        self.structured_model = self.model.with_structured_output(Membership_Form)

    def read_form(self)-> dict:
        '''
        Function to read and extract the extract output of the Form and return the JSON
        '''
        if self.form:
            form_image =  base64.b64encode(self.form.read()).decode("utf-8")

        message = [
                SystemMessage(
                    content=(
                        """
                            You are an information extraction assistant.  
                        You will be given OCR text (or an image-to-text output) of a "Membership Form".

                        Your task:  
                        - Extract only the fields that have been filled in the form.  
                        - If a field is blank, do not include it in the JSON.  
                        - Map the extracted values to the keys of the provided Pydantic schema.  
                        - Dates must be returned in DD/MM/YYYY format.  
                        - Numbers (age, amount_paid) should be integers/floats, not strings.  
                        - For signatures: return True if a signature is present, False if absent.  
                        - Do not add extra keys or explanations — only return the JSON object.  
                        

                        Schema fields to capture:  
                        - applicant_name  
                        - date_of_birth  
                        - age  
                        - pan_number  
                        - aadhaar_card  
                        - father_or_spouse_name  
                        - address  
                        - phone_mobile_no  
                        - email_id  
                        - occupation  
                        - nationality  
                        - nominee_name  
                        - nominee_date_of_birth  
                        - nominee_age  
                        - nominee_sex  
                        - nominee_relationship  
                        - bank_name  
                        - bank_account_no  
                        - ifsc_code  
                        - amount_paid  
                        - amount_in_words  
                        - introducer_name  
                        - introducer_code_no  
                        - introducer_signature_present  
                        - member_signature_present  
                        - official_signature_present  
                        """
                    )
                ),
                HumanMessage(
                    content=[
                        {"type": "text", "text": "Extract the filled details from this membership form."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{form_image}"}}
                    ]
                )
            ]  

        response = self.structured_model.invoke(message)

        return response.model_dump()



