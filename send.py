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
RECV_SIZE = 150

SLEEP_TIME = 0.0001

#get files
DATA_PATH = "./data/"
data_files = os.listdir(DATA_PATH)

udp_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_recv.bind(SRC)

for fileno, data_file in enumerate(data_files[:FILE_NUM]):
    #read file
    f = open(DATA_PATH+data_file,'rb')
    send_data = f.read()
    
    #init
    start = 0
    end = DATA_SIZE
    recv_data = ""
    raws = [None for i in range(SEC_SIZE)]
    for pktno in range(SEC_SIZE):

        #make packet
        header = fileno.to_bytes(FILENO_SIZE,'little') + pktno.to_bytes(PKTNO_SIZE,'little')
        raw = header + send_data[start:end]

        #send  packet
        udp_send.sendto(raw, DST)
        
        print("[*] Sended Data : File {} Pkt {} To {}".format(fileno, pktno, DST_IP))
        
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
    
