import socket, sys, threading, logging, time
from getIP import *
from calc import *
from entrada_aleatoria import *

logging.basicConfig(level = logging.DEBUG, format = "%(name)s: %(message)s",)
PACKID = 0

class MyUDPClient():

	# Construtor
	def __init__(self, host=get_lan_ip(), port=5430):
		self.PACKID	= 0
		self.MAX	= 4096
		self.PORT	= port
		self.HOST	= host
		self.DELAY	= 0.1
		self.sock	= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.logger	= logging.getLogger('MyUDPClient')

	# Le o arquivo de entrada
	def read_input(self, in_path):
		self.logger.debug('read_input')
		try:
			self.input_file = open(in_path)
			self.input_data = ''.join( [ line for line in self.input_file ] )
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e)
			sys.exit(2)
		except Exception as e:
			self.input_file.close()
			print >>sys.stderr, e
			sys.exit(2)
		self.input_file.close()

	# Gerencia o contador de pacotes
	def getid(self):
		self.PACKID += 1
		return self.PACKID

	# Armazana a mensagem
	def setmsg(self, msg=''):
		self.msg = msg
		self.msg = self.input_data

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
		msg = '|'.join((str(opt), addr, str(packid), message))
		msg += (' ' * (self.MAX - len(msg)))
		return msg

	# Monta todos os pacotes
	def makeallpackets(self):
		self.tosendpacks = list()
		opt	= 1
		addr = self.sock.getsockname()
		opt	= 0
		#addr = self.sock.getsockname()
		addr = get_lan_ip()
		for msg in self.msgqueue:
			packid = self.getid()
			pack = self.makepacket(opt, addr, packid, msg)
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
		return

	# Realiza a conexao com o servidor
	def conn(self):
		h, p = self.HOST, self.PORT
		self.sock.connect((h, p))

	# Quebra um pacote, separando os cabecalhos e a mensagem em uma lista
	def splitpack(self, pack):
		return pack.split('|')

#client()
c = MyUDPClient()
c.conn()


getInput()
in_path = "input.txt"
out_path = "output.txt"
c.read_input(in_path)

msg = 'testando ' * 1000 
c.setmsg()
c.setpacks()
q = c.makeallpackets()
c.sendall()
