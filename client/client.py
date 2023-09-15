import requests
import json
import os
import argparse

BASE_URL = "http://127.0.0.1:55000"
FILE_STORAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')

def list_files():
    response = requests.get(f"{BASE_URL}/list-files")
    
    if response.status_code == 200:
        data = response.json()  
        file_list = data["files"]  
        return file_list, response.status_code
    else:
        return None, response.status_code

def upload_files(*filenames):
    file_dict = {}
    for i, filename in enumerate(filenames, start=1):
        file_path = os.path.join(FILE_STORAGE_PATH, filename)
        file_key = f'candidate_file_{i}'
        file_dict[file_key] = open(file_path, 'rb')

    response = requests.post(f'{BASE_URL}/upload-files', files=file_dict)
    if response.status_code == 200:
        msg = response.json()['message']
        return msg, response.status_code
    else:
        msg = response.json()['error']
        return msg, response.status_code

def delete_files(*filenames):
    file_dict = {}
    for i, filename in enumerate(filenames, start=1):
        file_path = os.path.join(FILE_STORAGE_PATH, filename)
        file_key = f'candidate_file_{i}'
        file_dict[file_key] = open(file_path, 'rb')

    response = requests.post(f'{BASE_URL}/delete-files', files=file_dict)
    if response.status_code == 200:
        msg = response.json()['message']
        msg = response.json()['message']
        return msg, response.status_code
    else:
        msg = response.json()['error']
        msg = response.json()['error']
        return msg, response.status_code
    

def file_client_app():
    while True:
        print("Available commands: list, upload, delete, finish")

        user_input = input("Enter a command: ")

        if user_input == "list":
            filenames, status_code = list_files()
            if filenames is None:
                print(f"\n[FROM SERVER, ERROR]: no list of files were returned (status code: {status_code})")
            print("\n[FROM SERVER, SUCCESS] File List:")
            for filename in filenames:
                print(filename)
            print()
        
        elif user_input == "upload":
            filenames = input("Enter filenames to upload (comma-separated): ").split(',')
            filenames = [filename.strip() for filename in filenames]
            if not filenames:
                print("Please provide filenames to upload.")
            else:
                msg, status_code = upload_files(*filenames)
                if status_code == 200:
                    print(f'\n[FROM SERVER, SUCCESS({status_code})] {msg}')
                else:
                    print(f'\n[FROM SERVER, ERROR({status_code})] from server: {msg}')
            print()
        elif user_input == "delete":
            filenames = input("Enter filenames to delete (comma-separated): ").split(',')
            filenames = [filename.strip() for filename in filenames]
            if not filenames:
                print("Please provide filenames to delete.")
            else:
                msg, status_code = delete_files(*filenames)
                if status_code == 200:
                    print(f'\n[FROM SERVER, SUCCESS({status_code})] {msg}')
                else:
                    print(f'\n[FROM SERVER, ERROR({status_code})] from server: {msg}')
            print()
        elif user_input == "finish":
            print("Exiting the application.")
            break  # Exit the loop and terminate the application
        
        else:
            print("Invalid command. Please enter a valid command.")


if __name__ == "__main__":
    file_client_app()
    