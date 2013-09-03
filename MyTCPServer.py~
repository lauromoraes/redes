import logging
import socket
import threading
import SocketServer
from MyTCPRequestHandler import *
from recvall import *

logging.basicConfig(level = logging.DEBUG, format = "%(name)s: %(message)s",)

class MyTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

	def __init__(self, server_address, handler_class = MyTCPRequestHandler):
		self.logger = logging.getLogger('MyTCPServer')
		self.logger.debug('__init__')
		SocketServer.TCPServer.__init__(self, server_address, handler_class)
		SocketServer.ThreadingMixIn
		return

	def server_activate(self):
		self.logger.debug('server_activate')
		SocketServer.TCPServer.server_activate(self)
		return

	def serve_forever(self):
		self.logger.debug('serve_forever')
		self.logger.info('Handling requests, press <Ctrl-C> to quit')
		while True:
			self.handle_request()
		return

	def handle_request(self):
		self.logger.debug('handle_request')
		return SocketServer.TCPServer.handle_request(self)

	def verify_request(self, request, client_address):
		self.logger.debug('verify_request(%s, %s)', request, client_address)
		return SocketServer.TCPServer.verify_request(self, request, client_address)

	def process_request(self, request, client_address):
		self.logger.debug('process_request(%s, %s)', request, client_address)
		SocketServer.ThreadingMixIn.daemon_threads = True
		print(">>>>>>>>>>>>", SocketServer.ThreadingMixIn.daemon_threads)
		return SocketServer.ThreadingMixIn.process_request(self, request, client_address)

	def server_close(self):
		self.logger.debug('server_close')
		return SocketServer.TCPServer.server_close(self)

	def finish_request(self, request, client_address):
		self.logger.debug('finish_request(%s, %s)', request, client_address)
		return SocketServer.TCPServer.finish_request(self, request, client_address)

	def close_request(self, request_address):
		self.logger.debug('close_request(%s)', request_address)
		return SocketServer.TCPServer.close_request(self, request_address)

if __name__ == '__main__':
	import socket
	import sys
	import threading
	import logging

	logging.basicConfig(level = logging.DEBUG, format = "%(name)s: %(message)s",)
	
	address = (str(sys.argv[1]), int(sys.argv[2])) # let the kernel give us a port
	server = MyTCPServer(addr, MyTCPRequestHandler)
	server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	ip, port = server.server_address # find out what port we were given

	try:
		t = threading.Thread(target=server.serve_forever)
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
		    	server.socket.settimeout(2)
		    	pass
		except KeyboardInterrupt:
			print("\nSaindo...")
			server.socket.shutdown(socket.SHUT_WR)
			server.socket.close()
			server.server_close()			
			sys.exit(0)
			raise
		except:
			raise

	server.socket.close()
