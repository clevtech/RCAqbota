import socket
import time
import sys
import select
import termios
import tty
import sys


settings = termios.tcgetattr(sys.stdin)


def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


host = '0.0.0.0'
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .
"""


connected = False
print("Connecting")
print(msg)

while True:
    if not connected:
        try:
            s.connect((host, port))
            print("Server connected")
            connected = True
        except:
            pass
    else:
        while 1:
            try:
                key = getKey()
                if key == '\x03':
                    sys.exit()
                s.sendall(str(key).encode('utf-8'))
                msg = s.recv(1024)
                print(str(msg.decode('utf-8')))
            except:
                print("Server not connected")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connected = False
                break

s.close()
