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

SRC_PORT = 10000
DST_PORT = 10001

#file size
FILE_SIZE = 102400
DATA_SIZE = 51200

#get files
DATA_PATH = "./data/"
data_files = os.listdir(DATA_PATH)

tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        print(data_file,i,len(raw))
        #print(raw_)
        #pkt = IP_HEADER/UDP_HEADER/raw_
        #print(raw(pkt))
        #send and recv packet
        #send(pkt)
        #sr1(pkt)
        tcp_client.send(raw)
        tcp_client.recv(10)
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
    


