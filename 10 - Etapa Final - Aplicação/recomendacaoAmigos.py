#import xml.etree.ElementTree as ET


import sqlite3
import networkx as nx
import Tkinter
import matplotlib.pyplot as plt
import scipy as sp


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
	
# So para desenho

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

#
	

	me = "rubens"
	meusAmigos = nx.single_source_shortest_path_length(G, source=me, cutoff=1)

	meusAmigos.pop(me)
	recomendacaoAmigos = {}
	
	for amigos in meusAmigos:
		amigosDosAmigos = nx.single_source_shortest_path_length(G,source=amigos,cutoff=1)
		
		for possiveisAmigos in amigosDosAmigos:
			
			if possiveisAmigos not in recomendacaoAmigos:
				recomendacaoAmigos[possiveisAmigos] = 1
			else:
				recomendacaoAmigos[possiveisAmigos] += 1
	
	recomendacaoAmigos.pop(me)
	for i in meusAmigos:
		recomendacaoAmigos.pop(i)
	
	print(recomendacaoAmigos)
	print(sorted(recomendacaoAmigos, key=recomendacaoAmigos.get, reverse=True))



	plt.savefig("grafo.png")
	plt.show()
	


if __name__ == "__main__":
	extrairConhecidos()

