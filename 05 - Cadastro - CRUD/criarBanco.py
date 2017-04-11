import urllib2

import sqlite3

banco = sqlite3.connect("rede.db")
cursor = banco.cursor()

def createDataBase(arquivo):
	
	file = open(arquivo)
	data = file.read()
	pos = 0

	# enquanto existir blocos de CREATE
	while data.find("CREATE") != -1:
		
		index_comeco = data.find("CREATE")
		index_fim = data.find(");")
		comando = data[index_comeco:index_comeco + len("CREATE TABLE")] + " IF NOT EXISTS " + data[index_comeco+len("CREATE TABLE"):index_fim + len(");")]
		data = data[index_fim+1:]
		cursor.execute(comando)	
	
	banco.commit()

createDataBase("banco_de_dados_simplificado.sql")