import socket
import os
import pickle
import sys
import subprocess
import time

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))  # Binding to localhost
    server_socket.listen(1)
    

    while True:
        time.sleep(0.5)
        print(f"Server listening on port {port}")
        print("-" * 50)
        print("[*]Waiting for connection")
        control_socket, addr = server_socket.accept()
        
        print(f"    [*] Connection from {addr}")

        while True:
            # Receive command from the client
            command_data = control_socket.recv(4096)
            if not command_data:
                break  # Client closed the connection
            command = pickle.loads(command_data)
            if command['cmd'] == "quit":
                print("     [*]Client disconnected.")
                break
            elif command['cmd'] == "get":
                filename = command['filename']
                send_file(filename, control_socket)
            elif command['cmd'] == "put":
                filename = command['filename']
                receive_file(filename, control_socket)
            elif command['cmd'] == "ls":
                list_files(control_socket)
            if command['cmd'] == "quit":
                print("     [*]Client disconnected.")
                break
        
        control_socket.close()

def send_file(filename, control_socket):
    if not os.path.isfile(filename):
        response = {'status': 'FAIL', 'message': f"{filename} not found"}
        print("     [*]GET Failed")
        control_socket.send(pickle.dumps(response))
        return
    
    response = {'status': 'SUCCESS', 'message': f"Sending file: {filename}"}
    print("     [*]GET Success")
    control_socket.send(pickle.dumps(response))

    # Wait for client to send the ephemeral port for data connection
    data_socket = accept_data_connection(control_socket)

    with open(filename, 'rb') as f:
        file_data = f.read(4096)
        while file_data:
            data_socket.send(file_data)
            file_data = f.read(4096)
            

    data_socket.close()

def receive_file(filename, control_socket):
    response = {'status': 'SUCCESS', 'message': f"Receiving file: {filename}"}
    print("     [*]PUT Success")
    control_socket.send(pickle.dumps(response))
    # Wait for client to send the ephemeral port for data connection
    data_socket = accept_data_connection(control_socket)

    with open(filename, 'wb') as f:
        file_data = data_socket.recv(4096)
        while file_data:
            f.write(file_data)
            file_data = data_socket.recv(4096)
            
    data_socket.close()

def list_files(control_socket):
    command = "ls"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    response = result.stdout
    type(response)
    response = {'status': 'SUCCESS', 'message': ''.join(response)}
    print("     [*]'ls' Success")
    control_socket.send(pickle.dumps(response))

def accept_data_connection(control_socket):
    # Receive the ephemeral port number for data connection from client
    data_port_data = control_socket.recv(4096)
    data_port = pickle.loads(data_port_data)['data_port']

    # Create data connection on the port provided by the client
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect(('localhost', data_port))
    return data_socket

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python serv.py <PORTNUMBER>")
        sys.exit(1)
    
    try:
        port = int(sys.argv[1])  # Get port number from command line
    except ValueError:
        print("Invalid port number")
        sys.exit(1)
    
    start_server(port)
