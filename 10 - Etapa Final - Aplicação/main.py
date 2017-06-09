import sqlite3
import time
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

banco = sqlite3.connect('BANCO.DB')
cursor = banco.cursor()


class FilmeLabel(Label):
	pass


class RedeSocial(GridLayout):

	nome_usuario_atual = StringProperty()
	login_usuario_atual = StringProperty()
	qtdade_amigos = NumericProperty()


	# Construtor
	def __init__(self, **kwargs):
		super().__init__()
		Clock.schedule_once(partial(self.define_usuario, 'lucasfreitas'), .5)
		# Esse clock é necessário pra dar tempo do Kivy carregar tudo antes de executar a
		# funcao "define_usuario" pela primeira vez



	# Apresenta na tela todos os amigos do usuario atual
	def mostra_amigos(self, *args):
		# Limpa o grid
		grid_amigos = self.ids.grid_amigos
		grid_amigos.clear_widgets()

		# Busca todos os amigos
		cursor.execute (""" select
								Conhece.Login2
							from
								Conhece
							where
								Conhece.Login1 = '""" + self.login_usuario_atual + "'")
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
								F.Nome_Filme
							from
								GostaFilme as G
								inner join Filme as F on
									G.URI_Filme = F.URI_Filme
							where
								G.Login = '""" + self.login_usuario_atual + "'")
		filmes = cursor.fetchall()

		# Imprime os filmes na tela
		for filme in filmes:
			label_filme = FilmeLabel(text = filme[0][:-7], text_size = [grid_filmes.size[0], None])
			grid_filmes.add_widget(label_filme)




	# Apresenta todas as informacoes do usuario atual na tela
	def mostra_informacoes(self, *args):
		self.mostra_amigos()
		self.mostra_filmes()
		


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