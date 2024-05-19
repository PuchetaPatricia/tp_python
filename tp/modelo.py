'''
	modelo.py:
		Representa el modelo logico del programa
'''
from tkinter import ttk
import re
import os
from peewee import *
from datetime import datetime
from observador import Sujeto, ConcreteObserverA

# ***** DECORADORES *****

# Decorador para el metodo alta
def decorador_ingreso_registro(func):
    def envoltura(*args, **kwargs):
        data_ejecucion = func(*args, **kwargs)
        if data_ejecucion:
            print("Decorador -- Se ejecuto el metodo de alta")
            guardar_log(func.__name__, data_ejecucion)
            print('---'*25)
        else:
            return data_ejecucion

    return envoltura

# Decorador para el metodo de borrado
def decorador_eliminar_registro(func):
    def envoltura(*args, **kwargs):
        data_ejecucion = func(*args, **kwargs)
        if data_ejecucion != None:
            print("Decorador -- Se ejecuto el metodo de borrado")
            guardar_log(func.__name__, data_ejecucion)
            print('---'*25)
        else:
            return data_ejecucion
    return envoltura

# Decorador para el metodo modificar
def decorador_actualizacion_registro(func):
    def envoltura(*args, **kwargs):
        data_ejecucion = func(*args, **kwargs)
        if data_ejecucion != False:
            print("Decorador -- Se ejecuto el metodo modificar")
            guardar_log(func.__name__, data_ejecucion)
            print('---'*25)
        else:
            return data_ejecucion
    return envoltura


# Funcion para guardar un log en un archivo txt
def guardar_log(parameter, data):
    BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
    ruta = os.path.join(BASE_DIR, "logs.txt")
    log_function = open(ruta, "a")
    print(
        datetime.now().strftime("%H:%M:%S--%d/%m/%y"),
        "- Se utilizo el metodo",
        parameter,
        "\nDatos:",
        data,
        "\n",
        file=log_function,
    )


# ***** BASE *****

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
		'''

		base_sqlite.drop_tables([Estudiantes])
		base_sqlite.create_tables([Estudiantes])
		print('reseteando BD y actualizando vista')
		
	def insertar_datos_default(self):
		'''
			Inserta datos dummy en la tabla estudiantes.
		'''

		self.insertar_datos('Alan Martinez', 'AlanMartinez@hotmail.com', 6.5)
		self.insertar_datos('Pedro Villanueva', 'PVNueva66@gmail.com', 9)
		self.insertar_datos('Maria Benitez', 'Mbtez@gmail.com', 10)
		self.insertar_datos('Gustavo Romanov', 'tavo_14@outlook.com.ar', 2.5)
		self.insertar_datos('Josefina Cordara', 'JCor95@yahoo.com', 0)
		self.insertar_datos('Alfredo Gomez', 'GAlfredo@outlook.com.br', 8)
		
	def traer_datos(self):
		'''
			Trae todos los datos de la tabla estudiantes.
			Devuelve un objeto de tipo <class 'peewee.ModelSelect'>
		'''

		resultado = Estudiantes.select()
		return resultado
	
	def insertar_datos(self, nombre:str, email:str, nota:float):
		'''
			Inserta un nuevo registro en la tabla estudiantes.
		'''

		estudiante = Estudiantes()
		estudiante.nombre = nombre
		estudiante.email = email
		estudiante.nota = nota
		estudiante.save()

	def modificar_datos(self, id, nombre:str, email:str, nota:float):
		'''
			Modifica el registro de la tabla estudiantes, con los datos ingresados, segun el id pasado por parametro.
		'''

		actualizar = Estudiantes.update(nombre=nombre, email=email, nota=nota).where(Estudiantes.id == id)
		actualizar.execute()

	def eliminar_datos(self, id):
		'''
			Elimina el registro de la tabla estudiante, segun el id pasado por parametro.
		'''
		Estudiantes.delete_by_id(id)

class Modelo(Sujeto):
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
		'''

		hijos = mi_treeview.get_children()
		for hijo in hijos:
			# print('Hijo de treeview a borrar: ', hijo)
			mi_treeview.delete(hijo)

		resultado = self.bd.traer_datos()

		for fila in resultado:
			# print('fila',fila)
			mi_treeview.insert("", 0, text=fila.id, values=(fila.nombre, fila.email, fila.nota))

	@decorador_ingreso_registro
	def alta(self, nombre:str, email:str, nota:float, tree: ttk.Treeview):
		''' 
			Llama al metodo "insertar_datos" del manejador de base de datos para 
			realizar el alta del estudiante.
			Devuelve True si se dio el alta correctamente o False si no se pudo dar de alta el registro.
		'''
		print('---'*25)
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
		self.notificar('Alta ' + 'Nombre: ' + nombre + ' Email: ' + email + ' Nota: ' + str(nota))
		return 'Nombre: ' + nombre + ' Email: ' + email + ' Nota: ' + str(nota)

	def validar_nombre(self, nombre:str):
		''' 
			Valida si el nombre del estudiante coincide con el patron esperado.
			Devuelve algo analogo a TRUE si el nombre contiene caracteres a-z y no termina ni comienza en espacios.
		'''

		PATRON = '^[A-Za-z]+(?:[ _-][A-Za-z]+)*$$'  #regex para el nombre del alumno
		return re.match(PATRON, nombre) 

	def validar_email(self, email:str):
		''' 
			Valida si el mail del estudiante coincide con el patron esperado para un mail.
			Devuelve algo analogo a TRUE si el email es una 
			direccion de email VALIDA y algo analogo a FALSE si no lo es
		'''

		PATRON = '^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$'  #regex para el email
		return re.match(PATRON, email) 
			
	@decorador_actualizacion_registro
	def modificar(self, nombre:str, email:str, nota:float, tree: ttk.Treeview): 
		''' 
			Llama al metodo "modificar_datos" del manejador de base de datos para
			realizar la modificacion del estudiante seleccionado. 
			Devuelve True si se modifico correctamente el registro o False si no se pudo modificar el registro.
		'''
		print('---'*25)
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

		mi_id = item['text']
		print(f"Valores del item con id = {item['text']}:")
		lista_iterable = ['nombre','email','nota']
		for key, value in zip(lista_iterable, item['values']):
			print(f'{key}: {value}')

		self.bd.modificar_datos(mi_id, nombre, email, nota)

		self.actualizar_treeview(tree)
		print('Modificacion Exitosa')
		self.notificar('Modificacion ' + 'Id: ' + str(mi_id) + ' Nombre: ' + nombre + ' Email: ' + email + ' Nota: ' + str(nota))
		return   'Id: ' + str(mi_id) + ' Nombre: ' + nombre + ' Email: ' + email + ' Nota: ' + str(nota)
		
	@decorador_eliminar_registro
	def borrar(self, tree: ttk.Treeview):
		'''
			Llama al metodo "eliminar_datos" del manejador de base de datos para 
			realizar el borrado del estudiante seleccionado. En caso de no seleccionar nada, se envia una alerta por pantalla.
		'''
		print('---'*25)
		print('Entrando a BORRAR')
		valor_seleccionado = tree.selection() 
		if not valor_seleccionado:
			print('NO SE SELECCIONO NADA')
			return 
		print('valor_seleccionado',valor_seleccionado)
		item = tree.item(valor_seleccionado)
		print('item',item)

		mi_id = item['text']
		
		print(f"Valores del item con id = {item['text']}:")
		lista_iterable = ['nombre','email','nota']
		for key, value in zip(lista_iterable, item['values']):
			print(f'{key}: {value}')

		self.bd.eliminar_datos(mi_id)
		tree.delete(valor_seleccionado)
		print('FIN BORRAR')
		self.notificar('Borrado ' + 'Id: ' + str(item['text']) + ' Nombre: ' + item['values'][0] + ' Email: ' + item['values'][1]  + ' Nota: ' + str(item['values'][2]))
		return 'Id: ' + str(item['text']) + ' Nombre: ' + item['values'][0] + ' Email: ' + item['values'][1]  + ' Nota: ' + str(item['values'][2] )
		

	def insertar_datos_default(self, tree: ttk.Treeview):
		'''
			Llama al metodo "insertar_datos_default" del manejador de base de datos para insertar datos dummy.
		'''
		
		self.bd.insertar_datos_default()
		self.actualizar_treeview(tree)

	def resetear_tabla(self, tree: ttk.Treeview):
		'''
			Llama al metodo "resetear_tabla" del manejador de base de datos para borrar la tabla y volver a crearla vacia.
		'''

		self.bd.resetear_tabla()
		self.actualizar_treeview(tree)