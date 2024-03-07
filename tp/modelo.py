'''
modelo.py:
	Representa el modelo logico del programa
'''
from tkinter import ttk
import re
from peewee import *

base_sqlite = SqliteDatabase('base_sqlite.db')

class BaseModel(Model):
    class Meta:
        database = base_sqlite


class Estudiantes(BaseModel):
	'''
		Clase Estudiantes. La usa el ORM para generar
		la tabla de estudiantes en la base de datos.
	'''
    # id = IntegerField(primary_key = True, )  # no es necesario, el ORM ya le agrega un id llamado 'id' por defecto 
	nombre = CharField()
	email = CharField()
	nota = FloatField()

base_sqlite.connect()
base_sqlite.create_tables([Estudiantes])


class ManejadorBd():
	'''
		Clase ManejadorBd encargada de realizar
		todas las operaciones sobre la base de datos
	'''
	def resetear_tabla(self):
		'''
		Borra la tabla y la vuelve a crear vacia.
  		:returns: None
		'''

		base_sqlite.drop_tables([Estudiantes])
		base_sqlite.create_tables([Estudiantes])
		print('reseteando BD y actualizando vista')
		
	def insertar_datos_default(self):
		'''
		Inserta datos dummy en la tabla estudiantes.
  		:returns: None
		'''

		self.insertar_datos('Alan Martinez', 'AlanMartinez@hotmail.com', 6.5)
		self.insertar_datos('Pedro Villanueva', 'PVNueva66@gmail.com', 9)
		self.insertar_datos('Maria Benitez', 'Mbtez@gmail.com', 10)
		self.insertar_datos('Gustavo Romanov', 'tavo_14@outlook.com.ar', 2.5)
		self.insertar_datos('Josefina Cordara', 'JCor95@yahoo.com', 0)
		self.insertar_datos('Alfredo Gomez', 'GAlfredo@outlook.com.br', 8)
		
	def traer_datos(self) -> ModelSelect:
		'''
		Trae todos los datos de la tabla estudiantes.
		:returns: objeto de tipo <class 'peewee.ModelSelect'>
		'''

		resultado = Estudiantes.select()
		print('type(resultado):', type(resultado)) # test       <class 'peewee.ModelSelect'>
		print('resultado', resultado) # test
		return resultado
	
	def insertar_datos(self, nombre:str, email:str, nota:float):
		'''
		Inserta un nuevo registro en la tabla estudiantes.
  		:param nombre: Nombre a insertar
		:param email: Email a insertar
		:param nota: Nota a insertar
  		:returns: None
		'''

		estudiante = Estudiantes()
		estudiante.nombre = nombre
		estudiante.email = email
		estudiante.nota = nota
		estudiante.save()

	def modificar_datos(self, id, nombre:str, email:str, nota:float):
		'''
		Modifica el registro de la tabla estudiantes, con los datos ingresados, segun el id pasado por parametro.
		:param id: id del registro a modificar
		:param nombre: Nombre nuevo
		:param email: Email nuevo
		:param nota: Nota nueva
		:returns: None
		'''

		actualizar = Estudiantes.update(nombre=nombre, email=email, nota=nota).where(Estudiantes.id == id)
		actualizar.execute()

	def eliminar_datos(self, id):
		'''
		Elimina el registro de la tabla estudiante, segun el id pasado por parametro.
		:param id: id del registro a eliminar
		:returns: None
		'''
		Estudiantes.delete_by_id(id)

class Modelo():
	'''
		Clase correspondiente al Modelo. Utiliza un manejador de bases de datos
		llamando al constructor de la clase ManejadorBd
	'''
	def __init__(self):
		self.bd = ManejadorBd()

	def actualizar_treeview(self, mi_treeview: ttk.Treeview):
		'''
		Llama al metodo "traer_datos" del manejador de base de datos y
		actualiza el treeview de la ventana principal.
		:param: Instancia Treeview
  		:returns: None
		'''

		hijos = mi_treeview.get_children()
		for hijo in hijos:
			print('Hijo de treeview a borrar: ', hijo)
			mi_treeview.delete(hijo)

		resultado = self.bd.traer_datos()

		for fila in resultado:
			print('fila',fila)
			mi_treeview.insert("", 0, text=fila.id, values=(fila.nombre, fila.email, fila.nota))


	def alta(self, nombre:str, email:str, nota:float, tree: ttk.Treeview):
		''' 
		Llama al metodo "insertar_datos" del manejador de base de datos para 
		realizar el alta del estudiante. 
  		:param nombre: Nombre a insertar
		:param email: Email a insertar
		:param nota: Nota a insertar
  		:param tree: Instancia Treeview	
		:returns: Devuelve True si se dio el alta correctamente o False si no se pudo dar de alta el registro.
		'''

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
		Valida si el nombre del estudiante coincide con el patron esperado.
		:param nombre: Nombre a validar
  		:returns: Devuelve algo analogo a TRUE si el nombre contiene caracteres a-z y no termina ni comienza en espacios.
		'''

		PATRON = '^[A-Za-z]+(?:[ _-][A-Za-z]+)*$$'  #regex para el nombre del alumno
		return re.match(PATRON, nombre) 

	def validar_email(self, email:str):
		''' 
		Valida si el mail del estudiante coincide con el patron esperado para un mail.
		:param email: Email a validar
  		:returns: Devuelve algo analogo a TRUE si el email es una 
		direccion de email VALIDA y algo analogo a FALSE si no lo es
		'''

		PATRON = '^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$'  #regex para el email
		return re.match(PATRON, email) 
			
	def modificar(self, nombre:str, email:str, nota:float, tree: ttk.Treeview): 
		''' 
		Llama al metodo "modificar_datos" del manejador de base de datos para
		realizar la modificacion del estudiante seleccionado. 
		:param nombre: Nombre a modificar
		:param email: Email a modificar
		:param nota: Nota a modificar
  		:param tree: Instancia Treeview	
		:returns: Devuelve True si se modifico correctamente el registro o False si no se pudo modificar el registro.
		'''

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
		
		print('valor_seleccionado',valor_seleccionado)
		item = tree.item(valor_seleccionado)
		print('item',item)

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
		'''
		Llama al metodo "eliminar_datos" del manejador de base de datos para 
		realizar el borrado del estudiante seleccionado. En caso de no seleccionar nada, se envia una alerta por pantalla.
  		:param tree: Instancia Treeview	
		:returns: None
		'''
		
		print('Entrando a BORRAR')
		valor_seleccionado = tree.selection() 
		if not valor_seleccionado:
			print('NO SE SELECCIONO NADA')
			return
		print('valor_seleccionado',valor_seleccionado)
		item = tree.item(valor_seleccionado)
		print('item',item)
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
		'''
		Llama al metodo "insertar_datos_default" del manejador de base de datos para insertar datos dummy
  		:param tree: Instancia Treeview	
		:returns: None
		'''
		
		self.bd.insertar_datos_default()
		self.actualizar_treeview(tree)

	def resetear_tabla(self, tree: ttk.Treeview):
		'''
		Llama al metodo "resetear_tabla" del manejador de base de datos para borrar la tabla y volver a crearla vacia.
		:param tree: Instancia Treeview	
		:returns: None
		'''

		self.bd.resetear_tabla()
		self.actualizar_treeview(tree)