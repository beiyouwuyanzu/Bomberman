import socket
import json
import threading
from threading import Thread
import datetime
  
# s = socket.socket()
# s.connect(('127.0.0.1', 6666))  # 与服务器建立连接

# # 发送登录协议，请求登录
# s.sendall('{"protocol":"cli_login","username":"admin01","password":"123456"}|#|'.encode())
# # 接收服务端返回的消息
# data = s.recv(4096)
# print(data.decode())
# data = s.recv(4096)
# print(data.decode())
# input("")
# s.close()


def write_log(msg):
    cur_time = datetime.datetime.now()
    s = "[" + str(cur_time) + "]" + msg
    print(s)

class Client:

	def __init__(self, box, ip = '106.12.165.154', port = 8666 ):
		self.ip = ip 
		self.port = port 

		self.box = box
		self.s = socket.socket()
		self.s.connect((self.ip, self.port))
		self.listen()

	def send_data(self, data):
		data["protocol"] = "test"
		body = (json.dumps(data) + '|#|').encode()
		self.s.sendall(body)

	def send(self, data):
		threading.Thread(target = self.send_data, args = (data,)).start()

	def receive_data(self):
		bytes = None 
		try:
			while True:
				bytes = self.s.recv(4096)
				print(bytes.decode())
				if len(bytes) == 0:
					write_log("服务器发送数据为空, 退出")
					self.s.close()
				self.deal_data(bytes)
		except:
			self.s.close()
			raise
			write_log("数据异常， 退出")

	def deal_data(self, bytes):
		info = ""
		data = bytes.decode().split('|#|')
		if data:
			info = json.loads(data[0]).get('chat')
		if self.box:
			self.box.append_html_text("<br>" + info)

	def listen(self,):
		thread = Thread(target = self.receive_data)
		thread.setDaemon(True)
		thread.start()


if __name__ == '__main__':
	client = Client()
	data = {"key": "value"}
	data["protocol"] = "test"
	client.send(data)
	data["hahaha"] = "xixixi"
	client.send(data)
	# for i in range(10):
	# 	client.send(data)
	input("")