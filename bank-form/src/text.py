import pytesseract
from PIL import Image
import cv2
import os
import re
import json
import firebase_admin
from firebase_admin import credentials, db

# Path to your service account key file
cred = credentials.Certificate("C:/Users/Acer/Downloads/bankrobo-39d68-firebase-adminsdk-td3d1-de9fe68d6a.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://bankrobo-39d68-default-rtdb.firebaseio.com'
})

# Set the path to the Tesseract executable
tesseract_path = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_path

def correct_image_orientation(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    try:
        osd = pytesseract.image_to_osd(gray)
        angle = int(re.search(r'(?<=Rotate: )\d+', osd).group(0))

        if angle != 0:
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, -angle, 1.0)
            rotated = cv2.warpAffine(image, M, (w, h))
        else:
            rotated = image

    except pytesseract.TesseractError as e:
        print(f"Tesseract OSD Error: {e}")
        rotated = image

    # Save the corrected image
    corrected_image_path = 'corrected_' + os.path.basename(image_path)
    cv2.imwrite(corrected_image_path, rotated)
    return corrected_image_path

def extract_text(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    # Correct the image orientation
    corrected_image_path = correct_image_orientation(image_path)
    
    image = Image.open(corrected_image_path)
    image = image.convert('RGB')
    image.save(corrected_image_path, dpi=(300, 300))
    
    # Perform OCR on the image
    try:
        text = pytesseract.image_to_string(image, lang='eng+nep')
    except pytesseract.TesseractError as e:
        print(f"Tesseract OCR Error: {e}")
        text = ""

    return text

def filter_relevant_text(text):
    # Keywords to identify relevant lines
    keywords = ["Citizenship Certificate No", "Sex", "Full Name", "Date of Birth", "Birth Place", "Permanent Address", "VDC", "Ward No", "Certificate No"]

    # Filter lines containing the keywords
    relevant_lines = [line for line in text.split('\n') if any(keyword in line for keyword in keywords)]
    
    return relevant_lines

def parse_relevant_text(relevant_lines):
    # Initialize a dictionary to store the parsed data
    data = {
        "birth_place": {},
        "permanent_address": {}
    }

    # Debug: Print relevant lines
    print("Relevant Lines:")
    for line in relevant_lines:
        print(line)
    
    # Correct and parse the certificate number
    for line in relevant_lines:
        if re.search(r'Certificate\sNo[:\s]+\S+', line) or re.search(r'riueate\s\S+.\s(\S+)', line):
            certificate_number_match = re.search(r'Certificate\sNo[:\s]+\S+', line) or re.search(r'riueate\s\S+.\s(\S+)', line)
            if certificate_number_match:
                data['certificate_number'] = certificate_number_match.group(0).split(':')[-1].strip()
                print(f"Certificate Number Found: {data['certificate_number']}")
                break  # Assuming only one certificate number line is present

    # Parse the rest of the data
    for line in relevant_lines:
        if "Full Name" in line:
            parts = line.split(": ")
            if len(parts) > 1:
                data['full_name'] = parts[1].strip()
        elif "Date of Birth" in line:
            dob_parts = re.search(r'Year\s*:?(\d{4})\s*Month\s*:?(\w+)\s*Day\s*:?(\d+)', line)
            if dob_parts:
                year, month, day = dob_parts.groups()
                data['date_of_birth'] = f"{year}-{month}-{int(day):02d}"
        elif "Birth Place" in line:
            if "District" in line:
                parts = line.split(": ")
                if len(parts) > 1:
                    data['birth_place']['district'] = parts[1].strip()
        elif "Permanent Address" in line:
            if "District" in line:
                parts = line.split(": ")
                if len(parts) > 1:
                    data['permanent_address']['district'] = parts[1].strip()
        elif "VDC" in line:
            parts = line.split(": ")
            if len(parts) > 1:
                data['birth_place']['vdc'] = parts[1].strip()
        elif "Municipality" in line:
            parts = line.split(": ")
            if len(parts) > 1:
                data['municipality'] = parts[1].strip()
        elif "Ward No" in line:
            ward_no_match = re.search(r'Ward No[:\s]+(\d+)', line)
            if ward_no_match:
                ward_no = ward_no_match.group(1)
                if 'birth_place' in data:
                    data['birth_place']['ward_no'] = ward_no
                else:
                    data['municipality_ward_no'] = ward_no
        elif "Sex" in line:
            gender_match = re.search(r'Sex[:\s]+(\w+)', line)
            if gender_match:
                gender = gender_match.group(1).lower()
                if gender == "make":
                    gender = "male"
                elif gender == "femate":
                    gender = "female"
                data['gender'] = gender
    
    # Remove empty fields
    data = {k: v for k, v in data.items() if v}

    return data

def save_extracted_info(filename, relevant_lines, parsed_data):
    folder_path = os.path.dirname(filename)
    os.makedirs(folder_path, exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump({
            "Relevant Text": relevant_lines,
            "Parsed Data": parsed_data
        }, file, indent=4, ensure_ascii=False)

def generate_output_filename(full_name, output_dir):
    sanitized_name = re.sub(r'\W+', '_', full_name)  # Replace non-alphanumeric characters with underscores
    unique_filename = f"{sanitized_name}.json"
    full_path = os.path.join(output_dir, unique_filename)
    
    counter = 1
    while os.path.exists(full_path):
        unique_filename = f"{sanitized_name}_{counter}.json"
        full_path = os.path.join(output_dir, unique_filename)
        counter += 1
    
    return full_path

def main(image_path, output_dir):
    text = extract_text(image_path)
    print("Extracted Text:\n", text)  # Log the extracted text for debugging
    
    # Filter relevant lines
    relevant_lines = filter_relevant_text(text)
    
    # Correct relevant lines
    corrected_lines = correct_relevant_lines(relevant_lines)
    
    # Parse relevant text into structured data
    parsed_data = parse_relevant_text(corrected_lines)
    
    # Generate a unique output filename based on the full name
    if 'full_name' in parsed_data:
        output_file = generate_output_filename(parsed_data['full_name'], output_dir)
    else:
        output_file = generate_output_filename("Unknown_Name", output_dir)
    
    # Save the filtered lines and parsed data into a JSON file
    save_extracted_info(output_file, relevant_lines, corrected_lines, parsed_data)
    print(f"Extracted information saved to {output_file}")
    

def save_to_firebase(parsed_data):
    ref = db.reference('extracted_data')
    new_entry_ref = ref.push()
    new_entry_ref.set(parsed_data)

def main(image_path, output_file):
    text = extract_text(image_path)
    print("Extracted Text:\n", text)  # Log the extracted text for debugging
    
    # Filter relevant lines
    relevant_lines = filter_relevant_text(text)
    
    # Parse relevant text into structured data
    parsed_data = parse_relevant_text(relevant_lines)
    
    # Save the filtered lines and parsed data into a JSON file
    save_extracted_info(output_file, relevant_lines, parsed_data)
    print(f"Extracted information saved to {output_file}")
    
    # Save parsed data to Firebase Realtime Database
    save_to_firebase(parsed_data)
    print("Extracted information saved to Firebase Realtime Database")

if __name__ == "__main__":
    # Specify the local image path and output file
    image_path = 'X:/nigga.jpg'


    output_file = 'X:/Banking Robo/extracted_information/extracted_information.json'
    
    
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    main(image_path, output_file)
