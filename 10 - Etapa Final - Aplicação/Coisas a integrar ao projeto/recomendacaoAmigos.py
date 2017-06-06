import sqlite3
import networkx as nx
import Tkinter
import matplotlib.pyplot as plt
import scipy as sp

#banco = sqlite3.connect("rede.db")
banco = sqlite3.connect("BANCO.DB")
cursor = banco.cursor()

def view():
	cursor.execute	(
						'''
						CREATE VIEW IF NOT EXISTS ConheceNormalizada AS 
							SELECT Conhece.Login1, Conhece.Login2 FROM Conhece 
							UNION 
							SELECT Conhece.Login2, Conhece.Login1 FROM Conhece 
							ORDER BY Conhece.Login1 ASC;
							'''
					)

	cursor.execute	(
						'''
						SELECT * FROM ConheceNormalizada;
						'''
					)
	conhece = cursor.fetchall()
	return conhece

def criarGrafo(conhecidos):

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
	plt.savefig("grafo.png")
	plt.show()

	return G
	
def sugerirAmigos(me, grafo):

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

	for i in recomendados:
		print i
	


conhecidos = view()
grafoAmigos = criarGrafo(conhecidos)

sugerirPara = "davib"
sugerirAmigos(sugerirPara, grafoAmigos)