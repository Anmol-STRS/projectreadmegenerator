from .customuserinput import custominput
import google.generativeai as genai
import time
from .storage import Storage
import os
from dotenv import load_dotenv

"""
Generate class has necessary functions to produce readme file
"""
class generate:
    
    def generatereadmefile():
        
        """
        Takes the Storage class and the customuserinput class
         
        """
        STORAGE = Storage
        CUSTOMER_INPUT = custominput

        """
        Load Dotenv
          
        """
        load_dotenv(dotenv_path=STORAGE.env_module_loader())
        
        
        """
        Get the API Key and the Model the user is using from the environment file and use it as it is 
        
        """
        API_KEY = os.getenv("API_KEY")
        MODEL_USING = os.getenv("MODEL")
        
        if not API_KEY or not MODEL_USING:
            """
            If key or model is not found, the function ask for the key and the model and store
            it in an environment variable  
            
            """
            print('Value not provided')
            API_KEY = API_KEY or CUSTOMER_INPUT.askfortheapikey().strip().replace(' ', '')
            MODEL_USING = MODEL_USING or CUSTOMER_INPUT.askforthemodel().strip().replace(' ', '')
            if(STORAGE.storetheapikey(API_KEY, MODEL_USING)): 
                print('ENV file is added')
        
        """
        Ask for the Project link from the user
        """    
        PROJECT_LINK = CUSTOMER_INPUT.askforprojectlinkinput()
        
        
        """
        Configure the Gemini AI with the user API_KEY
        
        """
        genai.configure(api_key=API_KEY)

        """
        Inputs the model that user wants to use in GenAI
        
        """
        try:
            model = genai.GenerativeModel(model_name=MODEL_USING)
        except Exception as e:
            raise ValueError(f"Failed to initialize the model with name '{MODEL_USING}': {e}")

        """
        Generates a response 
        """
        response = model.generate_content(f"Please generate a beautiful and step by step README FILE for the project link {PROJECT_LINK}")

        def writereadme():
            """
            Function generates Readme file based on the AI response
            """
            while True:
                try:
                    with open('README.md', 'w', encoding='utf-8') as readme_file:
                        readme_file.write(response.text)

                    with open('README.md', 'r', encoding='utf-8') as readme_file:
                        content_written = readme_file.read()
                        
                    if content_written == response.text:
                        print('Readme file is generated')
                        break
                    
                except Exception as e:
                    print("Error occurred while reading/writing the README file:", e)
                
                time.sleep(2)
        writereadme()
        
    generatereadmefile()


