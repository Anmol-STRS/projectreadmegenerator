import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import projectreadmegenerator

projectreadmegenerator = projectreadmegenerator

class TestGenerateReadme(unittest.TestCase):

    @patch('projectreadmegenerator.Storage')
    @patch('projectreadmegenerator.custominput')
    @patch('projectreadmegenerator.load_dotenv')
    @patch('os.getenv')
    @patch('google.generativeai.GenerativeModel')
    def test_generatereadmefile_env_vars_loaded(self, mock_model, mock_getenv, mock_load_dotenv, mock_custominput, mock_storage):
        # Mock environment variables
        mock_getenv.side_effect = lambda key: 'A13413413jajdasdasd' if key == 'API_KEY' else 'gemini-1.5'
        
        # Mock storage and custom input methods
        mock_storage_instance = MagicMock()
        mock_custominput_instance = MagicMock()
        mock_storage.return_value = mock_storage_instance
        mock_custominput.return_value = mock_custominput_instance

        # Mock the AI model
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance
        mock_model_instance.generate_content.return_value.text = "Generated README content"
        
        with patch('builtins.open', mock_open()) as mocked_file:
            # Run the function
            from projectreadmegenerator import generate
            generate.generatereadmefile()

            # Assertions to check if the necessary methods were called
            mock_load_dotenv.assert_called()
            mock_getenv.assert_any_call('API_KEY')
            mock_getenv.assert_any_call('MODEL')
            mock_model_instance.generate_content.assert_called_once_with("Please generate a beautiful and step by step README FILE for the project link None")
            mocked_file.assert_called_with('README.md', 'w', encoding='utf-8')

    @patch('projectreadmegenerator.Storage')
    @patch('projectreadmegenerator.custominput')
    @patch('projectreadmegenerator.load_dotenv')
    @patch('os.getenv')
    @patch('google.generativeai.GenerativeModel')
    def test_generatereadmefile_missing_env_vars(self, mock_model, mock_getenv, mock_load_dotenv, mock_custominput, mock_storage):
        # Simulate missing environment variables
        mock_getenv.side_effect = lambda key: None
        
        # Mock storage and custom input methods
        mock_storage_instance = MagicMock()
        mock_custominput_instance = MagicMock()
        mock_storage.return_value = mock_storage_instance
        mock_custominput.return_value = mock_custominput_instance
        mock_custominput_instance.askfortheapikey.return_value = "input_api_key"
        mock_custominput_instance.askforthemodel.return_value = "input_model_name"

        # Mock the AI model
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance
        mock_model_instance.generate_content.return_value.text = "Generated README content"
        
        with patch('builtins.open', mock_open()) as mocked_file:
            # Run the function
            from projectreadmegenerator import generate
            generate.generatereadmefile()

            # Assertions to check if the necessary methods were called
            mock_load_dotenv.assert_called()
            mock_custominput_instance.askfortheapikey.assert_called()
            mock_custominput_instance.askforthemodel.assert_called()
            mock_storage_instance.storetheapikey.assert_called_with("input_api_key", "input_model_name")
            mock_model_instance.generate_content.assert_called_once_with("Please generate a beautiful and step by step README FILE for the project link None")
            mocked_file.assert_called_with('README.md', 'w', encoding='utf-8')

    @patch('projectreadmegenerator.Storage')
    @patch('projectreadmegenerator.custominput')
    @patch('projectreadmegenerator.load_dotenv')
    @patch('os.getenv')
    @patch('google.generativeai.GenerativeModel')
    def test_generatereadmefile_model_initialization_failure(self, mock_model, mock_getenv, mock_load_dotenv, mock_custominput, mock_storage):
        # Mock environment variables
        mock_getenv.side_effect = lambda key: 'fake_api_key' if key == 'API_KEY' else 'fake_model_name'
        
        # Mock storage and custom input methods
        mock_storage_instance = MagicMock()
        mock_custominput_instance = MagicMock()
        mock_storage.return_value = mock_storage_instance
        mock_custominput.return_value = mock_custominput_instance

        # Simulate model initialization failure
        mock_model.side_effect = Exception("Model initialization failed")
        
        with self.assertRaises(ValueError) as context:
            from projectreadmegenerator import generate
            generate.generatereadmefile()
        
        self.assertIn("Failed to initialize the model with name 'fake_model_name'", str(context.exception))

    @patch('projectreadmegenerator.Storage')
    @patch('projectreadmegenerator.custominput')
    @patch('projectreadmegenerator.load_dotenv')
    @patch('os.getenv')
    @patch('google.generativeai.GenerativeModel')
    @patch('builtins.open', new_callable=mock_open)
    def test_generatereadmefile_writing_file(self, mock_file, mock_model, mock_getenv, mock_load_dotenv, mock_custominput, mock_storage):
        # Mock environment variables
        mock_getenv.side_effect = lambda key: 'fake_api_key' if key == 'API_KEY' else 'fake_model_name'
        
        # Mock storage and custom input methods
        mock_storage_instance = MagicMock()
        mock_custominput_instance = MagicMock()
        mock_storage.return_value = mock_storage_instance
        mock_custominput.return_value = mock_custominput_instance

        # Mock the AI model
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance
        mock_model_instance.generate_content.return_value.text = "Generated README content"
        
        # Mock the open function
        mock_file_instance = mock_file.return_value
        mock_file_instance.read.return_value = "Generated README content"

        from projectreadmegenerator import generate
        generate.generatereadmefile()

        # Check that the file write and read calls were made correctly
        mock_file.assert_any_call('README.md', 'w', encoding='utf-8')
        mock_file.assert_any_call('README.md', 'r', encoding='utf-8')
        mock_file_instance.write.assert_called_once_with("Generated README content")
        mock_file_instance.read.assert_called_once()

    # Additional test cases can include:
    # - Simulating network failures when contacting the Generative AI model
    # - Handling different responses from the Generative AI model
    # - Testing the delay and retry mechanism for writing the README file
    # - Verifying the correct handling of user input for project links
    # - Ensuring proper storage of the API key and model name in the environment file

# Run the tests
if __name__ == '__main__':
    unittest.main()
