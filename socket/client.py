import socket   
from time import sleep
            
s = socket.socket()         
#host = socket.gethostname() 
host = '47.111.250.153'
print (host)
port = 6001 
s.connect((host, port))
s.send(b'get file')
rev_flag = 0
while True:
	'''
	data = s.recv(1024)
	rev_flag = 1
	print (str(data))
	'''
	data = s.recv(1024)
	if len(data) > 0:
		print (data)
	s.send(b'get file')
	while True:
		sleep(1)
		s.send(b'test')
	'''
	if 'file_name' in str(data) and len(data) > 0:
		print (str(data))
		rev_flag = 1
		data = []
		continue
	if rev_flag == 1 and len(data) > 0 :
		print ('start write')
		fh = open('test.txt','a')
		fh.write(str(data,encoding = 'utf8'))
		break
	'''
fh.close
s.close() 
