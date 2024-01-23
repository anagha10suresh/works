import os
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pytesseract

def detect_and_save_license_plate(image_path, result_label):
    # Read the image
    img = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if img is None:
        result_label.config(text="Error: Unable to load the image.")
        return

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load the Haar Cascade classifier
    cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

    # Check if the cascade classifier was loaded successfully
    if cascade.empty():
        result_label.config(text="Error: Unable to load the Haar Cascade XML file.")
        return

    # Detect license number plates
    plates = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))


    # Check if license plates are detected
    if len(plates) == 0:
        result_label.config(text="No license plates detected.")
        return

    # Create a folder named "result" if it doesn't exist
    result_folder = 'result'
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    # Get the current number of files in the "result" folder
    num_existing_files = len(os.listdir(result_folder))

    for i, (x, y, w, h) in enumerate(plates, 1):
        # Draw bounding rectangle around the license number plate
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Extract the region of interest (ROI) corresponding to the license plate
        gray_plate = gray[y:y+h, x:x+w]

        # Save each license plate in the "result" folder with a unique filename
        result_path = os.path.join(result_folder, f'Numberplate_{num_existing_files + i}.jpg')
        cv2.imwrite(result_path, gray_plate)

    # Display the original image with bounding boxes
    cv2.imshow('Number Plate Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Update the result label
    result_label.config(text=f"Number plates saved in '{result_folder}' folder.")

def open_file_dialog(result_label):
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
    if file_path:
        # Display the selected image in the GUI
        image = Image.open(file_path)
        image.thumbnail((400, 400))
        img_label.image = ImageTk.PhotoImage(image)
        img_label.config(image=img_label.image)

        # Perform license plate detection and save the result
        detect_and_save_license_plate(file_path, result_label)

# Create the main GUI window
root = tk.Tk()
root.title("License Plate Detection")

# Create a label to display the image
img_label = tk.Label(root)
img_label.pack(pady=10)

# Create a button to open the file dialog
upload_button = tk.Button(root, text="Upload Image", command=lambda: open_file_dialog(result_label))
upload_button.pack(pady=10)

# Create a label to display the result
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
