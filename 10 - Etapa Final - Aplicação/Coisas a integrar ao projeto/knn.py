from sklearn.neighbors import NearestNeighbors
import numpy as np


# site com tutorial
#http://scikit-learn.org/stable/modules/neighbors.html

#exemplo
# categorias: acao, aventura, crime, comedia, drama, fantasia, ficcao cintifica, romance, terror
																							
#Poderoso chefao		: crime, drama				:[0,0,1,0,1,0,0,0,0]
#Batman the dark knight	: action, crime, drama		:[1,0,1,0,1,0,0,0,0]
#senhor dos aneis		: aventura, drama, fantasia	:[0,1,0,0,1,1,0,0,0]
#Alien					: terror, ficcao cientifica	:[0,0,0,0,0,0,1,0,1]
#Sim senhor				: comedia, romance			:[0,0,0,1,0,0,0,1,0]


PC 		= np.array([0,0,1,0,1,0,0,0,0])
BATMA 	= np.array([1,0,1,0,1,0,0,0,0])
ANEIS 	= np.array([0,1,0,0,1,1,0,0,0]) 
ALIEN 	= np.array([0,0,0,0,0,0,1,0,1])
SIM 	= np.array([0,0,0,1,0,0,0,1,0])


Filmes = np.array([	PC, 
					BATMA,
					ANEIS,
					ALIEN,
					SIM])

gostoUsuario = np.array([[1,1,0,0,0,0,0,0,0]])

nbrs = NearestNeighbors(n_neighbors=3, radius = 1.8, algorithm='ball_tree').fit(Filmes)
distances,indices = nbrs.kneighbors(Filmes)	

radiusDist, radiusInd  = nbrs.radius_neighbors(gostoUsuario)

print(Filmes)

# nao retorna na ordem de proximidade
print(radiusInd)
print(radiusDist)