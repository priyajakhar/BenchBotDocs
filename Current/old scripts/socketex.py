import socket
import sys

IP_address = socket.gethostbyname(socket.gethostname()) # hosting IP
port = 4242 # Hosting port


# Set up a TCP/IP server
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to server address and port 81
server_address = (IP_address, port)
tcp_socket.bind(server_address)

print( 'Server bound to port: {0}\nAt IP: {1}\n'.format(port, IP_address) )
 
# Listen on port 4242
tcp_socket.listen(5)
 
while True: # Run indefinitely, accepting connections one at a time
    print("Waiting for connection...")
    connection, client = tcp_socket.accept() # Blocks the thread from progressing until a client is accepted
 
    try:
        print("Connected to client IP: {}".format(client))
         
        # Receive and handle data 512 bytes at a time, as long as the client is sending something
        while True: 
            data = connection.recv(512)
            print("\nReceived string: {}".format(data))

            # Handle the recieved data
            if 'connection_confirmation' in str(data): # Example of processing specific data differently
                print('Sending string: handshake_complete')
                connection.sendall(bytes('handshake_complete', 'utf-8')) # encode the confirmation message as utf-8 bytes and send it

            elif len(data) > 0: # Catch all, for if there is any data at all
                reply = input( 'Enter the server\'s response (to not respond, press enter with no text):\n' ) # prompt for an input to send
                if len(reply) > 0:
                    print('Sending string: {}'.format(reply))
                    connection.sendall(bytes(reply, 'utf-8')) # encode the string as utf-8 bytes and send it
            
            else:
                print('No data received.')
            
            if not data:
                break
 
    finally:
        connection.close()
        