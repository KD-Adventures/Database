import sys
import sqlite3

# abre o banco de dados chamado rede.db
banco = sqlite3.connect("rede.db")
cursor = banco.cursor()	


# formata o texto
def imprimir(dado):
	
	dados = []
	for i in dado:
		string = ""
		# para todo j ate o numero de elementos de i
		for j in range(len(i)):
			string += i[j]
		print string

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


def checkIfExist(dado, local, condicao):

	# verifica se o retorno esta vazio
	if getFromDataBase("SELECT " + dado + " FROM " + local + " WHERE " + condicao + ";") == []:
		return False
	else:
		return True

def apagar(table, row, dado):

	putOnDataBase("DELETE FROM " + table + " WHERE " + row + " = " + "\'" + dado + "\'"+ ";")
	# submete o codigo ao banco de dados
	banco.commit()

def listar(dado, local, condicao):
	
	if condicao == "NULL":
		imprimir(getFromDataBase("SELECT " + dado + " FROM " + local + ";"))
	else:
		imprimir(getFromDataBase("SELECT " + dado + " FROM " + local + " Where " + condicao + ";"))

	input = raw_input("\nDigite: \n1 - Para Apagar um usuario \n2 - Para Editar um usuario \n3 - Para voltar para a pagina inicial \n>> ")

	digitoValido = False
	while not digitoValido:
		
		if input == "1":
			existente = False
			while not existente:
				
				usuario = raw_input("Digite: \nO login do usuario ou\n1 - para retornar a pagina inicial:\n>> ")
				if usuario == "1":
					digitoValido = True
					break
				existente = checkIfExist("Usuario.Login", "Usuario", "Usuario.Login = '" + usuario + "'")

				if not existente:
					print "\nUsuario nao existente\n"
					continue
				
				confirmacao = raw_input("Tem certeza que quer excluir " + usuario + "? (Y/N)\n>> ")
				if confirmacao == "Y" or confirmacao == "y":
					apagar("Usuario", "Usuario.Login", usuario)

				digitoValido = True

		elif input == "2":
			usuario = raw_input("Digite o login do usuario:\n>>")
			editar(usuario)
			digitoValido = True
		
		elif input == "3":
			digitoValido = True
		
		else:
			input = raw_input("Digito invalido\nDigite: \n1 - Para Apagar um usuario \n2 - Para Editar um usuario \n3 - Para voltar para a pagina inicial \n>> ")


def inicial():

	sair = False
	while not sair:
		input = raw_input("Digite: \n1 - Para Inserir um novo usuario ou \n2 - Para listar os usuarios existentes\n>> ")
		if input == "1":
			inserir()
		elif input == "2":
			listar("Usuario.Login", "Usuario", "NULL")


inicial()