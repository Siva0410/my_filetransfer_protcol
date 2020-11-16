#! /usr/bin/env python3

import os
import socket
#from scapy.all import *

#Taro 169.254.219.169
#Hanako 169.254.107.46
SRC_IP = 'localhost'
SRC_PORT = 10000
DST_IP = 'localhost'
DST_PORT = 10001

#file size
FILE_SIZE = 102400
DATA_SIZE = 51200

#get files
DATA_PATH = "./data/"
data_files = os.listdir(DATA_PATH)

#header
# IP_HEADER = IP(dst=DST_IP, src=SRC_IP)
# TCP_HEADER = TCP(dport=DST_PORT, sport=SRC_PORT)
# UDP_HEADER = UDP(dport=DST_PORT, sport=SRC_PORT)

tcp_client =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect((DST_IP, DST_PORT))



    
for data_file in data_files:
    #read file
    f = open(DATA_PATH+data_file,'rb')
    data = f.read()
    
    #init
    start = 0
    end = DATA_SIZE

    for i in range(FILE_SIZE//DATA_SIZE):
        #make packet
        raw = data[start:end]
        print(len(raw))
        #print(raw_)
        #pkt = IP_HEADER/UDP_HEADER/raw_
        #print(raw(pkt))
        #send and recv packet
        #send(pkt)
        #sr1(pkt)
        tcp_client.send(raw)

#        response = tcp_client.recv(DATA_SIZE)
 #       print(response)

        #--------------------------------
        #ここにパケット紛失時の処理を書く
        #-------------------------------- 
        #set next packet
        start = end
        end = start + DATA_SIZE
        
    #close file
    f.close()    
    


