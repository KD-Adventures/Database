#!/usr/bin/python

import xml.etree.ElementTree as ET

import os
import urllib2


locais = ["http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/person.xml", "http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/music.xml",
          "http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/movie.xml", "http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/knows.xml"]


tagsPessoa       = ['Usuario', 'Person', 'uri', 'name', 'hometown']
tagsGostaArtista = ['GostaArtista', 'LikesMusic', 'person', 'bandUri', 'rating']
tagsGostaFilme   = ['GostaFilme','LikesMovie', 'person', 'movieUri', 'rating']
tagsConhecidos   = ['Conhece', 'Knows', 'person', 'colleague']


tags = [tagsPessoa, tagsGostaArtista, tagsGostaFilme, tagsConhecidos]


def extraiTitulo(url):

	# abre o url da internet
    pagina = urllib2.urlopen(url)

    for linha in pagina:
  
        if linha.find("</title>") != -1:
            index_comeco = linha.find("<title>")
            index_fim = linha.find("</title>")
            titulo = linha[index_comeco + len("<title>"):index_fim]
            break

    return titulo


def extraiDados(dados):
    
    i = len(dados) - 1

    while i > 0 and dados[i] != '/':
        i -= 1

    dados = dados[i+1:]

    return dados


def inserir(dados, entidade, arquivo):
	
	# escreve no arquivo
	arquivo.write("INSERT INTO ")
	arquivo.write(entidade)
	arquivo.write(" VALUES ('")
	flag = False

	# para todos os elementos em dados
	for elementos in dados:
		if flag == True:
			arquivo.write(", '")
		else:
			flag = True
		arquivo.write(elementos)
		arquivo.write("'")
	arquivo.write(");\n")



def getData(root, index):
    
    # pega o vetor com os nomes adequados para cada atributo dos elementos
    tag = tags[index]

    # nome do arquivo que será salvo
    salvarEm = tag[0] + ".sql"
    # abre um arquivo com o nome definido acima em modo de escrita
    file = open(salvarEm, "w");

    # para todo elemento com a tag[1]
    for child in root.findall(tag[1]):
        # cria um vetor vazio
        elementos = []

        # para todo atributo da tag do 2º elemento até o ultimo
        for atributo in tag[2:]:


            if atributo == "movieUri":
                # extrai o título da página para o atributo de child
                dado_final = extraiTitulo(child.get(atributo))
            elif child.get(atributo).startswith("http"):
                dado_final = extraiDados(child.get(atributo))
            else:
                dado_final = child.get(atributo)       
            
            #print dado_final


            if(dado_final == "" or dado_final == None):
                # coloca na ultima posição do vetor elementos
                elementos.append("NULL")
            else:
                # coloca na ultima posição do vetor elementos
                elementos.append(dado_final)        


        inserir(elementos, tag[0], file)

    file.close()


# for de 0 até número de locais
for index in range(len(locais)):
   	
   	# pega o arquivo xml da internet
    local = urllib2.urlopen(locais[index])
    
    # cria a arvore do xml
    Tree = ET.parse(local)
    
    # recebe a raiz do xml
    root = Tree.getroot()

    getData(root, index)

    # fecha o arquivo xml
    local.close
    
