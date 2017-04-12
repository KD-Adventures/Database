#!/usr/bin/python

import xml.etree.ElementTree as ET

import urllib2

import sqlite3

locais = []
# abre o txt que armazena o link para os arquivos xml
arquivos = open("readme.txt")
# para cada linha no arquivo
for linha in arquivos:
	# adiciona a linha na proxima posicao vazia da lista
	locais.append(linha)


tagsPessoa       = ['Usuario', 'Person', 'uri', 'name', 'hometown']
tagsGostaArtista = ['GostaArtista', 'LikesMusic', 'person', 'bandUri', 'rating']
tagsGostaFilme   = ['GostaFilme','LikesMovie', 'person', 'movieUri', 'rating']
tagsConhecidos   = ['Conhece', 'Knows', 'person', 'colleague']

tagsFilme 		 = ['Filme', 'LikesMovie', 'movieUri']
tagsArtista 	 = ['Artista', 'LikesMusic', 'bandUri']


tags = [tagsPessoa, tagsFilme, tagsArtista, tagsGostaArtista, tagsGostaFilme, tagsConhecidos]

# cria um dicionario vazio
titulosVerificados = {}
def extraiTitulo(url):

	# verifica se o titulo desse url ja foi encontrado
	for i in titulosVerificados:
		if i == url:
			# retorna o titulo relacionado ao url verificado i
			return titulosVerificados[i]
	
	# abre o url da internet
	pagina = urllib2.urlopen(url)
	for linha in pagina:  
		
		if linha.find("</title>") != -1:
			# encontra a posicao que comeca a tag <title>
			index_comeco = linha.find("<title>")
			# encontra a posicao que termina com a tag </title>
			index_fim = linha.find("</title>")
			# pega da posicao: inicio + tamanho <title>  ate a posicao final
			titulo = linha[index_comeco + len("<title>"):index_fim]

			# associa o tituo com o url
			titulosVerificados[url] = titulo
			break

	return titulo


def extraiDados(dados):
    
    # determina o tamanho do link
    i = len(dados) - 1

    # enquanto o link nao chegou ao fim
    while i > 0 and dados[i] != '/':
        i -= 1

    # pega da posicao i+1 ate o final do link
    dados = dados[i+1:]

    return dados


def inserir(dados, entidade, arquivo):
	
	# cria a string
	string = "INSERT OR IGNORE INTO " + entidade + " VALUES ('"
	maisDados = False
    
	# para todos os elementos em dados
	for elementos in dados:
		# se tiver mais dados, coloca uma virgula na string
		if maisDados == True:
			string += ", '"
		else:
			maisDados = True
		# concatena elementos na string
		string += elementos
		string += "'"
	# fecha o comando de sql
	string += ");\n"
	
	# salva o comando no arquivo
	arquivo.write(string)


def getData(root, tag):
    
	
    # nome do arquivo que sera salvo
	salvarEm = tag[0] + ".sql"

	# abre um arquivo com o nome definido acima em modo de escrita
	file = open(salvarEm, "w")
        
    # para todo elemento com a tag[1]
	for child in root.findall(tag[1]):
        # cria um vetor vazio
		elementos = []

        # para todo atributo da tag do segundo elemento ate o ultimo
		for atributo in tag[2:]:
			
			dado_final = []
			
			if atributo == "movieUri":
				# extrai o titulo da pagina para o atributo de child
				dado_final.append(child.get(atributo))
				
				if tag[0] == "Filme":
					dado_final.append(extraiTitulo(child.get(atributo)))
					#dado_final.append(child.get(atributo))
			
			elif atributo == "bandUri":
				dado_final.append(child.get(atributo))
				
				if tag[0] == "Artista":
					dado_final.append(extraiDados(child.get(atributo)))
			
			elif child.get(atributo).startswith("http"):
				dado_final.append(extraiDados(child.get(atributo)))
			
			else:
				dado_final.append(child.get(atributo))
            
			#print dado_final

			for i in dado_final:
				
				if(i == "" or i == None):
					# coloca na ultima posicao do vetor elementos
					elementos.append("NULL")
				else:
					# coloca na ultima posicao do vetor elementos
					elementos.append(i)
			
		inserir(elementos, tag[0], file)

	file.close()

# for de 0 ate numero de locais
for index in range(len(locais)):
   	
   	# pega o arquivo xml da internet
	local = urllib2.urlopen(locais[index])
    
    # cria a arvore do xml
	Tree = ET.parse(local)
    
    # recebe a raiz do xml
	root = Tree.getroot()

	# procura o conjunto de tags correspondente ao arquivo xml
	for atributo in tags:
		# se a tag do child de root for igual ao atributo
		if root[0].tag == atributo[1]:
			print "Criando " + atributo[0]
			if atributo[0] == 'Filme':
				print "Extraindo titulo do IMDB (demora um pouco)"
			getData(root, atributo)

    # fecha o arquivo xml
	local.close
    