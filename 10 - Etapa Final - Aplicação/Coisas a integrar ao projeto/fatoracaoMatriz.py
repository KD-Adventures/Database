import numpy as np 
import sqlite3
np.set_printoptions(precision=3)

banco = sqlite3.connect("BANCO.DB")
cursor = banco.cursor()


def criarMatriz():
	cursor.execute(
				'''
					SELECT * FROM GostaFilme;
				''')

	usuarioGostaFilme = cursor.fetchall()

	filmes = []
	usuarios = []
	gostoUsuario = {}
	filmesDoUsuario = []
	for i in sorted(usuarioGostaFilme):
		login = i[0]
		url = i[1]
		nota = i[2]

		if login not in usuarios:
			usuarios.append(login)
		if url not in filmes:
			filmes.append(url)
		
		if login not in gostoUsuario:
			filmesDoUsuario = []
			filmesDoUsuario.append((url,nota))
			gostoUsuario[login] = filmesDoUsuario
		else:
			gostoUsuario[login].append((url,nota))




	matrix = []
	for i in gostoUsuario:
		linha = np.zeros(len(filmes))
		for j in gostoUsuario[i]:
			url = j[0]
			nota = j[1]
			indice = filmes.index(url)
			linha[indice] = nota

		matrix.append(linha)

	matrix = np.array(matrix)
	return matrix

def calcularMatriz(R):


	K = 2
	P = np.random.rand(len(R),K)
	Q = np.random.rand(len(R[0]), K)

	steps = 1000
	alpha = 0.0002
	beta = 0.002

	# Transposta de Q
	Q = Q.T 


	for step in xrange(steps):
		if step % 100 == 0:
			print("Step: {}".format(step))
		for i in xrange(len(R)):
			for j in xrange(len(R[i])):
				if R[i][j] > 0:
					eij = R[i][j] - np.dot(P[i,:],Q[:,j])
					for k in xrange(K):
						P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
						Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
		eR = np.dot(P,Q)
		e = 0.
		for i in xrange(len(R)):
			for j in xrange(len(R[i])):
				if R[i][j] > 0:
					e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)
					for k in xrange(K):
						e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
		if e < 0.001:
			break

	#print(P)
	#print(Q.T)

	#print("\n\n\n")
	print(R)
	print(np.dot(P,Q))


R = criarMatriz()
calcularMatriz(R)
