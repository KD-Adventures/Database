import sqlite3

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty

banco = sqlite3.connect('joaquim.db')
cursor = banco.cursor()

###############################
# Funcoes para mexer no banco #
###############################





###################
# Classes do Kivy #
###################

class RedeSocial(Widget):
	meu_nome = StringProperty(None)
	cursor.execute("SELECT oi FROM Joaquim")
	meu_nome = str(cursor.fetchone()[0])



class RedeSocialApp(App):
	def build(self):
		return RedeSocial()

if __name__ == '__main__':
	RedeSocialApp().run()