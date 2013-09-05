import logging
import socket
import threading
import SocketServer
import time
import sys
import select
from recvall import *
from calc import *

logging.basicConfig( level = logging.DEBUG, format = "%(name)s: %(message)s", )

class MyUDPRequestHandler(SocketServer.BaseRequestHandler):

	def __init__(self, request, client_address, server):

		self.clients	= dict()
		self.PACKID	= 0	
		self.MAX	= 4096	
		self.logger = logging.getLogger('MyUDPRequestHandler')
		self.logger.debug('__init__')
		print(request)
		self.sock = request[1]
		self.data[0].strip()
		SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)		
		return

	# Gerencia o contador de pacotes
	def getid(self):
		self.logger.debug('getid')
		self.PACKID += 1
		return self.PACKID

	# Quebra um pacote, separando os cabecalhos e a mensagem em uma lista
	def splitpack(self, pack):
		self.logger.debug('splitpack')
		return pack.split('|')

	def rec(self):
		self.logger.debug('rec')
		self.sock.settimeout(None)
		#print(">>>>>>> 1", self.sock)
		#self.result = select.select([self.sock],[],[])
		#print(">>>>>>> 2")
		#data, address = self.result[0][0].recvfrom(self.MAX)
		#print(">>>>>>> 3")
		#data, address = recvall (self.sock, 2)
		
		#data, address = self.sock.recvfrom(self.MAX)
		print(self.data)
		print("<<<<<<<<<<<<")
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

	def setup(self):
		self.logger.debug('setup')
		return SocketServer.BaseRequestHandler.setup(self)

	def handle(self):
		self.logger.debug('handle')
	
		while True:
			try:
				address, fields, data = self.rec()
				print(">>>>>>>>>>>>>>>>>>>>>>>>>>>")
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
	
		self.request.shutdown(socket.SHUT_WR)
		self.request.close()
		return

	def finish(self):
		self.logger.debug('finish')
		return SocketServer.BaseRequestHandler.finish(self)

'''
	def handle(self):
		self.logger.debug('handle')
		data = recvall(self.request, 2)
		#print(self.request.accept()[1])
		#current_thread = threading.currentThread()
		#resp = "%s, %s" % (current_thread.getName(), data)
		#self.logger.debug('Thread: %s | recv()->"%s"', current_thread.getName(), data)
		#self.logger.debug('Threads: %s' % str( [ t.getName() for t in threading.enumerate()] ) )
		resp = calc(data)
		sent = 0
		size = 1024*5
		while(sent < len(resp)):
			if(sent+size <= len(resp)):
				sent += self.request.send(resp[sent:sent+size])
			else:
				sent += self.request.send(resp[sent:])
			time.sleep(0.1)
		#self.request.sendall("data")
		self.request.shutdown(socket.SHUT_WR)
		self.request.close()
		#time.sleep(3)
		return
'''
