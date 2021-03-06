import socket   
from time import sleep
import base64
import _thread
import serial
import time
import datetime
import os

host = '106.12.40.121'
port = 2201
mountPoint = 'RTK'
userAgent = 'NTRIP Aceinna CloudRTK 1.0'
username = 'yundong'
password = 'TEL8IOZTBJVVJ0IT'
com_port = 'com34'


def get_utc_day():
	year = int(time.strftime("%Y"))
	month = int(time.strftime("%m"))
	day = int(time.strftime("%d"))
	hour = int(time.strftime("%H"))
	minute = int(time.strftime("%M"))
	second = int(time.strftime("%S"))
	local_time = datetime.datetime(year, month, day, hour, minute, second)
	time_struct = time.mktime(local_time.timetuple())
	utc_st = datetime.datetime.utcfromtimestamp(time_struct)
	d1 = datetime.datetime(year, 1, 1)
	utc_sub = utc_st - d1
	utc_str = utc_sub.__str__()
	utc_day_int = int(utc_str.split( )[0])
	utc_day_str = str(utc_day_int + 1)
	return utc_day_str
	
def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print (path+' mkdir suc')
        return True
    else:
        print ('mkdir exist')
        return False

def rev_ntrip_data(port_handle,client,is_log):
	if is_log:
		day = get_utc_day()
		try:
			mkdir(day)
		except:
			pass
		file_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
		log_file = day + '/' + 'ntrip_' + file_time +'.bin'
		fs = open(log_file,'wb')
	while True:
		rev_data = client.recv(1024)
		if(len(rev_data) > 0):
			#print('len = %s' % (len(rev_data)))
			port_handle.write(rev_data)
			if is_log:
				fs.write(rev_data)
			#print(rev_data)
		sleep(0.1)
def rev_uart_data(port_handle,client,is_log):
	if is_log:
		day = get_utc_day()
		try:
			mkdir(day)
		except:
			pass
		file_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
		log_file = day + '/' + 'sta8100_' + file_time +'.log'
		fs = open(log_file,'w')
	while True:
		data = port_handle.read_all()
		if len(data) > 0 :
			client.send(data)
			print(str(data))
			if is_log:
				fs.write(str(data))
		sleep(0.1)
def ntip_connect():
	uart_handle=serial.Serial(com_port,460800, timeout=1)
	if(uart_handle.is_open):
		print('wrong port')
	rtk_client = socket.socket()  
	rtk_client.connect((host, port))
	auth = username + ':' + password
	bytes_auth = auth.encode("utf-8")
	authorization = base64.b64encode(bytes_auth)
	#authorization = username + ':' + password
	info = "GET /%s HTTP/1.0\r\nUser-Agent: %s\r\nAuthorization: Basic %s\r\n\r\n"%(mountPoint,userAgent,authorization.decode('utf-8'))
	print ("info = %s" % info)
	
	rtk_client.send(info.encode("utf8"))
	rev_data = rtk_client.recv(1024)
	if('ICY 200 OK' in str(rev_data)):
		print ('connect ntrip suc start connect com')
		_thread.start_new_thread(rev_ntrip_data,(uart_handle,rtk_client,1,))
		_thread.start_new_thread(rev_uart_data,(uart_handle,rtk_client,1,))
	'''
	try:
		serial=serial.Serial(com_port,460800, timeout=1)
		if(serial == NULL):
			print('wrong port')
		rtk_client = socket.socket()  
		rtk_client.connect((host, port))
		auth = username + ':' + password
		bytes_auth = auth.encode("utf-8")
		authorization = base64.b64encode(bytes_auth)
		#authorization = username + ':' + password
		info = "GET /%s HTTP/1.0\r\nUser-Agent: %s\r\nAuthorization: Basic %s\r\n\r\n"%(mountPoint,userAgent,authorization.decode('utf-8'))
		print (info)
		
		rtk_client.send(info.encode("utf8"))
		rev_data = rtk_client.recv(1024)
		if('ICY 200 OK' in str(rev_data)):
			print ('connect ntrip suc start connect com')
			_thread.start_new_thread(rev_ntrip_data,(serial,rtk_client,0,))
			_thread.start_new_thread(rev_uart_data,(serial,rtk_client,0,))
	except:
		print('error')
		return
	'''
	


if __name__ == '__main__':
	ntip_connect()
	while 1:
	   pass
