def isInt(num):
	try:
		int(num)
	except ValueError:
		return False
	return True

def calc(datas):
	results = []
	for data in datas.split('\n'):
		if(data[-2:] not in [';+', ';-', ';*']) or (len(data.split(';')[:-1]) < 2) or any (isInt(val) == False for val in data.split(';')[:-1]):
			result = 'Erro'
		else:
			valores = map(int, data.split(';')[:-1])

			result = valores[0]

			if(data[-1] == '+'):
				for val in valores[1:]:
					result = result + val

			elif(data[-1] == '-'):
				for val in valores[1:]:
					result = result - val

			elif(data[-1] == '*'):
				for val in valores[1:]:
					result = result * val
			else:
				result = 'Erro'
		results.append(result)
	return '\n'.join(repr(res) for res in results)
