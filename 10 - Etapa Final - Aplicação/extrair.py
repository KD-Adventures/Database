#import xml.etree.ElementTree as ET

import urllib2

import sqlite3
import networkx as nx
import Tkinter
import matplotlib.pyplot as plt

def extrairGeneros():
	urls = open("urls.txt")
	generos = open("generos.txt",'w')

	todosGeneros = []

	for url in urls:
		pagina = urllib2.urlopen(url)
		genero = []
		for linha in pagina:
			
			if linha.find("\"genre\">") != -1:
				index_comeco = linha.find("\"genre\">")
				index_fim = linha.find("<", index_comeco)
				#titulo = linha[index_comeco + len("\"genre\">"):index_fim]
				gen = linha[index_comeco + len("\"genre\">"):index_fim]

				if gen:
					genero.append(linha[index_comeco + len("\"genre\">"):index_fim])
				else:
					continue
					
				if gen not in todosGeneros:
					todosGeneros.append(gen)

		string = ""
		genero.sort()
		for i in genero:
			if string:
				string = string + " " + i
			else:
				string = i

		generos.write(string + "\n")
		print(string)

	todosGeneros.sort()

	# criar vetor
	generos = open("generos.txt", 'r')
	vetores = open("vetores.txt",'w')

	print(todosGeneros)

	for line in generos:
		for valores in todosGeneros:
			if valores in line.split():
				vetores.write("1")
			else:
				vetores.write("0")
			vetores.write(" ")
		vetores.write("\n")


	vetores.close()
	urls.close()
	generos.close()

def extrairConhecidos():
	conhecidos = open("conhecidos.txt")

	G = nx.Graph()

	todosNomes = []
	for linhas in conhecidos:

		grafo = []
		for nomes in linhas.split():
			grafo.append(nomes)
			if nomes not in todosNomes:
				todosNomes.append(nomes)
			
		G.add_nodes_from(grafo)
		G.add_edge(grafo[0],grafo[1])
	
	pos=nx.spring_layout(G)

	nx.draw_networkx_nodes(G,pos,
                       G.nodes(),
                       node_color='r',
                       node_size=500,
                   alpha=0.8)

	nx.draw_networkx_edges(G,pos,
                       G.edges(),
                       width=8,alpha=0.5,edge_color='r')

	labels = {}
	for i in G.nodes():
		for nome in todosNomes:
			if nome == i:
				labels[nome] = nome

	nx.draw_networkx_labels(G,pos,labels,font_size=16)

	distance = nx.single_source_shortest_path_length(G,"rubens")
	print(distance)
	plt.savefig("grafo.png")
	plt.show()
	


if __name__ == "__main__":
	#extrairGeneros()
	extrairConhecidos()