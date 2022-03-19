import re
import socket
from _thread import *


server = "192.168.56.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((server, port))
	
except socket.error as e:
	str(e)

def read_pos(st):
		st = st.split(",")
		return (int(st[0]), int(st[1]))  
	   
def make_pos(tup):
	return str(tup[0]) + "," + str(tup[1]) 

starting_pos = [(0, 0), (1, 0), (2, 0), (3, 0)]
pos = [(0, 0), (100, 0), ()]   
'''
1. send a starting pos on grid level
	send ID
2. recieve real pos


'''
s.listen(4)
print("Waiting for connection.. Server started")

def threaded_client(conn, player):
	send_data(conn, make_pos(starting_pos[player]))
	data = read_data(conn)
	pos[player] = make_pos(data)
	while True:
		data = read_and_reply(conn, (player == 1 and make_pos(pos[0]) or make_pos(pos[1])))
		pos[player] = read_pos(data)
		
 
def read_and_reply(conn, reply):
	try:
		data = conn.recv(2048).decode()
		if not data:
			print("Disconnected")
			return ""

		conn.sendall(str.encode(reply))
		return data
	except:
		print("Error while receiving and sending")
		return ""

def read_data(conn):
	try:
		data = conn.recv(2048).decode()
		if not data:
			print("Disconnected")
			return ""
		return data
	except:
		print("Error reading_data")
		return ""

def send_data(conn, data):
	try:
		conn.sendall(str.encode(data))
	except:
		print("Error sending data")
  

current_player = 0
while True:
	conn, addr = s.accept()
	print("Connected to: ",addr)
	
	start_new_thread(threaded_client, (conn, current_player))
	current_player += 1
 
