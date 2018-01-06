import bluetooth

def start_bluetooth_service():
    server_sock=bluetooth.BluetoothSocket( bluetooth.L2CAP )

    port = 0x1001

    server_sock.bind(("",port))
    server_sock.listen(1)

    #uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ef"
    #bluetooth.advertise_service( server_sock, "SampleServerL2CAP",
    #                   service_id = uuid,
    #                   service_classes = [ uuid ]
    #                    )
                       
    client_sock,address = server_sock.accept()
    print("Accepted connection from ",address)

def run():
    # Send list with names of songs
    songs = get_list_of_songs()
    data = transform_to_correct_format(songs)
    client_sock.send(data)
    
    while True:
    
        # Wait for command from client (picking a song, scrolling, etc)
        command = client_sock.recv(1024)
        
        # Execute command
        response = execute_command(command)
        
        # Send response to command
        client_sock.send(responsedata)

    client_sock.close()
    server_sock.close()
