import os
from scapy.all import *

#Taro 169.254.219.169
#Hanako 169.254.107.46
SRC_IP = 'localhost'
SRC_PORT = 10000
DST_IP = 'localhost'
DST_PORT = 10001

#header
IP_HEADER = IP(dst=DST_IP, src=SRC_IP)
TCP_HEADER = TCP(dport=DST_PORT, sport=SRC_PORT)

#file size
FILE_SIZE = 102400
DATA_SIZE = 51200

#get files
DATA_PATH = "./data/"
data_files = os.listdir(DATA_PATH)

for data_file in data_files:
    #read file
    f = open("./data/"+data_file,'rb')
    data = f.read()
    
    #init
    start = 0
    end = FILE_SIZE//DATA_SIZE + 1
    
    for i in range(FILE_SIZE//DATA_SIZE):
        #make packet
        raw = data[start:end]
        pkt = IP_HEADER/TCP_HEADER/raw
        
        #send and recv packet
        sr(pkt)
        #sr1(pkt)
        #--------------------------------
        #ここにパケット紛失時の処理を書く
        #-------------------------------- 
        #set next packet
        start = end
        end = start + FILE_SIZE//DATA_SIZE + 1
        
    #close file
    f.close()    
    
