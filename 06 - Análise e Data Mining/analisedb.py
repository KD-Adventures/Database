import math
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import os

banco = sqlite3.connect('rede.db')
cursor = banco.cursor()

def executar(comando):
	cursor.execute(comando)

def imprime(dado):
	for i in dado:
		print i




#1
def mediaFilmes():
	print 'Media dos filmes: '
	executar	(	
						'''
						SELECT AVG(GostaFilme.Nota) FROM GostaFilme;
						'''
					)
	print cursor.fetchone()[0]

def mediaArtistas():
	print 'Media dos artistas: '
	cursor.execute	(	
						'''
						SELECT AVG(GostaArtista.Nota) FROM GostaArtista;
						'''
					)
	print cursor.fetchone()[0]

def desvioPadraoFilmes():
	print 'Desvio padrao dos filmes: '
	cursor.execute	(
						'''
						SELECT (SUM((G.Nota - Media)*(G.Nota - Media)))/Quantidade FROM GostaFilme AS G,
							(SELECT AVG(G.Nota) AS Media, COUNT(G.Nota) AS Quantidade FROM GostaFilme AS G);
						'''
					)
	print math.sqrt(cursor.fetchone()[0])

def desvioPadraoArtistas():
	print 'Desvio padrao dos artistas: '
	executar	(
						'''
						SELECT (SUM((G.Nota - Media)*(G.Nota - Media)))/Quantidade FROM GostaArtista AS G,
							(SELECT AVG(G.Nota) AS Media, COUNT(G.Nota) AS Quantidade FROM GostaArtista AS G);
						'''
					)
	print math.sqrt(cursor.fetchone()[0])


#2
def maiorRatingMedioFilmes():
	print 'Filmes com maior rating medio: '
	executar	(	
						'''
						SELECT Filme.Nome_Filme, AVG(GostaFilme.Nota) AS Media
							FROM (Filme INNER JOIN GostaFilme ON Filme.URI_Filme = GostaFilme.URI_Filme)
							GROUP BY Filme.Nome_Filme
							HAVING COUNT(GostaFilme.URI_Filme) > 1
							ORDER BY Media DESC;
						'''
					)
	leitura = cursor.fetchall()
	for linha in leitura:
		imprime(linha) 


def maiorRatingMedioArtistas():
	print 'Artistas com maior rating medio: '
	executar	(	
						'''
						SELECT Artista.Nome_Artista, AVG(GostaArtista.Nota) AS Media
							FROM (Artista INNER JOIN GostaArtista ON Artista.URI_Artista = GostaArtista.URI_Artista)
							GROUP BY Artista.Nome_Artista
							HAVING COUNT(GostaArtista.URI_Artista) > 1
							ORDER BY Media DESC;
						'''
					)
	leitura = cursor.fetchall()
	for linha in leitura:
		imprime(linha) 




#3

def filmesPopulares():
	print 'Dez filmes mais populares: '
	executar	(
						'''
						SELECT Filme.Nome_Filme, COUNT(Filme.URI_Filme) AS Quantidade
							FROM (Filme INNER JOIN GostaFilme ON Filme.URI_Filme = GostaFilme.URI_Filme)
							GROUP BY Filme.URI_Filme
							HAVING Quantidade > 2
							ORDER BY Quantidade DESC
							LIMIT 10;
						'''
					)
	leitura = cursor.fetchall()
	for linha in leitura:
		imprime(linha)


def artistasPopulares():
	print 'Dez artistas mais populares: '
	executar	(
						'''
						SELECT Artista.Nome_Artista, COUNT(Artista.URI_Artista) AS Quantidade
							FROM (Artista INNER JOIN GostaArtista ON Artista.URI_Artista = GostaArtista.URI_Artista)
							GROUP BY Artista.URI_Artista
							HAVING Quantidade > 2
							ORDER BY Quantidade DESC
							LIMIT 10;
						'''
					)
	leitura = cursor.fetchall()
	for linha in leitura:
		imprime(linha)

def view():
	executar("""CREATE VIEW IF NOT EXISTS ConheceNormalizada AS SELECT Conhece.Login1, Conhece.Login2 FROM Conhece 
		UNION SELECT Conhece.Login2, Conhece.Login1 FROM Conhece ORDER BY Conhece.Login1 ASC""")
	leitura = cursor.fetchall()
	for linha in leitura:
		imprime(linha)
	executar("SELECT * FROM ConheceNormalizada;")
	leitura = cursor.fetchall()
	for linha in leitura:
		imprime(linha)

def gostaMesmoFilme():
	executar("""SELECT MesmoFilme.Login1, MesmoFilme.Login2, Count(*) FROM ( 
		SELECT ConheceNormalizada.*, GostaFilme.URI_Filme FROM ConheceNormalizada, GostaFilme
			WHERE ConheceNormalizada.Login1 = GostaFilme.Login
		INTERSECT
		SELECT ConheceNormalizada.*,GostaFilme.URI_Filme FROM ConheceNormalizada, GostaFilme
			WHERE ConheceNormalizada.Login2 = GostaFilme.Login
		) AS MesmoFilme GROUP BY MesmoFilme.Login1, MesmoFilme.Login2;""")
	leitura = cursor.fetchall()
	for linha in leitura:
		imprime(linha)

def conhecidosDosConhecidos():
	executar("""SELECT ConheceNormalizada.Login1, Conhecidos.* 
		FROM (
		SELECT ConheceNormalizada.Login1, COUNT(*)
			FROM ConheceNormalizada
			GROUP BY ConheceNormalizada.Login1 
			ORDER BY ConheceNormalizada.Login1 ) AS Conhecidos, ConheceNormalizada

		WHERE ConheceNormalizada.Login1 = "davib" AND Conhecidos.Login1 = ConheceNormalizada.Login2
			OR 
			ConheceNormalizada.Login1 = "lucasfreitas" AND Conhecidos.Login1 = ConheceNormalizada.Login2
			OR 
			ConheceNormalizada.Login1 = "dennyssilva" AND Conhecidos.Login1 = ConheceNormalizada.Login2
		ORDER BY ConheceNormalizada.Login1 ASC;""")
	leitura = cursor.fetchall()
	for linha in leitura:
		imprime(linha)

def artistasMaisCurtidos():
	executar("""SELECT
			URI_Artista,
			COUNT(Login) AS Gostam
			FROM GostaArtista
			GROUP BY URI_Artista order by Gostam DESC;
		""")

def filmesMaisCurtidos():
	executar("""SELECT 
			URI_filme, 
			COUNT(Login) AS gostam 
			FROM GostaFilme 
			GROUP BY URI_Filme ORDER BY gostam DESC
		""")
def pessoasQueMaisGostaramFilmes():
	executar("""SELECT 
			Login, 
			COUNT(URI_filme) AS gosta 
			FROM GostaFilme 
			GROUP BY login ORDER BY gosta DESC
		""")

def pessoasQueMaisGostaramArtistas():
	executar("""SELECT 
			Login,
			COUNT(URI_Artista) AS Gosta
			FROM GostaArtista
			GROUP BY Login order by Gosta DESC;
		""")

def dadosGraficos(dados, xlabel, ylabel, tam):
	dados()#leitura dos dados do db
	linha = cursor.fetchone()
	x_inf = []#lista para armazenar dados do eixo x
	y_inf = []#lista para armazenar dados do eixo y
	i=0 
	x_inf.append(linha[0])
	y_inf.append(linha[1])
	for linha in cursor:
		x_inf.append(linha[0])
		y_inf.append(linha[1])	
		i+= 1
		if i==tam-1:#numero de dados a ser mostrado no grafico
			break
	gerarGrafico(x_inf,y_inf,xlabel, ylabel,tam)

def gerarGrafico(x,y,xlabel,ylabel,tam):#dados do eixo x, daodos do eixo y, nome do eixo x, nome do eixo y, tamanho
	plt.plot(range(len(x)), y, 'ro')
	plt.xticks( range(len(x[:tam])), x[:tam], rotation = 'vertical' )
	plt.ylabel(ylabel)
	plt.xlabel(xlabel)
	plt.subplots_adjust(bottom=0.6)
	plt.show()#mostra o grafico
def clear():
	os.system('cls' if os.name == 'nt' else 'clear')

mediaFilmes()
raw_input('Aperte enter para continuar\n')
clear()
mediaArtistas()
raw_input('Aperte enter para continuar\n')
clear()
desvioPadraoFilmes()
raw_input('Aperte enter para continuar\n')
clear()
desvioPadraoArtistas()
raw_input('Aperte enter para continuar\n')
clear()
maiorRatingMedioFilmes()
raw_input('Aperte enter para continuar\n')
clear()
maiorRatingMedioArtistas()
raw_input('Aperte enter para continuar\n')
clear()
filmesPopulares()
raw_input('Aperte enter para continuar\n')
clear()
artistasPopulares()
raw_input('Aperte enter para continuar\n')
clear()
print'ConheceNormalizada'
view()
raw_input('Aperte enter para continuar\n')
clear()
print'Gosta do mesmo Filme'
gostaMesmoFilme()
raw_input('Aperte enter para continuar\n')
clear()
print'Conhecido dos conhecidos'
conhecidosDosConhecidos()
clear()
print'Artistam mais gostados'
dadosGraficos(artistasMaisCurtidos,'Artista Musical','Pessoas', 10)
raw_input('Aperte enter para continuar\n')
clear()
print'Filmes mais gostados'
dadosGraficos(filmesMaisCurtidos,'Filmes','Pessoas', 10)
raw_input('Aperte enter para continuar\n')
clear()
print'Pessoas que mais gostaram de filmes'
dadosGraficos(pessoasQueMaisGostaramFilmes,'Pessoas','Numero de Filmes', 10)
raw_input('Aperte enter para continuar\n')
clear()
print'Pessoas que mais gostaram de Artistas'
dadosGraficos(pessoasQueMaisGostaramArtistas,'Pessoas','Numero de Artistas', 10)
clear()
