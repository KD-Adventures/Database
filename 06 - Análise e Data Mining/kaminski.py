import math
import sqlite3

banco = sqlite3.connect('rede.db')
cursor = banco.cursor()


def imprime(dado):
	for i in dado:
		print(i)




#1
def mediaFilmes():
	print('Media dos filmes: ')
	cursor.execute	(	
						'''
						SELECT AVG(GostaFilme.Nota) FROM GostaFilme;
						'''
					)
	print(cursor.fetchone()[0])

def mediaArtistas():
	print('Media dos artistas: ')
	cursor.execute	(	
						'''
						SELECT AVG(GostaArtista.Nota) FROM GostaArtista;
						'''
					)
	print(cursor.fetchone()[0])

def desvioPadraoFilmes():
	print('Desvio padrao dos filmes: ')
	cursor.execute	(
						'''
						SELECT (SUM((G.Nota - Media)*(G.Nota - Media)))/Quantidade FROM GostaFilme AS G,
							(SELECT AVG(G.Nota) AS Media, COUNT(G.Nota) AS Quantidade FROM GostaFilme AS G);
						'''
					)
	print(math.sqrt(cursor.fetchone()[0]))

def desvioPadraoArtistas():
	print('Desvio padrao dos artistas: ')
	cursor.execute	(
						'''
						SELECT (SUM((G.Nota - Media)*(G.Nota - Media)))/Quantidade FROM GostaArtista AS G,
							(SELECT AVG(G.Nota) AS Media, COUNT(G.Nota) AS Quantidade FROM GostaArtista AS G);
						'''
					)
	print(math.sqrt(cursor.fetchone()[0]))


#2
def maiorRatingMedioFilmes():
	print('Filmes com maior rating medio: ')
	cursor.execute	(	
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
	print('Artistas com maior rating medio: ')
	cursor.execute	(	
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
	print('Dez filmes mais populares: ')
	cursor.execute	(
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
	print('Dez artistas mais populares: ')
	cursor.execute	(
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
	print('View ConheceNomralizada: ')
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
	for i in cursor.fetchall():
		print(i)


def gostaMesmoFilme():
	print('Conhecidos com mais filmes em comum: ')
	cursor.execute	(
						"""
						SELECT coisa.login1, coisa.login2 
							FROM (
								SELECT MesmoFilme.Login1 as login1, MesmoFilme.Login2 as login2, COUNT(*) as soma
									FROM ( 
										SELECT ConheceNormalizada.*, GostaFilme.URI_Filme 
											FROM ConheceNormalizada INNER JOIN GostaFilme ON ConheceNormalizada.Login1 = GostaFilme.Login
										INTERSECT
										SELECT ConheceNormalizada.*,GostaFilme.URI_Filme 
											FROM ConheceNormalizada INNER JOIN GostaFilme ON ConheceNormalizada.Login2 = GostaFilme.Login
									) AS MesmoFilme 
									GROUP BY MesmoFilme.Login1, MesmoFilme.Login2
							) AS coisa
							GROUP BY coisa.soma
							Having coisa.soma = MAX(coisa.soma);
						"""
					)

	for i in cursor.fetchall():
		print(i)


def conhecidosDosConhecidos():
	print('Conhecidos dos integrantes do grupo: ')
	cursor.execute	(
						"""
						SELECT ConheceNormalizada.Login1, Conhecidos.* 
							FROM (
								SELECT ConheceNormalizada.Login1, COUNT(*)
									FROM ConheceNormalizada
									GROUP BY ConheceNormalizada.Login1 
									ORDER BY ConheceNormalizada.Login1 
								) AS Conhecidos, ConheceNormalizada

							WHERE ConheceNormalizada.Login1 = "davib" AND Conhecidos.Login1 = ConheceNormalizada.Login2
								OR 
								ConheceNormalizada.Login1 = "lucasfreitas" AND Conhecidos.Login1 = ConheceNormalizada.Login2
								OR 
								ConheceNormalizada.Login1 = "dennyssilva" AND Conhecidos.Login1 = ConheceNormalizada.Login2
							ORDER BY ConheceNormalizada.Login1 ASC;
						"""
					)
	for i in cursor.fetchall():
		print(i)


mediaFilmes()
raw_input('Aperte enter para continuar\n')
mediaArtistas()
raw_input('Aperte enter para continuar\n')
desvioPadraoFilmes()
raw_input('Aperte enter para continuar\n')
desvioPadraoArtistas()
raw_input('Aperte enter para continuar\n')
maiorRatingMedioFilmes()
raw_input('Aperte enter para continuar\n')
maiorRatingMedioArtistas()
raw_input('Aperte enter para continuar\n')
filmesPopulares()
raw_input('Aperte enter para continuar\n')
artistasPopulares()

raw_input('Aperte enter para continuar\n')
view()
raw_input('Aperte enter para continuar\n')
gostaMesmoFilme()
raw_input('Aperte enter para continuar\n')
conhecidosDosConhecidos()