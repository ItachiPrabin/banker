import cv2
import pytesseract
from PIL import Image
import json
import os

# Set the tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path as per your installation

def capture_image(save_directory):
    # Open a connection to the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return None

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the frame
        cv2.imshow('Press "c" to capture or "q" to quit', frame)

        # Wait for user input
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            # If 'c' is pressed, capture the image
            image_path = os.path.join(save_directory, 'captured_image.jpg')
            cv2.imwrite(image_path, frame)
            print("Image saved as", image_path)
            cap.release()
            cv2.destroyAllWindows()
            return image_path
        elif key == ord('q'):
            # If 'q' is pressed, quit the process
            print("Image capture canceled")
            cap.release()
            cv2.destroyAllWindows()
            return None

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
        "Birth Place", "Permanent Address", "VDC", "Ward No", "Certificate No"
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

def main():
    # Directory to save the captured image
    save_directory = "X:\\Banking Robo\\extracted_information"
    
    # Ensure the directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    image_path = capture_image(save_directory)
    if image_path:
        extracted_text = extract_text_from_image(image_path)
        print("Extracted Text:\n", extracted_text)

        # Filter the relevant text
        relevant_text = filter_relevant_text(extracted_text)
        print("Relevant Text:\n", "\n".join(relevant_text))

        # Save the relevant text to JSON
        save_text_to_json(relevant_text, save_directory, "extracted_text.json")

if __name__ == "__main__":
    main()
