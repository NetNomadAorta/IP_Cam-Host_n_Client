import cv2
import socket
import struct
import pickle

# Define the host and port to send the video stream
host = '192.168.1.10'  # Replace with the IP address of the receiver computer
port = 5000

# Create a socket to connect to the receiver computer
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Create a VideoCapture object to capture video from the webcam
cap = cv2.VideoCapture(0)

# Loop to capture and send video frames
while True:
    ret, frame = cap.read()

    # Convert the frame to a byte string using pickle
    data = pickle.dumps(frame)

    # Pack the byte string into a struct to send the size of the data
    message_size = struct.pack("L", len(data))

    # Send the size of the data followed by the data itself
    client_socket.sendall(message_size + data)