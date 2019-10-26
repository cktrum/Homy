import bluetooth
import re
import os
from SongsLibrary import *

class BluetoothSrv():

    def __init__(self):
        self.port = 0x1001
        self.library = SongsLibrary()
        self.server_sock = None
        self.client_sock = None
        self.buffer_size = 1
        
    def start_bluetooth_service(self):
        
        # Make device visible
        os.system("hciconfig hci0 piscan")
    
        self.server_sock = bluetooth.BluetoothSocket( bluetooth.L2CAP )

        self.server_sock.bind(("", self.port))
        self.server_sock.listen(self.buffer_size)
        print("Listening for connections on port ", self.port)

        #uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ef"
        #bluetooth.advertise_service( server_sock, "SampleServerL2CAP",
        #                   service_id = uuid,
        #                   service_classes = [ uuid ]
        #                    )
                           
        self.client_sock, address = self.server_sock.accept()
        print("Accepted connection from ",address)
        
    def run(self):
        # TODO: implement state machine
        
        # Send list with names of songs
        print("Setup songs library")
        self.library.setup()
        songs = self.library.get_list_of_songs()
        data = self.transform_format(songs)
        
        print("Send songs to client")
        print(data)
        self.client_sock.send(data)
        
        while True:
        
            # Wait for command from client (picking a song, scrolling, etc)
            command = self.client_sock.recv(1024)
            print("Received command %s" % (command))
            
            # Execute command
            func_to_execute = self.execute_command(command)
            response = func_to_execute()
            print("response", response)
            
            if response is not None:
                # Send response to command
                self.client_sock.send("msg: " + str(response))

        self.client_sock.close()
        self.server_sock.close()
        
    def transform_format(self, songs):
        data = " "
        
        for artist, title in songs:
            song = artist + "_" + title + ";"
            data = data + song
            
        return data

    def execute_command(self, input):
        data = re.search("b'(.*)'", str(input))
        data = data.group(1)
        # extract potential arguments
        arguments = re.search("\((.*)\)", data)
        args = []
        for group in arguments.group:
            args.append(group)
         
        switcher = {
            "next_page": self.library.go_to_next_page,
            "prev_page": self.library.go_to_prev_page
            #"select_song": 
        }
        
        command = switcher.get(data, lambda: "nothing")
        return command
            

if  __name__ =='__main__':
    srv = BluetoothSrv()
    srv.start_bluetooth_service()    
    srv.run()
