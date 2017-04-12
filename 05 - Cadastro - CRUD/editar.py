
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
