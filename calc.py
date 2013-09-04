def isInt(num):
	try:
		int(num)
	except ValueError:
		return False
	return True

def calc(data):
	if(data[-2:] not in {';+', ';-', ';*'}) or any (isInt(val) == False for val in data.split(';')[:-1]):
		return "Erro"

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
		return "Erro"
	return result
