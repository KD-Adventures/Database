import sqlite3
import networkx as nx
import tkinter

banco = sqlite3.connect("BANCO.DB")
cursor = banco.cursor()

def criar_grafo(conhecidos):
	G = nx.Graph()
	
	todosNomes = []
	for linhas in conhecidos:

		grafo = []
		for nomes in linhas:
			grafo.append(nomes)
			if nomes not in todosNomes:
				todosNomes.append(nomes)
			
		G.add_nodes_from(grafo)
		G.add_edge(grafo[0],grafo[1])

	return G

	
def sugerir_amigos(me, grafo):
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
	
	#print(recomendacaoAmigos)
	recomendados = sorted(recomendacaoAmigos, key=recomendacaoAmigos.get, reverse=True)

	return recomendados