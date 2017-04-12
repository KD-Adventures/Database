import sys
import sqlite3

# abre o banco de dados chamado rede.db
banco = sqlite3.connect("rede.db")
cursor = banco.cursor()	


def toArray(dado):

	dados = []
	for i in dado:
		# para todo j ate o numero de elementos de i
		for j in range(len(i)):
			dados.append(i[j])
	return dados

# formata o texto
def imprimir(dado):
	
	toPrint = toArray(dado)
	
	for i in toPrint:			
		print i


def getFromDataBase(codigo):
	
	linhas = []
	# executa o codigo SQL
	cursor.execute(codigo)
	# pega todas as linhas retornadas
	for i in cursor.fetchall():
		linhas.append(i)
	return linhas

def putOnDataBase(codigo):

	cursor.execute(codigo)
	# submete o codigo ao banco de dados
	banco.commit()

def checkIfExist(dado, entidade, condicao):

	# verifica se o retorno esta vazio
	if getFromDataBase("SELECT " + dado + " FROM " + entidade + " WHERE " + condicao + ";") == []:
		return False
	else:
		return True

def apagar(entidade, row, dado):

	putOnDataBase("DELETE FROM " + entidade + " WHERE " + row + " = " + "\'" + dado + "\'"+ ";")
	

def inserir(entidade):
	

	cursor.row_factory = sqlite3.Row

	table = cursor.execute("SELECT * FROM " +  entidade + ";")

	string = "INSERT OR IGNORE INTO " + entidade + " VALUES ("		

	# pega o nome das colunas
	nomeColunas = table.fetchone().keys()
	
	dados = []
	for i in nomeColunas:

		input = raw_input("\nDigite " + i + " desejado: ")
		
		dados.append(input)
		# 0 -1 significa ultima posicao
		if i == nomeColunas[-1]:
			string += "' " + input + "');"
		else:
			string += "' " + input + "', "

	print "\nNovo usuario  \n"
	
	novoUsuario = ""
	for i in dados:
		# 0 -1 significa ultima posicao
		if i == dados[-1]:
			novoUsuario += i + "; "
		else:
			novoUsuario += i + ", "

	print novoUsuario

	confirmacao = raw_input("\nDigite S para confirmar ou N para cancelar: \n>> ")

	if confirmacao == "S" or confirmacao == "s":
		putOnDataBase(string)
	


def putOnDataBaseTuple(codigo,tuples):

	cursor.execute(codigo,tuples)
	# submete o codigo ao banco de dados
	banco.commit()


def editar(usuario):


	cursor.row_factory = sqlite3.Row
	table = cursor.execute("SELECT * FROM Usuario;")
	# pega o nome das colunas
	nomeColunas = table.fetchone().keys()
	
	elementos = toArray(getElements("*", "Usuario", " Usuario.Login = '{}'".format(usuario)))

	dados = []
	
	print "\n"
	for i in range(len(elementos)):
		# formata a string, coloca nomeColunas[i] na primeira chave, e elementos[i] na segunda
		print "{} : {}".format(nomeColunas[i],elementos[i])
		dados.append(elementos[i])
	

	campoExiste = False
	while not campoExiste: 
		campoModificado = raw_input("\nDigite o nome do campo a ser atualizado ou 1 - para cancelar:\n>> ")

		if campoModificado == "1":
			return

		campoExiste = False
		for i in nomeColunas:

			if campoModificado == i:
				valorNovo = raw_input("\nDigite " + i + ":\n>> ")
				campoExiste = True

				indexModificado = nomeColunas.index(i)
				valorAtual = dados[indexModificado]
				dados[indexModificado] = valorNovo

				putOnDataBaseTuple("REPLACE INTO Usuario VALUES (?,?,?);", tuple(dados))

		print("\nCampo Inexistente\n")



def getElements(dado, entidade, condicao):
	
	if condicao == "NULL":
		return getFromDataBase("SELECT " + dado + " FROM " + entidade + ";")
	else:
		return getFromDataBase("SELECT " + dado + " FROM " + entidade + " Where " + condicao + ";")



def printRelacionamentos(usuario):
	print "\n\n " + usuario + " conhece os seguintes usuarios: \n"
	table = getElements("Conhece.Login2", "Conhece", "Conhece.Login1 = '" + usuario + "'")
	imprimir(table)


def addRelacionamento(usuario1):
	
	while True:
		usuario2 = raw_input("\nQuem " + usuario1 + " conhece? (digite 1 para voltar para a pagina inicial)\n>>")

		if input == "1":
			return
		
		if not checkIfExist("Usuario.Login", "Usuario", "Usuario.Login = '" + usuario2 + "'"):
			print "\nEsse usuario nao existe\n"
			continue

		if checkIfExist("Conhece.Login2", "Conhece", "Conhece.Login1 = '" + usuario1 + "' AND Conhece.Login2 = '" + usuario2 + "'"):
			print "\nEsse relacionamento ja foi cadastrado\n"
			continue

		cursor.execute("INSERT INTO Conhece VALUES ('" + usuario1 + "', '" + usuario2 + "');")
		return



def relacionamentos():
	input = raw_input("\nDigite: \n1 - Para verificar relacionamentos de um usuario \n2 - Para adicionar relacionamentos de um usuario \n3 - Para voltar para a pagina inicial \n>> ")

	digitoValido = False
	while not digitoValido:

		if input == "1" or input == "2":
			existente = False
			digitoValido = True

			while not existente:
				usuario = raw_input("\nDigite: \nO login do usuario ou\n1 - para retornar a pagina inicial:\n>> ")
				
				if usuario == "1":
					return

				existente = checkIfExist("Usuario.Login", "Usuario", "Usuario.Login = '" + usuario + "'")

				if not existente:
					print "\nUsuario nao existente\n"
					continue

				if input == "1":
					printRelacionamentos(usuario)

				else:
					addRelacionamento(usuario)

		elif input == "3":
			return

		else:
			input = raw_input("Digito invalido\nDigite: \n1 - Para verificar relacionamentos de um usuario \n2 - Para adicionar relacionamentos de um usuario \n3 - Para voltar para a pagina inicial \n>> ")




def listar(dado, entidade, condicao):

	imprimir(getElements(dado, entidade, condicao))

	input = raw_input("\nDigite: \n1 - Para Apagar um usuario \n2 - Para Editar um usuario \n3 - Para editar relacionamentos \n4 - Para voltar para a pagina inicial \n>> ")

	digitoValido = False
	while not digitoValido:
		
		if input == "1" or input == "2":
			existente = False
			digitoValido = True
			while not existente:
				
				usuario = raw_input("\nDigite: \nO login do usuario ou\n1 - para retornar a pagina inicial:\n>> ")
				if usuario == "1":
					digitoValido = True
					break
				
				existente = checkIfExist("Usuario.Login", "Usuario", "Usuario.Login = '" + usuario + "'")

				if not existente:
					print "\nUsuario nao existente\n"
					continue

				if input == "1":
					confirmacao = raw_input("Tem certeza que quer excluir " + usuario + "? \n  Digite S para sim ou N para nao: \n>> ")
					if confirmacao == "S" or confirmacao == "s":
						apagar("Usuario", "Usuario.Login", usuario)

				else:
					editar(usuario)

		elif input == "3":
			digitoValido = True
			relacionamentos()

		elif input == "4":
			digitoValido = True
		
		else:
			input = raw_input("Digito invalido\nDigite: \n1 - Para Apagar um usuario \n2 - Para Editar um usuario \n3 - Para editar relacionamentos \n4 - Para voltar para a pagina inicial \n>> ")


def inicial():

	sair = False
	while not sair:
		input = raw_input("\nDigite: \n1 - Para Inserir um novo usuario ou \n2 - Para listar os usuarios existentes\n>> ")
		if input == "1":
			inserir("Usuario")
		elif input == "2":
			listar("Usuario.Login", "Usuario", "NULL")


inicial()