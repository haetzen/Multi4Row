import threading, sys, socket
from client import Client
from tkinter import * 
import tkinter as tk
from urllib.request import urlopen
import re

from funks import Funks

class Main:
	def __init__(self):
     
		print(f"Ip: {self.get_ip()}")
		self.tink = tk.Tk()
		self.tink.title("Select_Gamemode")
		self.tink.geometry("200x100")
		self.b1 = tk.Button(self.tink, text = "Host Game", command = self.host)
		self.b2 = tk.Button(self.tink, text = "Join Game", command = self.connect)
		self.b1.grid(row = 0, column = 0)
		self.b2.grid(row = 1, column = 0)
		
		self.tink.mainloop()
	
	def connect(self):
		threading.Thread(target = self.open_tk_connect, args = ()).start()
	
	def host(self):
		threading.Thread(target = self.open_tk_host, args = ()).start()
	
	def open_tk_connect(self):
		self.tink2 = tk.Tk()
		self.tink2.title("Connect")
		self.tink2.geometry("300x100")
		self.tink2.resizable(False, False)
		tk.Label(self.tink2, text="Ip: ").grid(row = 0)
		tk.Label(self.tink2, text ="Port: ").grid(row = 1)
		self.e1 = tk.Entry(self.tink2)
		self.e2 = tk.Entry(self.tink2)
  
		self.e1.insert(0, "192.168.56.1")
		self.e2.insert(0, "5555")

		self.e1.grid(row = 0, column = 1)
		self.e2.grid(row = 1, column = 1)
  
		self.b1 = tk.Button(self.tink2, text = "Ok", command = self.read_boxes_connect)
		self.b1.grid(row = 1, column = 2)
		
		self.tink2.mainloop()

		
	
	def read_boxes_connect(self):
		ip = self.e1.get()
		port = int(self.e2.get())
		#print(f"ip: {ip}, port: {port}")
		self.c = threading.Thread(target=Client, args = (False, ip, port, )).start()
		sys.exit()
 
	def open_tk_host(self):
		self.tink3 = tk.Tk()
		self.tink3.title("Host")
		self.tink3.geometry("300x100")
		self.tink3.resizable(False, False)
		
		tk.Label(self.tink3, text="Ip: ").grid(row = 0)
		tk.Label(self.tink3, text ="Port: ").grid(row = 1)
		tk.Label(self.tink3, text = "Players(2-4): ").grid(row = 2)
		self.e1 = tk.Entry(self.tink3)
		self.e2 = tk.Entry(self.tink3)
		self.e3 = tk.Entry(self.tink3)
  
		self.e1.insert(0, str(self.get_ip()))
		self.e2.insert(0, "5555")
		self.e3.insert(0, "2")
		
		self.e1.grid(row = 0, column = 1)
		self.e2.grid(row = 1, column = 1)
		self.e3.grid(row = 2, column = 1)
		self.b1 = tk.Button(self.tink3, text = "Ok", command = self.read_boxes_host)
		self.b1.grid(row = 3, column = 2)
		self.tink3.mainloop()
		
	
	def read_boxes_host(self):
		ip = str(self.e1.get())
		port = int(self.e2.get())
		players = int(self.e3.get())
		#print(f"ip: {ip}, port: {port}, players: {players}")
		self.c = threading.Thread(target=Client, args = (True, ip, port, players, )).start()
		sys.exit()
	
	
	def getPublicIp(seöf):
		data = str(urlopen('http://checkip.dyndns.com/').read())
		# data = '<html><head><title>Current IP Check</title></head><body>Current IP Address: 65.96.168.198</body></html>\r\n'

		return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)

	def get_ip(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
		local_ip_address = s.getsockname()[0]
		return local_ip_address
	
if __name__ == '__main__':
	Main()