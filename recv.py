#! /usr/bin/env python3

import os, sys
import socket

Taro = '192.168.3.201'
Hanako = '192.168.3.14'

if sys.argv[1] == 'Taro':
    SRC_IP = Taro
    DST_IP = Hanako
elif sys.argv[1] == 'Hanako':
    SRC_IP = Hanako
    DST_IP = Taro
elif sys.argv[1] == 'local':
    SRC_IP = 'localhost'
    DST_IP = 'localhost'


SRC_PORT = 10001
DST_PORT = 10000

LISTEN = 5

#file size
FILE_SIZE = 102400
DATA_SIZE = 51200

#get files
RECV_PATH = "./recv/"
os.makedirs(RECV_PATH, exist_ok=True)

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind((SRC_IP, SRC_PORT))
tcp_server.listen(LISTEN)
conn, address = tcp_server.accept()
print("[*] Connected!! [ Source : {}]".format(address))

for i in range(int(sys.argv[2])):
    #read file
    f = open(os.path.join(RECV_PATH, "recv"+str(i)),'w')
    
    #init
    start = 0
    end = DATA_SIZE + 1
    data = ""
    for i in range(FILE_SIZE//DATA_SIZE):
        #send and recv packet
        data = data + conn.recv(DATA_SIZE).decode()
        print("[*] Received Data : {}".format(data))
        conn.send(b'ACK')
        # --------------------------------
        # ここにパケット紛失時の処理を書く
        # -------------------------------- 
        #set next packet
        start = end
        end = start + DATA_SIZE + 1
        
        
    f.write(data)
    #close file
    f.close()


conn.close()
