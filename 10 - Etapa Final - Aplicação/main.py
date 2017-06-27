import os
import sqlite3
import time
import networkx as nx
import numpy as np 

from functools import partial

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.anchorlayout import AnchorLayout
#from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

from recomendacaoAmigos import criar_grafo, sugerir_amigos
from fatoracaoMatriz import calcular_matriz

banco = sqlite3.connect('BANCO.DB')
cursor = banco.cursor()


class FilmeLabel(Label):
	pass


class RedeSocial(GridLayout):

	nome_usuario_atual = StringProperty()
	login_usuario_atual = StringProperty('lucasfreitas')
	qtdade_amigos = NumericProperty()
	ordem_filmes = []


	# Construtor
	def __init__(self, **kwargs):
		super().__init__()

		# Constroi o grafo com todas as pessoas da rede e seus conhecidos
		cursor.execute('select * from ConheceNormalizada;')
		self.grafo_amigos = criar_grafo(cursor.fetchall())

		# Constroi a matriz de recomendacao de filmes
		if os.stat("matriz.txt").st_size > 0 and os.stat("ordem.txt").st_size > 0:
			with open("matriz.txt") as f:
				self.R = np.loadtxt(f)
			with open("ordem.txt") as f:
				self.ordem_filmes = f.readlines()
		else:
			(self.R, self.ordem_filmes) = calcular_matriz()
			with open("matriz.txt", 'wb') as f:
				np.savetxt(f, self.R, fmt='%.2f')
			with open("ordem.txt", 'w') as f:
				for linha in self.ordem_filmes:
					f.write(linha + '\n')

		cursor.execute('select Login from GostaFilme')
		self.usuarios_em_ordem = []
		for row in cursor:
			if row[0] not in self.usuarios_em_ordem:
				self.usuarios_em_ordem.append(row[0])

		Clock.schedule_once(partial(self.define_usuario, 'lucasfreitas'), .7)
		# Esse clock é necessário pra dar tempo do Kivy carregar tudo antes de executar a
		# funcao "define_usuario" pela primeira vez
		

	# Apresenta na tela todos os amigos do usuario atual
	def mostra_amigos(self, *args):
		# Limpa o grid
		grid_amigos = self.ids.grid_amigos
		grid_amigos.clear_widgets()

		# Busca todos os amigos
		cursor.execute (""" select
								C.Login2
							from
								ConheceNormalizada as C
							where
								C.Login1 = '""" + self.login_usuario_atual + "'")
		amigos = cursor.fetchall()
		self.qtdade_amigos = len(amigos)

		# Cria os botoes
		for amigo in amigos:
			botao_amigo = Button(	text = amigo[0],
									background_color = [.5, .2, .2, 1])
			botao_amigo.bind(on_press = partial(self.define_usuario, amigo[0]))
			grid_amigos.add_widget(botao_amigo)


	# Apresenta na tela todos os filmes curtidos pelo usuario atual
	def mostra_filmes(self, *args):
		# Limpa o grid
		grid_filmes = self.ids.grid_filmes
		grid_filmes.clear_widgets()

		# Busca todos os filmes
		cursor.execute (""" select
								F.Nome_Filme, G.Nota
							from
								GostaFilme as G
								inner join Filme as F on
									G.URI_Filme = F.URI_Filme
							where
								G.Login = '""" + self.login_usuario_atual + "'")
		filmes = cursor.fetchall()

		# Imprime os filmes na tela
		for filme in filmes:
			label_filme = FilmeLabel(	text = filme[0][:-7] + ' - ' + str(filme[1]), # Removendo os ultimos 7 caracteres
										text_size = [grid_filmes.size[0], None],
										font_size = 13)
			grid_filmes.add_widget(label_filme)


	# Apresenta na tela todos os artistas curtidos pelo usuario atual
	def mostra_artistas(self, *args):
		# Limpa o grid
		grid_artistas = self.ids.grid_artistas
		grid_artistas.clear_widgets()

		# Busca todos os artistas
		cursor.execute (""" select
								G.URI_Artista, G.Nota
							from
								GostaArtista as G
							where
								G.Login = '""" + self.login_usuario_atual + "'")
		artistas = cursor.fetchall()

		# Imprime os artistas na tela
		for artista in artistas:
			texto = artista[0][len('http://en.wikipedia.org/wiki/') + 1:] + ' - ' + str(artista[1])
			texto = texto.replace('_', ' ')
			label_artista = FilmeLabel(	text = texto,
										text_size = [grid_artistas.size[0], None],
										font_size = 13)
			grid_artistas.add_widget(label_artista)


	# Apresenta na tela pessoas que o usuario talvez conheca
	def recomenda_amigos(self, *args):
		# Limpa o grid
		grid_recom_amigos = self.ids.grid_recom_amigos
		grid_recom_amigos.clear_widgets()

		# Busca todas as recomendacoes
		recomendados = sugerir_amigos(self.login_usuario_atual, self.grafo_amigos)

		# Imprime na tela
		i = 0
		for pessoa in recomendados:
			label_recom_amigo = FilmeLabel( text = pessoa,
											text_size = [grid_recom_amigos.size[0], None],
											font_size = 13)
			grid_recom_amigos.add_widget(label_recom_amigo)
			i += 1
			if i == 5:
				break


	# Apresenta na tela filmes que talvez a pessoa goste
	def recomenda_filmes(self, *args):
		# Limpa o grid
		grid_recom_filmes = self.ids.grid_recom_filmes
		grid_recom_filmes.clear_widgets()

		# Busca todas as recomendações
		try:
			index = self.usuarios_em_ordem.index(self.login_usuario_atual)
		except:
			return
		nota_filmes_usuario = self.R[index]

		index = 0
		filmes_curtidos = []
		for nota_filme in nota_filmes_usuario:
			if nota_filme >= 4:
				filmes_curtidos.append(self.ordem_filmes[index])
			index += 1

		filmes_curtidos = sorted(filmes_curtidos)

		# Imprime na tela
		i = 0
		for filme in filmes_curtidos:
			print(filme)
			cursor.execute("select Nome_Filme from Filme where URI_Filme = '" + filme.rstrip() + "';")
			titulo = cursor.fetchone()[0]
			print (titulo)
			label_recom_filmes = FilmeLabel(	text = titulo[:-7],
												text_size = [grid_recom_filmes.size[0], None],
												font_size = 13)
			grid_recom_filmes.add_widget(label_recom_filmes)
			i += 1
			if i == 5:
				break
		



	# Apresenta todas as informacoes do usuario atual na tela
	def mostra_informacoes(self, *args):
		self.mostra_amigos()
		self.mostra_filmes()
		self.mostra_artistas()
		self.recomenda_amigos()
		self.recomenda_filmes()
		

	# Tenta carregar informacoes de outro usuario.
	# Se nao der, apenas mantem as informacoes do
	# 	usuario atual
	def define_usuario(self, login, *args):
		cursor.execute("select Nome_Usuario from Usuario as U where U.Login = '" + login + "'")
		try:
			self.nome_usuario_atual = str(cursor.fetchone()[0]).title()
		except:
			return
		self.login_usuario_atual = login
		self.ids.input_pesquisa.text = '' # Limpa a barra de pesquisa
		self.mostra_informacoes()





class RedeSocialApp(App):
	def build(self):
		return RedeSocial()





if __name__ == '__main__':
	RedeSocialApp().run()
	banco.close()