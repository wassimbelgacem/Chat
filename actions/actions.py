import os
import re
import chardet
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionHandleCVUpload(Action):
    def name(self) -> Text:
        return "action_handle_cv_upload"

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Directory where files are uploaded
        upload_directory = 'web/uploads'

        # Check if any file is uploaded
        uploaded_files = [f for f in os.listdir(upload_directory) if os.path.isfile(os.path.join(upload_directory, f))]

        if uploaded_files:
            # Get the latest uploaded file
            latest_uploaded_file = uploaded_files[-1]  # Using the last uploaded file
            file_path = os.path.join(upload_directory, latest_uploaded_file)

            if os.path.exists(file_path):
                # Extract phone number using regex
                phone_number = self.extract_phone_number(file_path)

                dispatcher.utter_message(
                    text=f"Your CV file '{latest_uploaded_file}' has been uploaded successfully! "
                         f"Thank you. Your phone number is {phone_number}")
            else:
                dispatcher.utter_message(text="Oops! Something went wrong with the CV upload. Please try again.")

        return []

    @staticmethod
    def extract_phone_number(file_path: str) -> Text:
        # Use your regex to extract the phone number from the file
        phone_regex = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
        # Detect file encoding
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())

        # Open the file with the detected encoding and error handling scheme
        with open(file_path, 'r', encoding=result['encoding'], errors='replace') as file:
            text = file.read()
            phone_numbers = phone_regex.findall(text)
            if phone_numbers:
                return phone_numbers[0]
            else:
                return "Phone number not found"



