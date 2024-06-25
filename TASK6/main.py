# Secret Keeper App with Biometric Authentication System Using Face Recognition

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import bcrypt
from cryptography.fernet import Fernet
import getpass

# Function to load training images and encode them for face recognition


def load_training_images(path):
    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv2.imread(os.path.join(path, cl))
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    return images, classNames

# Function to find face encodings from loaded images


def find_encodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(img)

        if len(face_locations) == 0:
            print("No faces found in the image.")
            continue

        encode = face_recognition.face_encodings(img, face_locations)[0]
        encodeList.append(encode)

    return encodeList


# Function to handle user registration and store hashed passwords


def register_user():
    print("\n🚀 Welcome to the Exiting Secret Keeper App - Registration")
    username = input("Enter username: ")

    if check_duplicate_username(username):
        print("\n❌ Oops! That username is already taken. Please choose a different one.")
        return

    password = getpass.getpass("Enter password: ")
    while len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
        print("\n❌ Password should be at least 8 characters long and contain both letters and numbers.")
        password = getpass.getpass("Enter password: ")

    first_name = input("Enter your First Name: ")
    last_name = input("Enter your Last Name: ")
    age = input("Enter your Age: ")
    email = input("Enter your Email Address: ")

    # Capture user images
    capture_user_images(username)

    salt = bcrypt.gensalt()
    password_hash = hash_password(password, salt)
    save_user_to_file(username, salt.decode(
        'utf-8'), password_hash.decode('utf-8'), first_name, last_name, age, email)
    print("\n✅ Registration successful! You're now registered in the Exiting Secret Keeper App.")

    print("\n🌟 You are now ready to use the system for secure authentication.")

# Function to capture and save user images


def capture_user_images(username):
    # Create a directory for user images if it doesn't exist
    user_photos_dir = 'data/User_Photos'
    if not os.path.exists(user_photos_dir):
        os.makedirs(user_photos_dir)

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Failed to open webcam")
        return

    print("\n📸 Please look at the camera and press 's' to capture your image.")

    count = 0
    while True:
        success, img = cap.read()
        if not success:
            print("Error: Failed to capture frame")
            break

        cv2.imshow('Camera', img)
        key = cv2.waitKey(1)

        if key == ord('s'):
            count += 1
            img_name = f"{username}_{count}.jpg"
            img_path = os.path.join(user_photos_dir, img_name)
            cv2.imwrite(img_path, img)
            print(f"✅ Image {count} captured and saved.")

        elif key == ord('q') or count >= 1:  # Press 'q' to quit or capture 5 images
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to log in existing users and validate credentials


def login_user():
    print("\n🔐 User Login")
    username = input("Enter username: ").lower()

    with open("data/users.txt", "r") as user_file:
        lines = user_file.readlines()
        for line in lines:
            data = line.strip().split(",")
            if len(data) == 7:
                stored_username, stored_salt, stored_password_hash, first_name, last_name, age, email = data
                if username == stored_username.lower():
                    entered_password = getpass.getpass("Enter password: ")

                    entered_password_hash = hash_password(
                        entered_password, stored_salt).decode('utf-8')
                    if entered_password_hash == stored_password_hash:
                        print(
                            "\n🔐 Password verified. Please look at the camera for biometric verification.")
                        if biometric_verification(username):
                            print(
                                "\n🎉 Login successful! Welcome back, {}.".format(first_name))
                            return username
                        else:
                            print(
                                "\n❌ Biometric verification failed. Login aborted.")
                            return None
                    else:
                        print("\n❌ Incorrect password. Login failed.")
                        return None

        print("\n❌ Oops! Username not found. Please check your credentials and try again.")
        return None

# Function to perform biometric verification using face recognition


def biometric_verification(username):
    path = 'data/User_Photos'  # Path to user photos directory
    images, classNames = load_training_images(path)
    encodeListKnown = find_encodings(images)

    if not encodeListKnown:
        print("Error: No face encodings found.")
        return False

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Failed to open webcam")
        return False

    while True:
        success, img = cap.read()
        if not success:
            print("Error: Failed to capture frame")
            break

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(
                encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(
                encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2),
                              (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                cv2.imshow('Webcam', img)
                cv2.waitKey(5000)  # Display matched user for 3 seconds
                cap.release()
                cv2.destroyAllWindows()
                return True

        # cv2.imshow('Webcam', img)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cap.release()
    cv2.destroyAllWindows()
    return False

# Function to greet the user upon successful login


def greet_user(first_name):
    if first_name.lower() != "user":
        print("\n🎉 Welcome back, {}! You're ready to authenticate.".format(first_name))

# Function to handle user interactions after login, including face recognition and secret management


def user_interaction(username, images, classNames, encodeListKnown):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Failed to open webcam")
        return

    while True:
        success, img = cap.read()
        if not success:
            print("Error: Failed to capture frame")
            break

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(
                encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(
                encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2),
                              (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                cap.release()
                cv2.destroyAllWindows()

                while True:
                    print("\n🔒 Secret Management Menu:")
                    print("1. Add a Secret")
                    print("2. View Secrets")
                    print("3. Delete a Secret")
                    print("4. Logout")

                    choice = input("Enter your choice (1-4): ")

                    if choice == "1":
                        add_secret_to_user(username)

                    elif choice == "2":
                        view_user_secrets(username)

                    elif choice == "3":
                        delete_user_secret(username)

                    elif choice == "4":
                        print("\n👋 Logging out...")
                        return

                    else:
                        print(
                            "\n❌ Invalid choice. Please enter a number between 1 and 4.")

            else:
                print("\n❌ Biometric verification failed.")
                return

        # cv2.imshow('Webcam', img)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # cap.release()
    # cv2.destroyAllWindows()

# Function to add a secret to the user's encrypted file


def add_secret_to_user(username):
    secret = input("\nEnter the secret you want to add: ")
    key, encrypted_secret = encrypt_secret(secret)
    add_secret_to_file(username, key, encrypted_secret)

# Function to view the user's decrypted secrets


def view_user_secrets(username):
    secrets = get_user_secrets(username)
    if secrets:
        print("\n🔐 Your Decrypted Secrets:")
        for index, secret in enumerate(secrets, start=1):
            print(f"{index}. {secret}")
    else:
        print("\n❌ No secrets found for this user.")

# Function to delete a user's specific secret


def delete_user_secret(username):
    secrets = get_user_secrets(username)
    if secrets:
        print("\n🔒 Your Secrets:")
        for index, secret in enumerate(secrets, start=1):
            print(f"{index}. {secret}")

        choice_index = int(
            input("\nEnter the number of the secret you want to delete (1, 2, ...): ")) - 1
        if 0 <= choice_index < len(secrets):
            delete_secret_from_file(username, secrets[choice_index].strip())
            print("\n✅ Secret deleted successfully!")
        else:
            print("\n❌ Invalid choice. Please enter a valid number.")
    else:
        print("\n❌ No secrets found.")

# Function to initialize necessary directories and files


def initialize_project():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("data/User_Photos"):
        os.makedirs("data/User_Photos")

# Function to hash password using bcrypt


def hash_password(password, salt):
    password_bytes = password.encode('utf-8')
    salt_bytes = salt if isinstance(salt, bytes) else salt.encode('utf-8')
    return bcrypt.hashpw(password_bytes, salt_bytes)

# Function to check if username already exists


def check_duplicate_username(username):
    with open("data/users.txt", "r") as user_file:
        lines = user_file.readlines()
        existing_usernames = [line.split(",")[0].lower() for line in lines]
    return username.lower() in existing_usernames

# Function to save user data to users.txt file


def save_user_to_file(username, salt, password_hash, first_name, last_name, age, email):
    with open("data/users.txt", "a") as user_file:
        user_file.write(
            f"{username},{salt},{password_hash},{first_name},{last_name},{age},{email}\n")

# Function to encrypt secret using Fernet


def encrypt_secret(secret):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_secret = cipher_suite.encrypt(secret.encode('utf-8'))
    print("\n🔒 Secret encrypted successfully!")
    return key, encrypted_secret

# Function to decrypt secret using Fernet


def decrypt_secret(key, encrypted_secret):
    cipher_suite = Fernet(key)
    decrypted_secret = cipher_suite.decrypt(encrypted_secret)
    return decrypted_secret.decode('utf-8')

# Function to add encrypted secret to user's secrets file


def add_secret_to_file(username, key, encrypted_secret):
    with open(f"data/{username}_secrets.txt", "a") as secrets_file:
        secrets_file.write(
            f"{key.decode('utf-8')},{encrypted_secret.decode('utf-8')}\n")

# Function to retrieve and decrypt user's secrets from secrets file


def get_user_secrets(username):
    secrets_list = []
    secrets_file_path = f"data/{username}_secrets.txt"
    if os.path.exists(secrets_file_path):
        with open(secrets_file_path, "r") as secrets_file:
            lines = secrets_file.readlines()
            for line in lines:
                key, encrypted_secret = line.strip().split(",")
                decrypted_secret = decrypt_secret(key.encode(
                    'utf-8'), encrypted_secret.encode('utf-8'))
                secrets_list.append(decrypted_secret)
    return secrets_list

# Function to delete a specific secret from user's secrets file


def delete_secret_from_file(username, secret):
    secrets_file_path = f"data/{username}_secrets.txt"
    if os.path.exists(secrets_file_path):
        with open(secrets_file_path, "r") as secrets_file:
            lines = secrets_file.readlines()

        with open(secrets_file_path, "w") as secrets_file:
            for line in lines:
                decrypted_secret = decrypt_secret(
                    line.strip().split(",")[0], line.strip().split(",")[1])
                if secret != decrypted_secret:
                    secrets_file.write(line)

# Function to delete user account and move data to deleted users file


def delete_user_account(username):
    with open("data/users.txt", "r") as user_file:
        lines = user_file.readlines()

    with open("data/users.txt", "w") as user_file:
        for line in lines:
            data = line.strip().split(",")
            stored_username = data[0]

            if username != stored_username.lower():
                user_file.write(line)

    with open("data/deleted_users.txt", "a") as deleted_users_file:
        deleted_users_file.write(",".join(data) + "\n")

    user_folder_path = f"data/{username}_secrets.txt"
    if os.path.exists(user_folder_path):
        os.remove(user_folder_path)

# Main function to orchestrate the biometric authentication system


def main():
    initialize_project()  # Initialize necessary directories and files

    path = 'data/User_Photos'  # Update path to user photos directory
    images, classNames = load_training_images(path)
    # print("Loaded images:", classNames)

    encodeListKnown = find_encodings(images)
    if not encodeListKnown:
        print("Error: No face encodings found.")
        return
    # print('Encoding Complete')

    while True:
        print("\n🚀 Secret Keeper App")
        print("1. Register User\n2. Login\n3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            register_user()

        elif choice == "2":
            username = login_user()
            if username:
                greet_user("User")
                user_interaction(username, images, classNames, encodeListKnown)

        elif choice == "3":
            print("\n👋 Exiting Secret Keeper App...")
            break

        else:
            print("\n❌ Invalid choice. Please enter a number between 1 and 3.")


# Entry point of the script
if __name__ == "__main__":
    main()
