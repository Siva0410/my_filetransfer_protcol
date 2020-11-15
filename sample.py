from scapy.all import *

#Taro 169.254.219.169
#Hanako 169.254.107.46
SRC_IP = '169.254.219.169'
DST_IP = '169.254.107.46'

FILE_SIZE = 102400
PKT_SIZE = 40

#read file
f = open('test.txt','rb')
txt = f.read()
f.close()

start = 0
end = FILE_SIZE/PKT_SIZE + 1

for i in range(1,41):
    #make packet
    raw = txt[start:end]
    pkt = (IP(dst=DST_IP)/ICMP(id=0x1234, sec=(i-1))/raw)
    
    #send and recv packet
    sr1(pkt)
    #--------------------------------
    #ここにパケット紛失時の処理を書く
    #--------------------------------
    #set next packet
    start = end
    end = start + FILE_SIZE/PKT_SIZE + 1
    
