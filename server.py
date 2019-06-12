#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()

print('connected:', addr)

while 1:
    try:
        key = getKey()
        if key == '\x03':
            sys.exit()
        conn.sendall(str(key).encode('utf-8'))
    except:
        break

conn.close()
