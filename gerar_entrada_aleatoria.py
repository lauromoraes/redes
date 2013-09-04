import random


max_valores = 5
operacoes = 10000
operando = ["","+","-","*","+","-","*","+","-","*"]

saida = open("entrada.txt", "w")
for i in range(operacoes):
	max_valores = random.randint(0, 5)
	for valor in range(max_valores):
		saida.write(repr(random.randint(0, 10)) + ";")
	saida.write(operando[random.randint(0, 9)]+"\n")
saida.close