import userinput
import google.generativeai as genai
import time
import storage
import os
from dotenv import load_dotenv

STORAGE = storage.Storage
CUSTOMER_INPUT = userinput.customuserinput

load_dotenv()

API_KEY = os.getenv("API_KEY")
MODEL_USING = os.getenv("MODEL")

if not API_KEY:
    API_KEY = CUSTOMER_INPUT.askfortheapikey()

if not MODEL_USING:
    MODEL_USING = CUSTOMER_INPUT.askforthemodel()

PROJECT_LINK = CUSTOMER_INPUT.askforprojectlinkinput()

if not API_KEY or not MODEL_USING:
    STORAGE.storetheapikey(API_KEY, MODEL_USING)
    raise ValueError("API key and model must be provided.")


genai.configure(api_key=API_KEY)

try:
    model = genai.GenerativeModel(model_name=MODEL_USING)
except Exception as e:
    raise ValueError(f"Failed to initialize the model with name '{MODEL_USING}': {e}")

response = model.generate_content(f"Please generate a beautiful and step by step README FILE for the project link {PROJECT_LINK}")

def generateReadmefile():
    while True:
        try:
            print(response.text)
            with open('README.md', 'w', encoding='utf-8') as readme_file:
                readme_file.write(response.text)

            with open('README.md', 'r', encoding='utf-8') as readme_file:
                content_written = readme_file.read()
                
            if content_written == response.text:
                break
            
        except Exception as e:
            print("Error occurred while reading/writing the README file:", e)
        
        time.sleep(1)

generateReadmefile()
