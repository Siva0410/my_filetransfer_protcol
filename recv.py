import os
import socket
#from scapy.all import *

#Taro 169.254.219.169
#Hanako 169.254.107.46
SRC_IP = 'localhost'
SRC_PORT = 10001
DST_IP = 'localhost'
DST_PORT = 10000

LISTEN = 5
#header
# IP_HEADER = IP(dst=DST_IP, src=SRC_IP)
# TCP_HEADER = TCP(dport=DST_PORT, sport=SRC_PORT)
# UDP_HEADER = UDP(dport=DST_PORT, sport=SRC_PORT)

#file size
FILE_SIZE = 102400
DATA_SIZE = 51200

#get files
DATA_PATH = "./data/"

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind((SRC_IP, SRC_PORT))
tcp_server.listen(LISTEN)
client,address = tcp_server.accept()
print("[*] Connected!! [ Source : {}]".format(address))

for i in range(1):
    #read file
    f = open(DATA_PATH+"data"+str(i),'w')
    
    #init
    start = 0
    end = DATA_SIZE + 1
    data = ""
    for i in range(FILE_SIZE//DATA_SIZE):
        #send and recv packet
        data = data + client.recv(DATA_SIZE).decode()
        print("[*] Received Data : {}".format(data))
        # --------------------------------
        # ここにパケット紛失時の処理を書く
        # -------------------------------- 
        #set next packet
        start = end
        end = start + DATA_SIZE + 1
        
        
    f.write(data)
    #close file
    f.close()


client.close()
