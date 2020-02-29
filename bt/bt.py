import sys
import bluetooth

class BT:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        self.sock.connect((self.address, self.port))

    def send(self,msg):
        self.sock.send(msg)

    def kill(self):
        self.sock.close()

if __name__ == '__main__':
    bt_connection = BT("00:18:E5:04:0B:6B",1)
    bt_connection.send("1,1,1,1\n")