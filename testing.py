def makearq():
	path = "modelo_entrada2.txt"
	arq = open(path, 'w+')

	data = '|'.join( [ str(i) for i in range(10000)] )
	 

	print(data)

	arq.write(data)
	arq.close()

makearq()
