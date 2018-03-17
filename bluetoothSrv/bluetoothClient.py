import sys
import bluetooth

if sys.version < '3':
    input = raw_input

sock=bluetooth.BluetoothSocket(bluetooth.L2CAP)

if len(sys.argv) < 2:
    bt_addr="B8:27:EB:ED:EA:FA"
else:
    bt_addr=sys.argv[1]
    
port = 0x1001

print("trying to connect to %s on port %d" % (bt_addr, port))

sock.connect((bt_addr, port))

print("connected")

while True:
    data = input()
    if(len(data) == 0): break
    print("data being send: ", data)
    sock.send(data)
    data = sock.recv(1024)
    print("Data received:", str(data))

sock.close()