from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
from typing import Dict
import os
from .details import Membership_Form
from ImageProcessing.processor import ImageProcessor

load_dotenv()

class MembershipFormExtractor:

    def __init__(self, form) -> None:
        self.form = form
        self.model = AzureChatOpenAI(
            deployment_name='gpt-5-mini',  # Use your actual deployment name
            api_version="2024-08-01-preview",
            azure_endpoint=os.getenv("OPENAI_API_BASE"),
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.structured_model = self.model.with_structured_output(Membership_Form)

    def read_form(self) -> Dict:
        '''
        Function to read and extract the extract output of the Form and return the JSON
        '''
        if self.form:
            # Preprocess the form image for better OCR accuracy
            form_processed_bytes = ImageProcessor.preprocess_form_image(self.form)
            
            # Encode to base64
            form_image = ImageProcessor.encode_to_base64(form_processed_bytes)

        message = [
                SystemMessage(
                    content=(
                        """
                            You are an information extraction assistant.  
                        You will be given an image of a "Membership Form" that has been preprocessed for optimal OCR.

                        Your task:  
                        - Extract only the fields that have been filled in the form.  
                        - If a field is blank, do not include it in the JSON.  
                        - Map the extracted values to the keys of the provided Pydantic schema.  
                        - Dates must be returned in DD/MM/YYYY format.  
                        - Numbers (age, amount_paid) should be integers/floats, not strings.  
                        - For signatures: return True if a signature is present, False if absent.  
                        - Do not add extra keys or explanations — only return the JSON object.  
                        - Pay special attention to handwritten entries as they may appear bolder due to preprocessing.

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
                        {"type": "text", "text": "Extract the filled details from this preprocessed membership form."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{form_image}"}}
                    ]
                )
            ]  

        response = self.structured_model.invoke(message)
        return response.model_dump()