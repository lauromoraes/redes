import socket, sys, threading, logging

logging.basicConfig(level = logging.DEBUG, format = "%(name)s: %(message)s",)
PACKID = 0

class MyUDPClient():

	# Construtor
	def __init__(self, host='localhost', port=666):
		self.PACKID	= 0
		self.MAX	= 4096
		self.PORT	= 666
		self.HOST	= 'localhost'
		self.DELAY	= 0.1
		self.sock	= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.logger	= logging.getLogger('MyUDPClient')

	# Gerencia o contador de pacotes
	def getid(self):
		self.PACKID += 1
		return self.PACKID

	# Armazana a mensagem
	def setmsg(self, msg=''):
		self.msg = msg

	# Divide a mensagem original em pedacos para que se monte os pacotes ao se juntar com os cabecalhos
	def setpacks(self):
		tam = len(self.msg)
		broken = 0
		msgsize = self.MAX - 64
		self.msgqueue = []
		while broken < tam:
			if (broken+msgsize) < tam:
				m = self.msg[broken:(broken+msgsize)]
				self.msgqueue.append(m)
				broken += msgsize
				
			else:
				self.msgqueue.append(self.msg[broken:])
				broken += msgsize
		return self.msgqueue

	# Monta o pacote juntando todos os campos
	def makepacket(self, opt, addr, packid, message):
		msg = '|'.join((str(opt), str(addr[0]), str(addr[1]), str(packid), message))
		msg += (' ' * (self.MAX - len(msg)))
		return msg

	# Monta todos os pacotes
	def makeallpackets(self):
		self.tosendpacks = list()
		opt	= 1
		addr	= self.sock.getsockname()
		packid	= self.getid()
		for msg in self.msgqueue:
			pack	= self.makepacket(opt, addr, packid, msg)
			self.tosendpacks.append(pack)
		return self.tosendpacks

	# Recebe as mensagens pacote por pacote
	def sendall(self):
		delay = self.DELAY
		for pack in self.tosendpacks:
			totalsent = 0
			while totalsent < self.MAX:
				sent = self.sock.send(pack[totalsent:])
				print('sent: ', sent)
				if sent == 0:
					raise RuntimeError('socket connection broken')
				totalsent += sent
			self.sock.settimeout(delay)
			try:
				data = self.sock.recv(self.MAX)
				print(data)
			except socket.timeout:
				delay *= 2
				if delay > 2.0:
					raise RuntimeError('Maybe server is down.')
			except:
				raise
			else:
				ack = True
				#self.sock.close()
		return

	# Realiza a conexao com o servidor
	def conn(self):
		h, p = self.HOST, self.PORT
		self.sock.connect((h, p))

	# Quebra um pacote, separando os cabecalhos e a mensagem em uma lista
	def splitpack(self, pack):
		return pack.split('|')

##################################
def client():

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	logger = logging.getLogger('MyUDPClient')

	MAX = 4096
	PORT = 666
	HOST = 'localhost'
	delay = 0.1
	message = 'teste'
	PACKID = 0

	# Cliente conecta-se ao servidorPACKID = 
	sock.connect((HOST, PORT))
	logger.debug('Client socket name is: %s' % str(sock.getsockname()))

	opt = 1
	addr = sock.getsockname()
	packid = makeid()
	pack = makepacket(opt, addr, packid, message)
	print(pack)
	ack = False
	while not ack:
		sock.send(pack)
		sock.settimeout(delay)
		try:
			data = sock.recv(MAX)
			print(data)
		except socket.timeout:
			delay *= 2
			if delay > 2.0:
				raise RuntimeError('Maybe server is down.')
		except:
			raise
		else:
			ack = True
			sock.close()

#client()
c = MyUDPClient()
c.conn()
msg = 'testando ' * 1000 
c.setmsg(msg)
c.setpacks()
q = c.makeallpackets()
c.sendall()

'''
for i in q:
	print('LEN: ', len(i))
	print(c.splitpack(i))
	print('\n')
'''
