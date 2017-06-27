import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
import tkinter

banco = sqlite3.connect("BANCO.DB")
cursor = banco.cursor()


def imprimir_caminho_recomendacoes(G, eu, amigos, amigosRecomendados, todosNomes):
	
	pos=nx.spring_layout(G)
	
	amigos = []
	for edges in G.edges():
		if edges[0] == eu:
			if edges[1] not in amigos:
				amigos.append(edges[1])
		elif edges[1] == eu:
			if edges[0] not in amigos:
				amigos.append(edges[0])
		
	colorNode = []				
	colorEdge = []
	for edges in G.edges():
		if edges[0] == eu or edges[1] == eu:
			colorEdge.append('red')
		elif edges[0] in amigos and edges[1] != eu:
			if edges[1] in amigos:
				colorEdge.append('green')
			else:
				colorEdge.append('yellow')
		elif edges [1] in amigos and edges[0] != eu:
			if edges[0] in amigos:
				colorEdge.append('green')
			else:
				colorEdge.append('yellow')
		else:
			colorEdge.append('grey')

	colorNode = []
	for node in G:
		if node == eu:
			colorNode.append('red')
		elif node in amigos:
			colorNode.append('green')
		elif node in amigosRecomendados:
			colorNode.append('yellow')
		else:
			colorNode.append('grey')

	nx.draw_networkx_nodes(G,pos,
                       G.nodes(),
                       node_color=colorNode,
                       node_size=500,
                   alpha=0.8)

	nx.draw_networkx_edges(G,pos,
                       G.edges(),
                       width=8,alpha=0.5,edge_color=colorEdge)

	labels = {}
	for i in G.nodes():
		for nome in todosNomes:
			if nome == i:
				labels[nome] = nome

	nx.draw_networkx_labels(G,pos,labels,font_size=16)
	plt.show()



def imprimir_grafo(grafo, conhecidos):

	todosNomes = []
	for linhas in conhecidos:
		for nomes in linhas:
			if nomes not in todosNomes:
				todosNomes.append(nomes)

	pos=nx.spring_layout(grafo)

	nx.draw_networkx_nodes(grafo,pos,
                       grafo.nodes(),
                       node_color='r',
                       node_size=500,
                   alpha=0.8)

	nx.draw_networkx_edges(grafo,pos,
                       grafo.edges(),
                       width=8,alpha=0.5,edge_color='r')

	labels = {}
	for i in grafo.nodes():
		for nome in todosNomes:
			if nome == i:
				labels[nome] = nome

	nx.draw_networkx_labels(grafo,pos,labels,font_size=16)
	#plt.savefig("fig.png")
	plt.show()




def criar_grafo(usuarios):
	G = nx.Graph()
	
	todosNomes = []
	for linhas in usuarios:

		grafo = []
		for nomes in linhas:
			grafo.append(nomes)
			if nomes not in todosNomes:
				todosNomes.append(nomes)
			
		G.add_nodes_from(grafo)
		G.add_edge(grafo[0],grafo[1])

	return G

	
def sugerir_amigos(me, grafo, imprimir):
	meusAmigos = nx.single_source_shortest_path_length(grafo, source=me, cutoff=1)

	meusAmigos.pop(me)
	recomendacaoAmigos = {}
	
	for amigos in meusAmigos:
		amigosDosAmigos = nx.single_source_shortest_path_length(grafo,source=amigos,cutoff=1)
		
		for possiveisAmigos in amigosDosAmigos:
			
			if possiveisAmigos not in recomendacaoAmigos:
				recomendacaoAmigos[possiveisAmigos] = 1
			else:
				recomendacaoAmigos[possiveisAmigos] += 1
	
	recomendacaoAmigos.pop(me)
	for i in meusAmigos:
		recomendacaoAmigos.pop(i)
	
	recomendados = sorted(recomendacaoAmigos, key=recomendacaoAmigos.get, reverse=True)

	if imprimir == True:		
		for i in recomendados:
			print("{}: {}".format(i, recomendacaoAmigos[i]))

	return recomendados