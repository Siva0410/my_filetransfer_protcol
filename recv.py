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


SRC_PORT = 50001
DST_PORT = 50000

SRC = (SRC_IP, SRC_PORT)
DST = (DST_IP, DST_PORT)

#header
FILENO_SIZE = 2
PKTNO_SIZE = 1
HEADER_SIZE = FILENO_SIZE + PKTNO_SIZE

#file size
FILE_SIZE = 102400
SEC_SIZE = 100
DATA_SIZE = FILE_SIZE//SEC_SIZE
PKT_SIZE = FILE_SIZE//SEC_SIZE + HEADER_SIZE

#get files
RECV_PATH = "./recv/"
os.makedirs(RECV_PATH, exist_ok=True)

#udp_recv 
udp_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_recv.bind(SRC)

#udp_send
udp_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(int(sys.argv[2])):
    #read file
    f = open(os.path.join(RECV_PATH, "recv"+str(i)),'w')
    
    #init
    recv_data = ""
    
    for j in range(SEC_SIZE):
        #send and recv packet
        recv_binary_data, recv_addr = udp_recv.recvfrom(PKT_SIZE)
        recv_header = recv_binary_data[:HEADER_SIZE]
        fileno, pktno = int.from_bytes(recv_header[:FILENO_SIZE], 'little'),int.from_bytes(recv_header[FILENO_SIZE:], 'little')
        recv_data = recv_data + recv_binary_data[HEADER_SIZE:].decode()
        
        print("[*] Received Data : File {} Sec {} From {}".format(fileno, pktno, recv_addr))
        udp_send.sendto(b'ACK', DST)
        
    #write file
    f.write(recv_data)
    #close file
    f.close()


