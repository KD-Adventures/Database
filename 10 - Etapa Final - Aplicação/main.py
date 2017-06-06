import sqlite3

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
#from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
from functools import partial

banco = sqlite3.connect('BANCO.DB')
cursor = banco.cursor()


class RedeSocial(GridLayout):
	nome_usuario_atual = StringProperty()
	login_usuario_atual = StringProperty()
	qtdade_amigos = NumericProperty(3)


	# Apresenta todas as informacoes na tela
	def mostra_informacoes(self, *args):
		grid_amigos = self.ids.grid_amigos
		grid_amigos.clear_widgets()
		cursor.execute (""" select
								Conhece.Login2
							from
								Conhece
							where
								Conhece.Login1 = '""" + self.login_usuario_atual + "'")
		amigos = cursor.fetchall()
		self.qtdade_amigos = len(amigos)
		for amigo in amigos:
			botao_amigo = Button(	text = amigo[0],
									size_hint_y = 0.5,
									background_color = [.5, .2, .2, 1])
			botao_amigo.bind(on_press = partial(self.define_usuario, amigo[0]))
			grid_amigos.add_widget(botao_amigo)


	# Tenta carregar informacoes de outro usuario.
	# Se nao der, apenas mantem as informacoes do
	# 	usuario atual
	def define_usuario(self, login, *args):
		cursor.execute("select Nome_Usuario from Usuario as U where U.Login = '" + login + "'")
		try:
			backup = self.nome_usuario_atual
			self.nome_usuario_atual = str(cursor.fetchone()[0]).title()
			self.login_usuario_atual = login
		except:
			self.nome_usuario_atual = backup
			return
		self.mostra_informacoes()


class RedeSocialApp(App):
	def build(self):
		rede = RedeSocial()
		rede.define_usuario('lucasfreitas')
		return rede


if __name__ == '__main__':
	RedeSocialApp().run()
	banco.close()