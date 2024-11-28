import socket
import pickle
import sys
import os

def start_client(server_name, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_name, port))  # Connecting to the specified server

    while True:
        command = input("ftp> ").strip()
        
        if not command:
            continue

        if command == "quit":
            request = {'cmd': 'quit'}
            client_socket.send(pickle.dumps(request))
            break
        
        command_parts = command.split(" ")
        #print(command_parts[0])
        if command_parts[0] == "get":
            filename = command_parts[1]
            request = {'cmd': command_parts[0], 'filename': filename}

        elif command_parts[0] == "put":
            if not os.path.isfile(command_parts[1]):
                print("[!]File doesn't exist.")
                continue
            else:
                filename = command_parts[1]
                request = {'cmd': command_parts[0], 'filename': filename}
        elif command_parts[0] == "ls":
            request = {'cmd': 'ls'}
        else:
            print("Unknown command.")
            continue

        # Serialize and send the command
        client_socket.send(pickle.dumps(request))

        # Wait for response
        response_data = client_socket.recv(4096)
        response = pickle.loads(response_data)
        #print(response)
        
        if response['status'] == 'SUCCESS':
            print(f"Success: {response['message']}")
            if 'filename' in request:
                if request['cmd'] == "get":
                    receive_file(filename, client_socket)
                elif request['cmd'] == "put":
                    send_file(filename, client_socket)
        else:
            print(f"Error: {response['message']}")

    client_socket.close()

def send_file(filename, control_socket):
    # Create a data socket and bind to an ephemeral port
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.bind(('', 0))  # Let OS choose an available ephemeral port
    data_port = data_socket.getsockname()[1]  # Get the ephemeral port number
    control_socket.send(pickle.dumps({'data_port': data_port}))  # Notify server of data port
    print("EP port sent to the server.")

    # Connect to the server on the chosen data port
    data_socket.listen(1)
    data_connection, _ = data_socket.accept()

    with open(filename, 'rb') as f:
        file_data = f.read(4096)
        while file_data:
            data_connection.send(file_data)
            file_data = f.read(4096)

    data_connection.close()

def receive_file(filename, control_socket):
    # Create a data socket and bind to an ephemeral port
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.bind(('', 0))  # Let OS choose an available ephemeral port
    data_port = data_socket.getsockname()[1]  # Get the ephemeral port number
    control_socket.send(pickle.dumps({'data_port': data_port}))  # Notify server of data port

    # Connect to the server on the chosen data port
    data_socket.listen(1)
    data_connection, _ = data_socket.accept()

    with open(filename, 'wb') as f:
        file_data = data_connection.recv(4096)
        while file_data:
            f.write(file_data)
            file_data = data_connection.recv(4096)

    data_connection.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python cli.py <server machine> <server port>")
        sys.exit(1)
    
    server_name = sys.argv[1]  # Get server name (machine)
    try:
        port = int(sys.argv[2])  # Get port number from command line
    except ValueError:
        print("Invalid port number")
        sys.exit(1)
    
    start_client(server_name, port)
