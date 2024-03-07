# ##############################################
# MODELO
# ##############################################
from tkinter import ttk
import re
from peewee import *

base_sqlite = SqliteDatabase('base_sqlite.db')

class BaseModel(Model):
    class Meta:
        database = base_sqlite

class Estudiantes(BaseModel):
    # id = IntegerField(primary_key = True, )  # no es necesario, el ORM ya le agrega un id llamado 'id' por defecto 
    nombre = CharField()
    email = CharField()
    nota = FloatField()

base_sqlite.connect()
base_sqlite.create_tables([Estudiantes])

	
# mi modelo original

# id integer PRIMARY KEY AUTOINCREMENT,
# nombre text NOT NULL,
# email text NOT NULL,
# nota real



class ManejadorBd():
	def resetear_tabla(self):
		base_sqlite.drop_tables([Estudiantes])
		base_sqlite.create_tables([Estudiantes])
		print('reseteando BD y actualizando vista')
		
	def insertar_datos_default(self):
		self.insertar_datos('Alan Martinez', 'AlanMartinez@hotmail.com', 6.5)
		self.insertar_datos('Pedro Villanueva', 'PVNueva66@gmail.com', 9)
		self.insertar_datos('Maria Benitez', 'Mbtez@gmail.com', 10)
		self.insertar_datos('Gustavo Romanov', 'tavo_14@outlook.com.ar', 2.5)
		self.insertar_datos('Josefina Cordara', 'JCor95@yahoo.com', 0)
		self.insertar_datos('Alfredo Gomez', 'GAlfredo@outlook.com.br', 8)
		
	def traer_datos(self):
		resultado = Estudiantes.select()
		print('type(resultado):', type(resultado)) # test       <class 'peewee.ModelSelect'>
		print('resultado', resultado) # test
		return resultado
	
	def insertar_datos(self, nombre:str, email:str, nota:float):
		estudiante = Estudiantes()
		estudiante.nombre = nombre
		estudiante.email = email
		estudiante.nota = nota
		estudiante.save()

	def modificar_datos(self, id, nombre:str, email:str, nota:float):
		actualizar = Estudiantes.update(nombre=nombre, email=email, nota=nota).where(Estudiantes.id == id)
		actualizar.execute()

	def eliminar_datos(self, id):
		#registro_a_borrar = Estudiantes.get( Estudiantes.id == id ) #type: Estudiantes
		#registro_a_borrar.delete_instance()
		
		# encontre este metodo 
		Estudiantes.delete_by_id(id)

class Modelo():
	def __init__(self):
		self.bd = ManejadorBd()

	def actualizar_treeview(self, mi_treeview: ttk.Treeview):
		'''Actualiza la vista'''
		hijos = mi_treeview.get_children()
		for hijo in hijos:
			print('Hijo de treeview a borrar: ', hijo)
			mi_treeview.delete(hijo)

		resultado = self.bd.traer_datos()

		for fila in resultado:
			print('fila',fila)
			mi_treeview.insert("", 0, text=fila.id, values=(fila.nombre, fila.email, fila.nota))


	# TODO 1: Areglar return para que devuelva el mensaje del print en una warning.
	# TODO 2: Agregar filtro para 'nota' que sea perteneciente al intervalo [0.0, 10.0] unicamente
	def alta(self, nombre:str, email:str, nota:float, tree: ttk.Treeview):
		''' Realiza el alta del estudiante. Devuelve True/False '''
		print('Entrando ALTA')
		if( not self.validar_email(email) ):
			print(f"error en campo email: '{email}' no es una direccion de email valida")
			return False
		
		if( not self.validar_nombre(nombre) ):
			print(f"error en campo nombre: '{nombre}' no es un nombre de estudiante valido.")
			return False
		
		print('nombre:', nombre, ',', 'email:', email, ',', 'nota:', nota)

		self.bd.insertar_datos(nombre, email, nota)

		print("Alta exitosa")
		self.actualizar_treeview(tree)
		return True

	def validar_nombre(self, nombre:str):
		''' 
		Devuelve algo analogo a TRUE si el nombre contiene caracteres a-z y no termina ni comienza en espacios.
		'''
		PATRON = '^[A-Za-z]+(?:[ _-][A-Za-z]+)*$$'  #regex para el nombre del alumno
		return re.match(PATRON, nombre) 

	def validar_email(self, email:str):
		''' 
		Devuelve algo analogo a TRUE si el email es una 
		direccion de email VALIDA y algo analogo a FALSE si no lo es
		'''
		PATRON = '^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$'  #regex para el email
		return re.match(PATRON, email) 
			
	def modificar(self, nombre:str, email:str, nota:float, tree: ttk.Treeview): 
		''' Realiza la modificacion del estudiante. Devuelve True/False '''
		print('Entrando a MODIFICAR')

		valor_seleccionado = tree.selection()
		if not valor_seleccionado:
			print('NO SE SELECCIONO NADA')
			return False
		
		if( not self.validar_email(email) ):
			print(f"error en campo email: '{email}' no es una direccion de email valida")
			return False
		
		if( not self.validar_nombre(nombre) ):
			print(f"error en campo nombre: '{nombre}' no es un nombre de estudiante valido.")
			return False
		
		print('valor_seleccionado',valor_seleccionado)   #('I005',)
		item = tree.item(valor_seleccionado)
		print('item',item)    # item {'text': 26, 'image': '', 'values': ['Alfredo Gomez', 'GAlfredo@s': ''}

		print("item['text']",item['text'])
		mi_id = item['text']
		print(f"Valores del item con id = {item['text']}:")
		lista_iterable = ['nombre','email','nota']
		for key, value in zip(lista_iterable, item['values']):
			print(f'{key}: {value}')

		self.bd.modificar_datos(mi_id, nombre, email, nota)

		self.actualizar_treeview(tree)
		print('Modificacion Exitosa')
		return True
		

	def borrar(self, tree: ttk.Treeview):
		print('Entrando a BORRAR')
		valor_seleccionado = tree.selection() 
		if not valor_seleccionado:
			print('NO SE SELECCIONO NADA')
			return
		print('valor_seleccionado',valor_seleccionado)   #('I005',)
		item = tree.item(valor_seleccionado)
		print('item',item)    #{'text': 5, 'image': '', 'values': ['daSDasd', '13.0', '2.0'], 'open': 0, 'tags': ''}
		print("item['text']",item['text'])
		mi_id = item['text']
		
		print(f"Valores del item con id = {item['text']}:")
		lista_iterable = ['nombre','email','nota']
		for key, value in zip(lista_iterable, item['values']):
			print(f'{key}: {value}')

		self.bd.eliminar_datos(mi_id)
		tree.delete(valor_seleccionado)
		print('FIN BORRAR')

	def insertar_datos_default(self, tree: ttk.Treeview):
		self.bd.insertar_datos_default()
		self.actualizar_treeview(tree)

	def resetear_tabla(self, tree: ttk.Treeview):
		self.bd.resetear_tabla()
		self.actualizar_treeview(tree)