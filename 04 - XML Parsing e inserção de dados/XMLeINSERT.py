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
	arquivo.write("INSERT INTO ")
	arquivo.write(entidade)
	arquivo.write(" VALUES ('")
	flag = False
	for elementos in dados:
		if flag == True:
			arquivo.write(", '")
		else:
			flag = True
		arquivo.write(elementos)
		arquivo.write("'")
	arquivo.write(");\n")



def getData(root, index):
    
    tag = tags[index]

    salvarEm = tag[0] + ".sql"
    file = open(salvarEm, "w");

    for child in root.findall(tag[1]):
        elementos = []
        for atributo in tag[2:]:
            if atributo == "movieUri":
                dado_final = extraiTitulo(child.get(atributo))
            elif child.get(atributo).startswith("http"):
                dado_final = extraiDados(child.get(atributo))
            else:
                dado_final = child.get(atributo)       
            
            print dado_final

            if(dado_final == "" or dado_final == None):
                elementos.append("NULL")
            else:
                elementos.append(dado_final)
        


        inserir(elementos, tag[0], file)

    file.close()



for index in range(len(locais)):
   
    local = urllib2.urlopen(locais[index])
    Tree = ET.parse(local)
    root = Tree.getroot()

    getData(root, index)
    local.close
    
