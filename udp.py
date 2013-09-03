import socket, sys, threading, logging, select

logging.basicConfig(level = logging.DEBUG, format = "%(name)s: %(message)s",)
PACKID = 0

class MyUDPServer():

	# Construtor
	def __init__(self):
		self.PACKID	= 0
		self.MAX	= 4096
		self.PORT	= 666
		self.HOST	= 'localhost'
		self.DELAY	= 0.1
		self.sock	= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.logger	= logging.getLogger('MyUDPClient')
		return

	# Gerencia o contador de pacotes
	def getid(self):
		self.PACKID += 1
		return self.PACKID




def makeid():
	global PACKID
	PACKID += 1
	return PACKID

def makepacket(opt, addr, packid, message):
	return '|'.join((str(opt), str(addr[0]), str(addr[1]), str(packid), message))

def server():
	MAX = 4096
	PORT = 666
	HOST = 'localhost'
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

server()
'''
t = threading.Thread(target=server)
t.setDaemon(True) # don't hang on exit
t.start()
'''
