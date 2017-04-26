import sqlite3
import matplotlib
import matplotlib.pyplot as plt

# abre o banco de dados chamado rede.db
banco = sqlite3.connect("rede.db")
cursor = banco.cursor()	

def executar(comando):
	cursor.execute(comando)
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
	for linha in cursor:
		x_inf.append(linha[0])
		y_inf.append(linha[1])	
		i+= 1
		if i==tam:#numero de dados a ser mostrado no grafico
			break
	gerarGrafico(x_inf,y_inf,xlabel, ylabel,tam)

def gerarGrafico(x,y,xlabel,ylabel,tam):#dados do eixo x, daodos do eixo y, nome do eixo x, nome do eixo y, tamanho
	plt.plot(range(len(x)), y, 'ro')
	plt.xticks( range(len(x[:tam])), x[:tam], rotation = 'vertical' )
	plt.ylabel(ylabel)
	plt.xlabel(xlabel)
	plt.subplots_adjust(bottom=0.6)
	plt.show()#mostra o grafico
print'Artistam mais gostados'
dadosGraficos(artistasMaisCurtidos,'Artista Musical','Pessoas', 10)
raw_input('Aperte enter para continuar\n')
print'Filmes mais gostados'
dadosGraficos(filmesMaisCurtidos,'Filmes','Pessoas', 10)
raw_input('Aperte enter para continuar\n')
print'Pessoas que mais gostaram de filmes'
dadosGraficos(pessoasQueMaisGostaramFilmes,'Pessoas','Numero de Filmes', 10)
raw_input('Aperte enter para continuar\n')
print'Pessoas que mais gostaram de Artistas'
dadosGraficos(pessoasQueMaisGostaramArtistas,'Pessoas','Numero de Artistas', 10)
