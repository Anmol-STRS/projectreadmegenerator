import userinput
import google.generativeai as genai

CUSTOMER_INPUT = userinput.customuserinput

PROJECT_LINK = CUSTOMER_INPUT.askforprojectlinkinput() 
API_KEY = CUSTOMER_INPUT.askfortheapikey()
MODEL_USING = CUSTOMER_INPUT.askforthemodel()

"""
CONFIGURING THE MODEL FROM THE GEMINI

"""
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name= MODEL_USING)
RESPONSE = model.generate_content(f"Please generate a beautiful and step by step README FILE for the project link {PROJECT_LINK}")


def generateReadmefile():
    with open('README.md', 'w') as readme_file:
        readme_file.write(RESPONSE.text)
        
        
generateReadmefile()