import importlib
import json
import os
import unicodedata as emoji
import sys # Import sys to get script path

# Global variables to hold modules once they are loaded
global gemini_module
global model
global webbrowser_module
gemini_module = None
webbrowser_module = None
model = None

# --- Define the absolute path for CONFIG_FILE in AppData ---
APPDATA_DIR = os.getenv('APPDATA')
if not APPDATA_DIR:
    print("Could not find AppData directory. Exiting.")
    sys.exit(1)
CONFIG_DIR = os.path.join(APPDATA_DIR, 'DEB')
os.makedirs(CONFIG_DIR, exist_ok=True)
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')  # Now in %APPDATA%\DEB\config.json

def load_api_key():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('api_key')
        except json.JSONDecodeError:
            print(f"Warning: {CONFIG_FILE} is corrupted. Please re-enter your API key.")
            os.remove(CONFIG_FILE) # Remove corrupted file
            return None
    return None

def save_api_key(api_key_to_save):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump({'api_key': api_key_to_save}, f)
    except IOError as e:
        print(f"Error saving API key to {CONFIG_FILE}: {e}")
        print("Please check file permissions or try running the script as administrator if this persists.")
        sys.exit(1) # Exit if cannot save config

# --- API Key Setup ---
api_key = load_api_key()

if not api_key:
    # Loop to ensure we get a valid API key or an exit command
    while True:
        user_input_key = input('Welcome to DEB! Please enter your Gemini API key, type help, or exit with x: ')
        if user_input_key.lower() == 'x':
            print("Goodbye.")
            exit()
        elif user_input_key.lower() == 'help':
            # --- Lazy Load webbrowser Here ---
            if webbrowser_module is None:
                try:
                    webbrowser_module = importlib.import_module('webbrowser')
                except ImportError:
                    print("An error occured. Please contact the developer, and include these details: The webbrowser module had an ImportError.")
                    exit() # Critical error, cannot proceed

            print('Loading...')
            webbrowser_module.open_new_tab('https://wesleymartin.net/deb-extras/get-gemini-api-key')
            print("Once you have your key, paste it here.")
            continue # Go back to the start of this while loop and ask again
        elif not user_input_key:
            print("API key cannot be empty. Please enter your key or type help or x.")
            continue
        else:
            api_key = user_input_key # A valid key was entered
            break # Exit this API key input loop

    save_api_key(api_key)
    print("API key saved! You won't be asked for it again unless the config file is deleted.")
    print('You are now ready to start using DEB.')

# --- Main Program Loop ---
while True:
    char = input('Enter an emoji. Press x to exit. Press enter after each input: ')

    if char.lower() == 'x':
        print('Goodbye.')
        exit()

    if len(char) != 1:
        print('Oops. You must enter a single character. In the future, I may introduce support for multiple emojis.')
        continue

    try:
        result = emoji.name(char)
        print('Character is', result)

        while True: # Loop for next_command
            next_command = input('Enter e to describe another emoji, or type m to learn more about the emoji. Type x to exit: ').lower()
            if next_command == 'm':
                print('Just a moment...')

                # --- Lazy Load Gemini Here ---
                if gemini_module is None:
                    try:
                        gemini_module = importlib.import_module('google.generativeai')

                        # Configure Gemini only after it's loaded
                        gemini_module.configure(api_key=api_key)

                        model = gemini_module.GenerativeModel('gemini-2.0-flash-lite')
                    except ImportError:
                        print("Error: The 'google-generativeai' module is not installed.")
                        print("Please install it using: pip install google-generativeai")
                        continue # Go back to asking for next_command
                    except Exception as config_error:
                        print(f"An error occurred while configuring Gemini API with the provided key: {config_error}. ")
                        # If API key is bad, prevent further Gemini attempts
                        # Also remove the invalid key from config.json to re-prompt
                        print("The API key might be invalid. Removing it from config.json to re-prompt.")
                        try:
                            os.remove(CONFIG_FILE)
                        except OSError as e:
                            print(f"Could not remove config file: {e}")
                        api_key = None # Clear api_key so it gets re-prompted
                        continue

                # Now that gemini_module and model are attempted to be loaded/configured
                if model: # Only proceed if model was successfully created
                    try:
                        response = model.generate_content(f'Describe to a blind person how the {char} emoji, {result}, looks, and what it means, in one sentence. If it is not an emoji, describe the shape of the character.')
                        print(response.text)
                        print('Generated by AI. May be inaccurate or offensive.')
                    except Exception as error:
                        print(f"An error occurred while communicating with the Gemini API. Please contact the developer with the following details: {error}. Do NOT include the API key.")
                        # If there's an API communication error, it's a good idea to prompt for the key again
                        print("Removing API key from config.json to re-prompt on next run.")
                        try:
                            os.remove(CONFIG_FILE)
                        except OSError as e:
                            print(f"Could not remove config file: {e}")
                        api_key = None # Clear api_key so it gets re-prompted
                else:
                    print("Gemini model could not be loaded or configured due to previous errors. Cannot describe emoji.")

                while True: # Loop for third_command
                    third_command = input('Press e to describe another emoji, or x to exit: ').lower()
                    if third_command == 'e':
                        break
                    elif third_command == 'x':
                        print('Goodbye.')
                        exit()
                    else:
                        print('Invalid command. Please enter "e" or "x".')
                break

            elif next_command == 'e':
                break
            elif next_command == 'x':
                print('Goodbye.')
                exit()
            else:
                print('Invalid command. Please enter "e", "m", or "x".')

    except ValueError:
        print('Error: Unrecognized character.')
        continue
    except Exception as error:
        print(f"An error occurred. Please contact the developer, and include these details: {error}.")
        exit()