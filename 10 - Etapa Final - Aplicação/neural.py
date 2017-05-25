from sklearn.neural_network import MLPRegressor
import numpy as np

vetores = open("vetores.txt", 'r')

X = []
y = []
for linhas in vetores:
	novoVetor = []
	# do primeiro ate o penultimo
	for word in linhas.split()[:-1]:
		novoVetor.append(float(word))
	y.append(float(linhas.split()[-1]))
	X.append(novoVetor)


#X = [[0., 1., 0.], [1., 1., 0.], [1.,0., 0.]]
#y = [0, 1, 1]



clf = MLPRegressor(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=4, random_state=1)
clf.fit(X,y)


print(clf.predict([[0., 0., 0., 1., 1., 0., 0.]]))
