import socket
import json
import time
import random
import sys

# Server connection details
SERVER_IP = "127.0.0.1"  # Same as your server IP
SERVER_PORT = 8889       # Same as your server PORT

# Device information
DEVICE_ID = "ESP32-Sensor1"  # You can change this or make it configurable

def generate_random_data():
    """Generate random sensor data"""
    return {
        "Device": DEVICE_ID,
        "IP": "192.168.1.100",
        "LUX": round(random.uniform(100.0, 500.0), 2),
        "NH3": round(random.uniform(5.0, 20.0), 2),
        "HS": round(random.uniform(30.0, 350.0), 2),
        "H": round(random.uniform(50.0, 90.0), 2),
        "T": round(random.uniform(18.0, 35.0), 2)
    }

def connect_and_send_data():
    """Connect to the server and send random sensor data"""
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        print(f"Connecting to server at {SERVER_IP}:{SERVER_PORT}...")
        client_socket.connect((SERVER_IP, SERVER_PORT))
        
        # Wait for server request
        data = client_socket.recv(1024)
        if data == b"a":
            print("Received request from server")
            
            # Generate random sensor data
            sensor_data = generate_random_data()
            print(f"Generated sensor data: {sensor_data}")
            
            # Convert to JSON and send
            json_data = json.dumps(sensor_data)
            client_socket.sendall(json_data.encode())
            print("Data sent successfully")
            
        # Close the connection
        client_socket.close()
        return True
        
    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Main function to run the client"""
    print("Sensor Client Started")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            success = connect_and_send_data()
            if success:
                # Wait before sending next data
                wait_time = random.randint(5, 15)  # Random wait between 5-15 seconds
                print(f"Waiting {wait_time} seconds before sending next data...")
                time.sleep(wait_time)
            else:
                # If connection failed, wait a bit longer before retrying
                print("Retrying in 10 seconds...")
                time.sleep(10)
    except KeyboardInterrupt:
        print("\nClient stopped by user")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()