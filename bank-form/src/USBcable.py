import os
import subprocess
import pytesseract
from PIL import Image
import json
import firebase_admin
from firebase_admin import credentials, db

# Set the tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path as per your installation

# Path to your service account key file
cred = credentials.Certificate("C:/Users/Acer/Downloads/bankrobo-39d68-firebase-adminsdk-td3d1-de9fe68d6a.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://bankrobo-39d68-default-rtdb.firebaseio.com'
})

def capture_image(save_directory):
    # Ensure the save directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Define paths
    #remote_image_path = "/sdcard/captured_image.png"
    local_image_path = os.path.join(save_directory, "captured_image.png")

    # Capture screenshot using ADB
    #subprocess.run(["adb", "exec-out", "screencap", "-p", remote_image_path])

    # Pull the image from the device to the local machine
    subprocess.run(["adb", "pull", local_image_path])

    print(f"Image saved as {local_image_path}")
    return local_image_path

def extract_text_from_image(image_path):
    # Open the image file
    img = Image.open(image_path)

    # Use pytesseract to extract text
    text = pytesseract.image_to_string(img)

    return text

def filter_relevant_text(text):
    # Keywords to identify relevant lines
    keywords = [
        "Citizenship Certificate No", "Sex", "Full Name", "Date of Birth", 
        "Birth Place", "Permanent Address", "VDC", "Ward No",
    ]

    # Filter lines containing the keywords
    relevant_lines = [line for line in text.split('\n') if any(keyword in line for keyword in keywords)]
    
    return relevant_lines

def save_text_to_json(text, directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)

    data = {'extracted_text': text}
    filepath = os.path.join(directory, filename)

    with open(filepath, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"Extracted text saved to {filepath}")

def save_to_firebase(text):
    ref = db.reference('extracted_data')
    latest_ref = ref.child('latest')
    latest_ref.set({'extracted_text': text})

    new_entry_ref = ref.push()
    new_entry_ref.set({'extracted_text': text})

def main():
    # Directory to save the captured image
    save_directory = "X:\\Banking Robo\\extracted_information"
    
    # Capture image using mobile device via USB
    image_path = capture_image(save_directory)
    if image_path:
        extracted_text = extract_text_from_image(image_path)
        print("Extracted Text:\n", extracted_text)

        # Filter the relevant text
        relevant_text = filter_relevant_text(extracted_text)
        print("Relevant Text:\n", "\n".join(relevant_text))

        # Save the relevant text to JSON
        save_text_to_json(relevant_text, save_directory, "extracted_text.json")

        # Save the extracted text to Firebase
        save_to_firebase(relevant_text)
        print("Extracted information saved to Firebase Realtime Database")

if __name__ == "__main__":
    main()
