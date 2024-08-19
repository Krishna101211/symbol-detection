# Import the necessary modules
import json
import requests
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os

# Define a function capture_image() to capture an image from the camera using 
# OpenCV and save it as "camera_image.png
def capture_image():
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    if ret:
        cv2.imwrite("camera_image.png", frame)
        capture.release()

# Define a function detect_logo() to detect logos in the captured
# image using the Eden AI Logo Detection API
def detect_logo():
    file_path = "camera_image.png"
    # api key
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTViZjNjNWItMWRiNi00OGUzLWE3ZmQtMDQzNTBlZGZhYTFiIiwidHlwZSI6ImFwaV90b2tlbiJ9.w4_VHKrdBnJ4ldzRiqqDlaUHIlEAAjwtIZTh0ZaSPyI"
    }

    url = "https://api.edenai.run/v2/image/logo_detection"
    data = {
        "providers": "google",
        "country": "in"  # Specify country as India
    }
    files = {"file": open(file_path, "rb")}

    response = requests.post(url, data=data, files=files, headers=headers)
    result = json.loads(response.text)

    display_result(file_path, result)

    # Delete the captured image file
    os.remove(file_path)

#  Define a function display_result() to create a new window
# using tkinter (Toplevel) to display the logo detection result.
# It creates a label to display the JSON response (result) and 
# another label to display the captured image. 
def display_result(file_path, result):
    window = tk.Toplevel()
    window.title("Logo Detection Result")

    # Create a label to display the result
    result_label = tk.Label(window, text=json.dumps(result, indent=4), justify="left", font=("Courier", 10))
    result_label.pack(padx=10, pady=10)

    # Load and display the image
    image = Image.open(file_path)
    image.thumbnail((400, 400))
    image_tk = ImageTk.PhotoImage(image)
    image_label = tk.Label(window, image=image_tk)
    image_label.image = image_tk  # Keep a reference to avoid garbage collection
    image_label.pack(padx=10, pady=10)

# Define a function reset() to delete the captured image 
# file if it exists and restart the video frame update.
def reset():
    # Delete the captured image file if it exists
    file_path = "camera_image.png"
    if os.path.exists(file_path):
        os.remove(file_path)

    # Restart video frame update
    update_video_frame()

# Define a function reset() to delete the captured image
# file if it exists and restart the video frame update.
def update_video_frame():
    _, frame = capture.read()
    if frame is not None:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (400, 400))
        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(image=img)
        video_frame.img_tk = img_tk
        video_frame.config(image=img_tk)
        video_frame.after(10, update_video_frame)

# Define a function exit_program() to destroy the
# main tkinter window and exit the program.
def exit_program():
    root.destroy()


# Create the main tkinter window using Tk().
# Set the title as "Logo Detection GUI".
root = tk.Tk()
root.title("Logo Detection GUI")

# Create a label (video_frame) in the main window 
# to display the video stream from the camera.
video_frame = tk.Label(root)
video_frame.pack(padx=10, pady=10)

# Create a button (capture_button) to capture an image from the camera when clicked. 
# The capture_image() function is called when the button is pressed.
capture_button = tk.Button(root, text="Capture Image", command=capture_image)
capture_button.pack(padx=10, pady=10)

# Create a button (detect_button) to detect logos in the captured image when clicked. 
# The detect_logo() function is called when the button is pressed.
detect_button = tk.Button(root, text="Detect Logo", command=detect_logo)
detect_button.pack(padx=10, pady=10)

# Create a button (reset_button) to reset the program by deleting 
# the captured image file (if it exists) and restarting the video frame update. 
# The reset() function is called when the button is pressed
reset_button = tk.Button(root, text="Reset", command=reset)
reset_button.pack(padx=10, pady=10)

# Create an exit button (exit_button) to exit the program. 
# The exit_program() function is called when the button is pressed
exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.pack(padx=10, pady=10)

# Initialize video capture using cv2.VideoCapture(0) 
# to capture frames from the default camera
capture = cv2.VideoCapture(0)

# Start updating the video frame by calling the update_video_frame() function.
update_video_frame()

# Run the main event loop using root.mainloop(), which continuously
# listens for events and updates the GUI accordingly.
root.mainloop()
