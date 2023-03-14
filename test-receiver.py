import cv2
import socket
import struct
import pickle

# Define the host and port to receive the video stream
host = '192.168.1.7'
port = 5000

# Create a socket to listen for the video stream
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(0)

# Accept the connection from the sender computer
connection, address = server_socket.accept()

# Loop to receive and display video frames
while True:
    # Receive the size of the data
    data = b""
    message_size = struct.calcsize("L")
    while len(data) < message_size:
        packet = connection.recv(message_size - len(data))
        if not packet:
            break
        data += packet
    if not packet:
        break

    # Unpack the size of the data from the struct
    message_size = struct.unpack("L", data)[0]

    # Receive the data itself and convert it back to a frame
    data = b""
    while len(data) < message_size:
        packet = connection.recv(message_size - len(data))
        if not packet:
            break
        data += packet
    if not packet:
        break
    frame = pickle.loads(data)

    # Display the frame
    cv2.imshow('Video Stream', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
connection.close()
server_socket.close()
cv2.destroyAllWindows()