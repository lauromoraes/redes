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
		self.server_address = (self.HOST, self.PORT)
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

				# Rotina que cadastra um novo cliente
				if fields[0] == opts.conn:
					m = self.confirm_conn(fields)
					self.sock.sendto(m, address)
					s = ': '.join( ('conn accepted', address[0], repr(address[1])) )
					self.logger.debug( s )

				# Rotina para receber requisicao de servico do cliente
				# Primeiro o cliente informa quantos pacotes ira enviar
				elif fields[0] == opts.npacksrec:
					m = opts.npacksrec
					self.sock.sendto(m, address)
					npacks = fields[2]
					m = opts.packrec
					self.logger.debug('receiving %s packs from %s' % (npacks, address) )
					# Servidor comeca a receber os pacotes e confimrar 
					for i in range( int(npacks) ):
						print(threading.currentThread())
						address, fields, data = self.rec()
						_id = fields[2]
						self.logger.debug('pack %s received from %s' % (_id, address) )
						if fields[0] == opts.packrec:
							self.logger.debug('pack %s received from %s' % (_id, address) )
							self.clients[fields[1]][0][_id] = data
							#print(data)
							self.sock.sendto(m, address)
						time.sleep(0.5)

				#print(fields)
				#print(address)
				
			except KeyboardInterrupt:
				self.sock.close()
				print('\nSaindo...')
				sys.exit(0)
				raise
			except:
				raise

if __name__ == '__main__':

	logging.basicConfig(level = logging.DEBUG, format = "%(name)s: %(message)s",)
	
	#address = (str(sys.argv[1]), int(sys.argv[2])) # let the kernel give us a port
	#address = (get_lan_ip(), int(sys.argv[1])) # let the kernel give us a port
	server = MyUDPServer()
	#server.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	ip, port = server.server_address # find out what port we were given

	try:
		t = threading.Thread(target=server.serve)
		t.setDaemon(True) # don't hang on exit
		t.start()
		print "Server loop running in thread:", t.name
	except RuntimeError as e:
		print >>sys.stderr, e
		sys.exit(2)

	logger = logging.getLogger('server')
	logger.info('Server on %s:%s', ip, port)
	while True:
		try:
		    	server.sock.settimeout(2)
		    	pass
		except KeyboardInterrupt:
			print("\nSaindo...")
			server.sock.shutdown(socket.SHUT_WR)
			server.sock.close()
			server.server_close()			
			sys.exit(0)
			raise
		except:
			raise

	server.sock.close()

