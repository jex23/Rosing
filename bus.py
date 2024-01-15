import cv2
from PIL import Image, ImageTk
import tkinter as tk
import os
import time
import serial

# Serial connection setup
ser = serial.Serial('COM40', 9600, timeout=1)  # Change 'COM1' to the correct port your Arduino/ESP8266 is connected to

# Functions for relay control
def set_relay_d0_high():
    ser.write(b'H')  # Send command to turn on relay connected to D0
    print("Relay on pin D0 turned ON")

def set_relay_d0_off():
    ser.write(b'L')  # Send command to turn off relay connected to D0
    print("Relay on pin D0 turned OFF")

def set_relay_d1_high():
    ser.write(b'I')  # Send command to turn on relay connected to D1
    print("Relay on pin D1 turned ON")

def set_relay_d1_off():
    ser.write(b'O')  # Send command to turn off relay connected to D1
    print("Relay on pin D1 turned OFF")

def update_frame():
    global running
    ret, frame = cap.read()

    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Resize the frame
        frame = cv2.resize(frame, (1280, 720)) 
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=img)

        # Update the image on the panel
        panel.img = img
        panel.config(image=img)

    if running:
        update_elapsed_time()

    # Call update_frame function after 10 milliseconds
    root.after(10, update_frame)

def update_elapsed_time():
    # Implement your logic for updating elapsed time here
    pass

def capture_frame_periodic():
    if running:
        ret, frame = cap.read()
        if ret:
            folder_name = time.strftime("%B-%d-%Y", time.localtime())  # Month-Date-Year format

            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            time_label = time.strftime("%I_%M_%S_%p", time.localtime())
            img_name = os.path.join(folder_name, f'{time_label}.jpg')
            cv2.imwrite(img_name, frame)
            print(f"Frame captured and saved: {img_name}")

        # Schedule the function to be called again after 30 seconds
        root.after(30000, capture_frame_periodic)

def toggle_capture():
    global running
    if running:
        capture_button.config(text="Capture every 30 seconds Off")
        running = False
        set_relay_d1_off()
    else:
        capture_button.config(text="Capture every 30 seconds On")
        running = True
        # Call the function to start periodic capture
        capture_frame_periodic()
        set_relay_d1_high()

# Create the main Tkinter window
root = tk.Tk()
root.title("Webcam Viewer")

# Open the webcam using OpenCV with the provided RTSP video source
cap = cv2.VideoCapture("rtsp://admin:BicolUni2020@192.168.1.64:554/Streaming/Channels/101")

# Set the dimensions of the window
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Create a panel to display the video frames
panel = tk.Label(root)
panel.pack(padx=10, pady=10)

# Create a capture button
capture_button = tk.Button(root, text="Capture every 30 seconds Off", command=toggle_capture)
capture_button.pack(pady=10)

# Initialize the running variable
running = False

# Start updating the frame
update_frame()

# Run the Tkinter event loop
root.mainloop()

# Release the video capture object
cap.release()
