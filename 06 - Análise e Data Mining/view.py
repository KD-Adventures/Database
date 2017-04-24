import sqlite3


# abre o banco de dados chamado rede.db
banco = sqlite3.connect("rede.db")
cursor = banco.cursor()	

def executar(comando):
	cursor.execute(comando)

def view():
	executar("""CREATE VIEW IF NOT EXISTS ConheceNormalizada AS SELECT Conhece.Login1, Conhece.Login2 FROM Conhece 
		UNION SELECT Conhece.Login2, Conhece.Login1 FROM Conhece ORDER BY Conhece.Login1 ASC""")
	executar("SELECT * FROM ConheceNormalizada;")

def gostaMesmoFilme():
	executar("""SELECT MesmoFilme.Login1, MesmoFilme.Login2, Count(*) FROM ( 
		SELECT ConheceNormalizada.*, GostaFilme.URI_Filme FROM ConheceNormalizada, GostaFilme
			WHERE ConheceNormalizada.Login1 = GostaFilme.Login
		INTERSECT
		SELECT ConheceNormalizada.*,GostaFilme.URI_Filme FROM ConheceNormalizada, GostaFilme
			WHERE ConheceNormalizada.Login2 = GostaFilme.Login
		) AS MesmoFilme GROUP BY MesmoFilme.Login1, MesmoFilme.Login2;""")

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


view()
gostaMesmoFilme()
conhecidosDosConhecidos()

