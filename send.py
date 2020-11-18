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

SRC_PORT = 50000
DST_PORT = 50001

SRC = (SRC_IP, SRC_PORT)
DST = (DST_IP, DST_PORT)

#file size
FILE_SIZE = 102400
SEC_SIZE = 100
HEAD_SIZE = 2+1
DATA_SIZE = FILE_SIZE//SEC_SIZE
PKT_SIZE = FILE_SIZE//SEC_SIZE + HEAD_SIZE
RECV_SIZE = 150

SLEEP_TIME = 0.0001

#get files
DATA_PATH = "./data/"
data_files = os.listdir(DATA_PATH)

udp_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_recv.bind(SRC)

for i, data_file in enumerate(data_files[:int(sys.argv[2])]):
    #read file
    f = open(DATA_PATH+data_file,'rb')
    send_data = f.read()
    
    #init
    start = 0
    end = DATA_SIZE
    recv_data = ""
    for j in range(SEC_SIZE):
        #make packet
        header = (i).to_bytes(2,'little') + j.to_bytes(1,'little')
        print(len(header))
        raw = header + send_data[start:end]
        print(data_file,j,len(raw))

        #send  packet
        udp_send.sendto(raw, DST)

        #recv packet
        recv_binary_data, recv_addr = udp_recv.recvfrom(RECV_SIZE)
        recv_data = recv_binary_data.decode()
        print("[*] Received Data : Recv {} From {}".format(recv_data,recv_addr))

        #time.sleep(SLEEP_TIME)

        #set next packet
        start = end
        end = start + DATA_SIZE
        
    #close file
    f.close()    
    
