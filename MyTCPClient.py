import sys
import socket
import threading
import logging
from recvall import *

logging.basicConfig(level = logging.DEBUG, format = "%(name)s: %(message)s",)

class MYTCPClient(object):

	def __init__(self):
		self.logger = logging.getLogger('client')
		self.__my_socket = None
		return

	def read_input(self, in_path):
		self.logger.debug('read_input')
		try:
			self.input_file = open(in_path)
			self.input_data = '#' + '#'.join( [ line[:-2] for line in self.input_file if len(line) > 2 and line[0:2] != '//' ][1:] ) + '#'
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e)
			sys.exit(2)
		except Exception as e:
			self.input_file.close()
			print >>sys.stderr, e
			sys.exit(2)
		self.input_file.close()

	def read_input2(self, in_path):
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

	def write_output(self, out_path):
		self.logger.debug('write_output')
		try:
			self.output_file = open(out_path, 'w')
			self.output_file.write( self.received_data  )
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e)
			sys.exit(2)
		except Exception as e:
			self.output_file.close()
			print >>sys.stderr, e
			sys.exit(2)
		self.output_file.close()

	def break_data(self):
		self.logger.debug('break_data')
		try:
			packsize = 4096
			datasize = len( self.input_data )
			if datasize < packsize:
				return [self.input_data]
			else:
				self.datas_packs = []				
				sent = 0
				while sent < datasize:
					if (sent+packsize) < datasize:
						self.datas_packs.append( self.input_data[sent:(sent+packsize)] )
					else:
						self.datas_packs.append( self.input_data[sent:] )
					sent += packsize
				return self.datas_packs
		except Exception as e:
			print >>sys.stderr, e
			sys.exit(2)	

	def set_key(self, key):
		self.logger.debug('set_key')
		self.__key = key

	def get_key(self):
		self.logger.debug('get_key')
		try:
			return self.__key
		except Exception as e:
			print >>sys.stderr, e0
			return ''

	def set_server_address(self, address):
		self.logger.debug('set_server_address')
		self.__address = address

	def get_server_address(self):
		self.logger.debug('get_server_address')
		return self.__address
	
	def cripto(self):
		self.logger.debug('cripto')
		raw_data = ''
		return raw_data

	def decripto(self, raw_data=None):
		self.logger.debug('decripto')
		return

	def setup_socket(self):
		self.logger.debug('setup_socket')
		self.__my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.logger.debug('connecting to server')
		try:
			self.__my_socket.connect( self.__address )
		except Exception as e:
			print >>sys.stderr, e
			sys.exit(2)
		return

	def close_socket(self):
		self.logger.debug('close_socket')
		self.__my_socket.close()
		self.__my_socket = None
		return

	def send_data(self):
		self.logger.debug('send_data')
		return self.__my_socket.sendall( self.input_data )

	def wait_response(self):
		self.logger.debug('wait_response')
		response = recvall(self.__my_socket, 2)
		self.received_data = response
		return response

	def __del__(self):
		if self.__my_socket != None:
			self.close_socket()

if __name__ == '__main__':
	c = MYTCPClient()
	in_path = "modelo_entrada2.txt"
	out_path = "modelo_saida.txt"
	c.read_input2(in_path)
	c.cripto()
	#print( c.break_data() )
	c.set_server_address( ('200.239.135.25', 5430) )
	#c.set_server_address( ('200.239.133.2', 666) )
	c.setup_socket()
	c.send_data()
	
	data = c.wait_response()
	print(data)
	c.close_socket()
	c.decripto()
	c.write_output(out_path)
'''
	ip, port = 'localhost', 666
	logger = logging.getLogger('client')
	
	logger.debug('creating socket')
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	logger.debug('connecting to server')
	s.connect((ip, port))
	
	# Send the data
	message = 'Hello World!'
	logger.debug('sending data: "%s"', message)
	len_sent = s.send(message)

	# Receive a response
	logger.debug('waiting for response')
	response = s.recv(1024)
	logger.debug('response from server: "%s"', response)

	# Clean up
	logger.debug('closing socket')
	s.close()
	logger.debug('done')
'''
