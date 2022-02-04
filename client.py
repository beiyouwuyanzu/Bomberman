import socket
import json
import threading
from threading import Thread
import datetime
import uuid
from player import Player

  
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

"""
设计要发的协议:
每秒发送10次, 但是每秒刷新60次。 所以要用一个缓存来存取当前一段时间的信息
需要发送的状态包括:
	1. 人物的位置
	2. 人物的朝向
	3. 人物是否处于移动状态
	4. 人物放置的糖泡位置

	{
		"protocol": "player_status",
		"uid": "xxxxx",
		"direct": 0\1\2\3,
		"movement": 0\1,
		"bombs": [],
	}
"""
def write_log(msg):
    cur_time = datetime.datetime.now()
    s = "[" + str(cur_time) + "]" + msg
    print(s)

class Client:

	online_players = []
	TILE_SIZE = 1
	# def __init__(self, box, ip = '106.12.165.154', port = 8666 ):
	def __init__(self, box, ip = '127.0.0.1', port = 8666 ):
		self.ip = ip 
		self.port = port 
		self.box = box
		self.s = socket.socket()
		self.s.connect((self.ip, self.port))
		self.listen()

	def send_data(self, data):
		if "protocol" not in data:
			data["protocol"] = "test"
		body = (json.dumps(data) + '|#|').encode()
		try:
			self.s.sendall(body)
		except:
			self.box.append_html_text("<br>" + "send text failed")

	def send(self, data):
		threading.Thread(target = self.send_data, args = (data,)).start()

	def receive_data(self):
		bytes = None 
		try:
			while True:
				bytes = self.s.recv(4096)
				# print(bytes.decode())
				if len(bytes) == 0:
					write_log("服务器发送数据为空, 退出")
					self.s.close()
				try:
					self.deal_data(bytes)
				except:
					Server.write_log("deal_data failed:" + bytes.decode())
		except:
			self.s.close()
			raise
			write_log("数据异常， 退出")

	def deal_data(self, bytes):
		info = ""
		data = bytes.decode().split('|#|')
		# print("receive：", data)
		if data:
			proto = json.loads(data[0]).get('protocol')
			if proto and hasattr(self, proto):
				# print(proto)
				method = getattr(self, proto)
				result = method(data[0])
			else:
				write_log("not match client method" + proto)
	
		# 兜底
		if data:
			info = json.loads(data[0]).get('chat')
		if self.box and info:
			self.box.append_html_text("<br>" + info)

	def listen(self,):
		thread = Thread(target = self.receive_data)
		thread.setDaemon(True)
		thread.start()

	def close(self,):
		self.s.close()


	def player_status(self, data):
		# print("play_status", data)
		data = json.loads(data)
		# 如果当前uuid不在online_players 里面， 增添一名新玩家
		if not any([x.uuid == data.get("uuid") for x in self.online_players]):
			# print("not find exist player")
			tmp_player = Player(self.TILE_SIZE, self.TILE_SIZE)
			tmp_player.posX, tmp_player.posY = data.get('pos')
			tmp_player.movement = data.get('movement')
			tmp_player.direction = data.get('direction')
			tmp_player.uuid = data.get('uuid')

			self.online_players.append(tmp_player)
		else:
			for p in range(len(self.online_players)):
				if self.online_players[p].uuid == data.get("uuid"):
			
					self.online_players[p] = Player(self.TILE_SIZE, self.TILE_SIZE)
					self.online_players[p].posX, self.online_players[p].posY = data.get('pos')
					self.online_players[p].movement = data.get('movement')
					self.online_players[p].direction = data.get('direction')
					self.online_players[p].uuid = data.get('uuid')
					self.online_players[p].update = True
					break

		# print("prase done from online_players")


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