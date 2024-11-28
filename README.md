# Socket-Programming

Project Title: Simplified File Transfer Protocol (FTP) Implementation Using Python


Authors and Contact Information:

1. Hafsa Nasir -
2. Desire Hernandez -
3. Vimal Sajeeva Doss - vimalsajeeva@csu.fullerton.edu


Programming Language:

Language Used: Python 


How to Execute the Program:

Prerequisites
1. Python Version: Ensure Python 3.x is installed on your system. You can verify by running:
python3 --version
2. Network Environment:
● Server and client should be on the same network (e.g., localhost) for testing.
● If running on different machines, ensure they can communicate over the specified
port.

Running the Server:
1. Open a terminal and navigate to the directory containing the server code
cd /path/to/server_code/
2. Start the server by running:
python3 server_FTP.py <PORT_NUMBER>
● Replace <PORT_NUMBER> with the desired port number (e.g., 6666).
● Example:
python3 server_FTP.py 6666
3. The server will output a message indicating it is listening for incoming connections:
Server listening on port 6666
Running the Client
1. Open another terminal and navigate to the directory containing the client code:
cd /path/to/client_code/
2. Start the client by running:
python3 client_FTP.py <SERVER_ADDRESS> <PORT_NUMBER>
● Replace <SERVER_ADDRESS> with the server's hostname or IP address (e.g., localhost or 127.0.0.1 for testing locally).
● Replace <PORT_NUMBER> with the port number used by the server.
● Example:
python3 client_FTP.py localhost 6666
3. The client will connect to the server and display the prompt: ftp>
Client Commands:
At the ftp> prompt, you can execute the following commands: 1. List files on the server:
ls
The server will return a list of files in its current directory.
2. Download a file from the server:
get <FILENAME>
● Replace <FILENAME> with the name of the file you want to download.
● Example:
get example.txt
3. Upload a file to the server:
put <FILENAME>
● Replace <FILENAME> with the name of the file you want to upload.
● Ensure the file exists in the client’s directory.
● Example:
put upload.txt
4. Quit the session: quit
This will close the connection and terminate the client application.
