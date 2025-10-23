from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os
from .details import Aadhaar_Details
from ImageProcessing.processor import ImageProcessor

load_dotenv()

class AadhaarExtractor:
    '''
    This class is for OCR extraction from Aadhaar Cards
    '''
    def __init__(self, user_aadhaar_image_front, user_aadhaar_image_back) -> None:
        self.model = AzureChatOpenAI(
            deployment_name='gpt-5-mini',  # Use your actual deployment name
            api_version="2024-08-01-preview",
            azure_endpoint=os.getenv("OPENAI_API_BASE"),
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.structured_model = self.model.with_structured_output(Aadhaar_Details)
        self.user_aadhaar_image_front = user_aadhaar_image_front
        self.user_aadhaar_image_back = user_aadhaar_image_back

    def read_aadhaar(self) -> dict:
        if self.user_aadhaar_image_front and self.user_aadhaar_image_back:
            # Preprocess both images for better OCR
            front_processed_bytes = ImageProcessor.preprocess_aadhaar_image(self.user_aadhaar_image_front)
            back_processed_bytes = ImageProcessor.preprocess_aadhaar_image(self.user_aadhaar_image_back)
            
            # Encode to base64
            front_image = ImageProcessor.encode_to_base64(front_processed_bytes)
            back_image = ImageProcessor.encode_to_base64(back_processed_bytes)

            # Messages
            message = [
                SystemMessage(
                    content=(
                        """
                            You are an expert OCR system specialized in extracting information from Indian Aadhaar cards. Please analyze this image and extract ALL visible information in the exact JSON format specified below.

                            Extract the following information from this Aadhaar card image:

                            {
                            "aadhaar_number": "extract the 12-digit Aadhaar number (without spaces/hyphens or extra characters)",
                            "name": "full name of the cardholder",
                            "father_husband_name": "father's or husband's name if visible",
                            "date_of_birth": "date of birth in DD/MM/YYYY format",
                            "gender": ["Male", "Female", "Transgender"],
                            "address": "complete address including house number, street, area, city, state",
                            "pincode": "pincode",
                            "issue_date": "issue date if visible",
                            }

                            IMPORTANT INSTRUCTIONS:
                            - Extract ONLY information that is clearly visible and readable
                            - Use "null" for any field that is not visible or unclear
                            - Ensure the Aadhaar number is exactly 12 digits
                            - Maintain exact spelling and formatting as shown on the card
                            - For address, include all visible components in proper sequence
                            - Double-check all extracted numbers for accuracy
                            - If text is partially obscured or unclear, mark as "partially_visible: [what you can see]"

                            Return ONLY the JSON response, no additional text or explanation.
                        """
                    )
                ),
                HumanMessage(
                    content=[
                        {"type": "text", "text": "Extract the text from these Aadhaar images."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{front_image}"}},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{back_image}"}}
                    ]
                )
            ]    

            response = self.structured_model.invoke(message)
            return response.model_dump()