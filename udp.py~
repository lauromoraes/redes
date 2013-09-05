import socket, sys, threading, logging, select, time
from getIP import *

logging.basicConfig(level = logging.DEBUG, format = "%(name)s: %(message)s",)
PACKID = 0

class opts():
	conn		= '0'
	npacksrec	= '1'
	packrec		= '2'

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
		self.logger	= logging.getLogger('MyUDPServer')
		self.logger.debug('__init__')

		return

	# Gerencia o contador de pacotes
	def getid(self):
		self.PACKID += 1
		return self.PACKID

	# Quebra um pacote, separando os cabecalhos e a mensagem em uma lista
	def splitpack(self, pack):
		return pack.split('|')

	def rec(self):
		self.result = select.select([self.sock],[],[])
		data, address = self.result[0][0].recvfrom(self.MAX)
		if not len(data) < 65:
			header = data[:65]
		else:
			header = data
		fields  = self.splitpack(header)[:-1]
		return address, fields, data
	
	def confirm_conn(self, fields):
		self.logger.debug('confirm_conn')
		if not fields[1] in self.clients:
			self.clients[fields[1]] = list()
			self.clients[fields[1]].append(dict()) # Pacotes de tarefas [0]
			self.clients[fields[1]].append(dict()) # Pacotes de respostas [1]
		return opts.conn

	#
	def serve(self):
		self.logger.debug('serve')
		while True:
			try:
				address, fields, data = self.rec()
				if fields[0] == opts.conn: # Cliente esta querendo se conectar
					m = self.confirm_conn(fields)
					self.sock.sendto(m, address)
					s = ': '.join( ('conn accepted', address[0], repr(address[1])) )
					self.logger.debug( s )
				elif fields[0] == opts.npacksrec:
					m = opts.npacksrec
					self.sock.sendto(m, address)
					npacks = fields[2]
					m = opts.packrec
					self.logger.debug('receiving %s packs from %s' % (npacks, address) )
					for i in range( int(npacks) ):
						address, fields, data = self.rec()
						_id = fields[2]
						self.logger.debug('pack %s received from %s' % (_id, address) )
						if fields[0] == opts.packrec:
							self.logger.debug('pack %s received from %s' % (_id, address) )
							self.clients[fields[1]][0][_id] = data
							print(data)
							self.sock.sendto(m, address)

				print(fields)
				print(address)
				
			except KeyboardInterrupt:
				self.sock.close()
				print('\nSaindo...')
				sys.exit(0)
				raise
			except:
				raise


server = MyUDPServer()
t = threading.Thread(target=server.serve)
t.setDaemon(True) # don't hang on exit
t.run()
