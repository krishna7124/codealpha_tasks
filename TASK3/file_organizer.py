""" 
Task 3 - FILE ORGANIZER
Hey there! I have build a script that organizes files in a directory based on their types,
like images, documents, videos, etc. I'll be using the os and shutil libraries for file manipulation.
"""

import os
import shutil


def organize_files(directory):
    # Dictionary mapping file types to their respective directories
    file_types = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        'Documents': ['.txt', '.doc', '.docx', '.pdf', '.xlsx', '.xls', '.ppt'],
        'Videos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv'],
        'Audios': ['.mp3', '.wav', '.flac', '.aac',],
        'Archives': ['.zip', '.rar', '.tar',],
        'Executables': ['.exe', '.msi']
    }

    # Step 1: Create directories for each main category
    for main_category in file_types.keys():
        # Create directory for the main category if it doesn't exist
        main_category_dir = os.path.join(directory, main_category)
        os.makedirs(main_category_dir, exist_ok=True)

    # Step 2: Create 'Other' directory to store files not falling into any specified category
    other_dir = os.path.join(directory, 'Other')
    os.makedirs(other_dir, exist_ok=True)

    # Step 3: Organize files
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            # Get the file extension
            file_extension = os.path.splitext(file)[1]
            found = False
            # Iterate through each main category to find the appropriate directory for the file
            for main_category, extensions in file_types.items():
                if file_extension in extensions:
                    # Move the file to the corresponding directory based on its extension
                    shutil.move(file_path, os.path.join(
                        directory, main_category, file))
                    found = True
                    break
            if not found:
                # If file extension not found in main categories, move the file to 'Other' directory
                other_file_type_dir = os.path.join(
                    other_dir, file_extension[1:])
                os.makedirs(other_file_type_dir, exist_ok=True)
                shutil.move(file_path, os.path.join(other_file_type_dir, file))


# Entry point of the script
if __name__ == "__main__":
    try:
        # Replace 'directory_path' with the path of the directory you want to organize
        directory_path = 'data'
        organize_files(directory_path)
        print("Files organized successfully!")
    except Exception as e:
        # Print any error that occurs during the execution of the script
        print(f"Error occurred: {e}")
