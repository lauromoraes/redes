import socket, sys, threading, logging, select
from getIP import *

logging.basicConfig(level = logging.DEBUG, format = "%(name)s: %(message)s",)
PACKID = 0

class MyUDPServer():

	# Construtor
	def __init__(self):
		self.clients	= dict()
		self.PACKID	= 0
		self.MAX	= 4096
		self.PORT	= 5430
		self.HOST	= get_lan_ip()
		self.DELAY	= 0.1
		self.sock	= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind((self.HOST, self.PORT))
		self.sock.setblocking(0)
		self.logger	= logging.getLogger('MyUDPClient')
		return

	# Gerencia o contador de pacotes
	def getid(self):
		self.PACKID += 1
		return self.PACKID

	# Quebra um pacote, separando os cabecalhos e a mensagem em uma lista
	def splitpack(self, pack):
		return pack.split('|')

	#
	def serve(self):
		while True:
			try:
				self.result = select.select([self.sock],[],[])
				data, address = self.result[0][0].recvfrom(self.MAX)
				header = data[:65]
				fields  = self.splitpack(header)[:-1]
				print(fields)
				print(address)
				self.sock.sendto('ACK' ,address)
			except KeyboardInterrupt:
				self.sock.close()
				print('\nSaindo...')
				sys.exit(0)
				raise
			except:
				raise


server = MyUDPServer()
server.serve()











def makeid():
	global PACKID
	PACKID += 1
	return PACKID

def makepacket(opt, addr, packid, message):
	return '|'.join((str(opt), str(addr[0]), str(addr[1]), str(packid), message))

def server():
	MAX = 4096
	PORT = 666
	HOST = get_lan_ip()
	delay = 0.1
	message = 'teste'

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((HOST, PORT))
	sock.setblocking(0)

	logger = logging.getLogger('MyUDPServer')	
	logger.debug('Listen at: %s' % str(sock.getsockname()))
	
	while True:
		try:
			result = select.select([sock],[],[])
			print(result)
			#data, address = sock.recv(MAX)
			data, address = result[0][0].recvfrom(MAX)
			#print(data, address)
			print(data)
			sock.sendto('ACK' ,address)
		except KeyboardInterrupt:
			sock.close()
			print('\nSaindo...')
			sys.exit(0)
			raise
		except:
			raise

#server()
'''
t = threading.Thread(target=server.serve)
t.setDaemon(True) # don't hang on exit
t.start()
'''
'''
t = threading.Thread(target=server)
t.setDaemon(True) # don't hang on exit
t.start()
'''
