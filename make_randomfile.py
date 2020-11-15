f = open('test.txt', 'w')

f.write('A'*1024*100) #100kB
f.close()
