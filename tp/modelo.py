# ##############################################
# MODELO
# ##############################################
from tkinter import ttk
import sqlite3
import re


class ManejadorBd():
	BD = 'estudiantes.db'

	def __init__(self) -> None:
		self.con = self.iniciar_conexion()
		self.crear_tabla()

	def iniciar_conexion(self):
		con = sqlite3.connect(self.BD)
		return con
	
	def crear_tabla(self):
		try:
			cursor = self.con.cursor() 
			# DLL de la tabla
			sql = """
			CREATE TABLE IF NOT EXISTS estudiantes
			(
				id integer PRIMARY KEY AUTOINCREMENT,
				nombre text NOT NULL,
				email text NOT NULL,
				nota real
			)
			"""
			cursor.execute(sql)
			self.con.commit()	
		except Exception as e:
			print("Hay un error:", e)

	def borrar_tabla(self):
		cursor = self.con.cursor() 
		# DLL de la tabla
		sql = 'DROP TABLE IF EXISTS estudiantes'
		cursor.execute(sql)
		self.con.commit()

	def resetear_tabla(self):
		self.borrar_tabla()
		self.crear_tabla()
		print('reseteando BD y actualizando vista')
		

	def insertar_datos_default(self):
		cursor = self.con.cursor() 
		# DML 
		sql = """
		INSERT INTO estudiantes (nombre, email, nota)
			VALUES('Alan Martinez', 'AlanMartinez@hotmail.com', 6.5),
			('Pedro Villanueva', 'PVNueva66@gmail.com', 9),
			('Maria Benitez', 'Mbtez@gmail.com', 10),
			('Gustavo Romanov', 'tavo_14@outlook.com.ar', 2.5),
			('Josefina Cordara', 'JCor95@yahoo.com', 0),
			('Alfredo Gomez', 'GAlfredo@outlook.com.br', 8);
		"""
		cursor.execute(sql)
		self.con.commit()
		

	def traer_datos(self):
		sql = "SELECT * FROM estudiantes ORDER BY id DESC"
		cursor = self.con.cursor()
		datos = cursor.execute(sql)
		resultado = datos.fetchall()
		print('resultado', resultado) # test
		return resultado
	
	def insertar_datos(self, nombre:str, email:str, nota:float):
		cursor = self.con.cursor()
		data = (nombre, email, nota)
		sql = "INSERT INTO estudiantes(nombre, email, nota) VALUES(?, ?, ?)"
		cursor.execute(sql, data)
		self.con.commit()

	def modificar_datos(self, id, nombre:str, email:str, nota:float):
		cursor = self.con.cursor()
		#mi_id = int(mi_id)
		#data = (mi_id,)
		sql = f""" 
		UPDATE estudiantes 
		SET nombre = '{nombre}',
			email = '{email}',
			nota = {nota}
		WHERE id = {id};
		"""
		print('sql ejecutado: ',sql)
		cursor.execute(sql)
		self.con.commit()

	def eliminar_datos(self, id):
		cursor = self.con.cursor()
		#mi_id = int(mi_id)
		data = (id,)
		sql = "DELETE FROM estudiantes WHERE id = ?;"
		cursor.execute(sql, data)
		self.con.commit()

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
			mi_treeview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3]))



	# TODO 1: Areglar return para que devuelva el mensaje del print en una warning.
	# TODO 2: Agregar filtro para 'nota' que sea perteneciente al intervalo [0.0, 10.0] unicamente
	# TODO 3: Agregar filtro para 'nombre' similar a email con regex.
	def alta(self, nombre:str, email:str, nota:float, tree: ttk.Treeview):
		''' Realiza el alta del estudiante. Devuelve True/False '''
		print('Entrando ALTA')
		if( not self.validar_email(email) ):
			print(f"error en campo email: '{email}' no es una direccion de email valida")
			return False
		print('nombre:', nombre, ',', 'email:', email, ',', 'nota:', nota)

		self.bd.insertar_datos(nombre, email, nota)

		print("Alta exitosa")
		self.actualizar_treeview(tree)
		return True
			

	def validar_email(self, email:str):
		''' 
		Devuelve algo analogo a TRUE si el email es una 
		direccion de email VALIDA y algo analogo a FALSE si no lo es
		'''
		PATRON = '^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$'  #regex para el email
		return re.match(PATRON, email) 

			

	def modificar(self, nombre:str, email:str, nota:float, tree: ttk.Treeview): # TODO
		print('Entrando a MODIFICAR')

		valor_seleccionado = tree.selection()
		if not valor_seleccionado:
			print('NO SE SELECCIONO NADA')
			return
		
		if( not self.validar_email(email) ):
			print(f"error en campo email: '{email}' no es una direccion de email valida")
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

		self.bd.modificar_datos(mi_id, nombre, email, nota)

		self.actualizar_treeview(tree)
		print('FIN MODIFICAR')
		

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