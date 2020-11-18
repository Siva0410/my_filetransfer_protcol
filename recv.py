#! /usr/bin/env python3

import os, sys, time
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
FILE_NUM = int(sys.argv[2])
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


recv_list = [None for _ in range(SEC_SIZE)]
file_data = [recv_list for _ in range(FILE_NUM)]
pkt_list = [i for i in range(SEC_SIZE)]

#init
last_fileno = -1
recv_data = "" 
base_fileno = 0

for _ in range(FILE_NUM*SEC_SIZE):
    #send and recv packet
    recv_binary_data, recv_addr = udp_recv.recvfrom(PKT_SIZE)
    recv_header = recv_binary_data[:HEADER_SIZE]
    fileno, pktno = int.from_bytes(recv_header[:FILENO_SIZE], 'little'),int.from_bytes(recv_header[FILENO_SIZE:], 'little')
        
    #create new file storage
    if last_fileno < fileno:
        last_fileno = fileno
        
    #add pkt to file storage
    file_data[fileno][pktno] = recv_binary_data[HEADER_SIZE:].decode()
    
    for i in range(base_fileno,last_fileno+1):
        if None not in file_data[i]:
            for s in file_data[i]:
                recv_data += s
            print(recv_data)        
            #read file
            f = open(os.path.join(RECV_PATH, "recv"+str(i)),'w')
            #write file
            f.write(recv_data)
            #close file
            f.close()
            recv_data = ""
            base_fileno += 1
            print("[*] Write recv{} file! ".format(i))
               
    print("[*] Received Data : File {} Sec {} From {}".format(fileno, pktno, recv_addr))
    udp_send.sendto(b'ACK', DST)
        
    


