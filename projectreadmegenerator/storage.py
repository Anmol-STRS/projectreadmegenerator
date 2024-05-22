class Storage:
    
    @staticmethod 
    def storetheapikey(api_key , project_model):
        content = f'API_KEY = {api_key} \nMODEL = {project_model}'
        with open('projectreadmegenerator/.env', 'w') as envfile:
            envfile.write(content)
            