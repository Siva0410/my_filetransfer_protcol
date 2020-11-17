#! /usr/bin/env python3

import os, sys
import socket

Taro = '169.254.155.219'
Hanako = '169.254.229.153'

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

SRC = (SRC_IP, SRC_PORT)
DST = (DST_IP, DST_PORT)

#file size
FILE_SIZE = 102400
SEC_SIZE = 100
DATA_SIZE = FILE_SIZE//SEC_SIZE
RECV_SIZE = DATA_SIZE

#get files
RECV_PATH = "./recv/"
os.makedirs(RECV_PATH, exist_ok=True)

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(SRC)


#print("[*] Connected!! [ Source : {}]".format(address))

for i in range(int(sys.argv[2])):
    #read file
    f = open(os.path.join(RECV_PATH, "recv"+str(i)),'w')
    
    #init
    start = 0
    end = DATA_SIZE + 1
    data = ""
    for j in range(SEC_SIZE):
        #send and recv packet
        recv_data, addr = udp_server.recvfrom(RECV_SIZE)
        data = data + recv_data.decode()
        print("[*] Received Data : File {} Sec {} From {}".format(i,j,addr))
#        conn.send(b'ACK')
        # --------------------------------
        # ここにパケット紛失時の処理を書く
        # -------------------------------- 
        #set next packet
        start = end
        end = start + DATA_SIZE + 1
        
        
    f.write(data)
    #close file
    f.close()


