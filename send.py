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

SRC_PORT = 10000
DST_PORT = 10001

#file size
FILE_SIZE = 102400
SEC_SIZE = 100
DATA_SIZE = FILE_SIZE//SEC_SIZE
SLEEP_TIME = 0.01

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

    for i in range(SEC_SIZE):
        #make packet
        raw = data[start:end]
        print(data_file,i,len(raw))

        #send and recv packet
        tcp_client.send(raw)
        tcp_client.recv(10)
        time.sleep(SLEEP_TIME)
#        response = tcp_client.recv(DATA_SIZE)
#        print(response)

        #--------------------------------
        #ここにパケット紛失時の処理を書く
        #-------------------------------- 
        #set next packet
        start = end
        end = start + DATA_SIZE
        
    #close file
    f.close()    
    


