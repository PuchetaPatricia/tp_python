'''
	vista.py:
		Representa la interfaz del programa con el usuario
'''
from tkinter import Tk, Label, W, E, Entry, Button, StringVar, DoubleVar, ttk
from tkinter.messagebox import showinfo, showwarning
from modelo import Modelo

class Vista():
	'''
		Clase Vista. 
		Administra la vista con la que interactua el usuario.
	'''
	def __init__(self):
		self.objeto_Crud = Modelo()
		
	def limpiar_campos(self, nombre:StringVar, email:StringVar, nota:DoubleVar):
		'''
			Limpia los campos de los Entry de la ventana principal.
		'''
		nombre.set('')
		email.set('')
		nota.set(0.0)

	# TODO 1: Agregar mensaje de razon de falla (ej, email incorrecto)
	# TODO 2: Repetir esta misma funcion pero para modificar/eliminar
	def alta_aux(self, nombre:StringVar, email:StringVar, nota:DoubleVar, tree: ttk.Treeview, alta):
		'''
			Se encarga de solicitar el alta de un nuevo registro al modelo, con los datos ingresados.
			"alta" es una funcion del modelo.
		'''

		try:
			confirmacion_alta = alta(nombre.get(), email.get(), nota.get(), tree) #type: bool
			if confirmacion_alta == False:
				print('ALTA FALLIDA')
				showwarning('Mensaje','Alta fallida')
			else:
				print('ALTA CORRECTA')
				showinfo('Mensaje','Alta correcta')
				self.limpiar_campos(nombre, email, nota)

		except Exception as e:
			showwarning('Mensaje', f'Alta fallida. Error en el ingreso de datos.')
			print(f'Excepcion: {e}')

	def modificar_aux(self, nombre:StringVar, email:StringVar, nota:DoubleVar, tree: ttk.Treeview, modificar):
		'''
			Se encarga de solicitar la modificacion de un registro al modelo, con los datos ingresados y el registro seleccionado del treeview.
			"modificar" es una funcion del modelo.
		'''

		try:
			confirmacion_modificar = modificar(nombre.get(), email.get(), nota.get(), tree) #type: bool

			if confirmacion_modificar == False:
				print('MODIFICACION FALLIDA')
				showwarning('Mensaje','Modificacion fallida')
			else:
				print('MODIFICACION CORRECTA')
				showinfo('Mensaje','Modificacion correcta')
				self.limpiar_campos(nombre, email, nota)
				
		except Exception as e:
			showwarning('Mensaje', f'Modificacion fallida. Error en el ingreso de datos.')
			print(f'Excepcion: {e}')


	# --------------------------------------------------
	# TREEVIEW
	# --------------------------------------------------
	def crear_treeview(self, root: Tk) -> ttk.Treeview:
		'''
			Crea la estructura del treeview mostrado en la ventana principal.
		'''

		tree = ttk.Treeview(root)
		tree["columns"]=("col1", "col2", "col3")
		tree.column("#0", width=90, minwidth=50, anchor=W)
		tree.column("col1", width=200, minwidth=80)
		tree.column("col2", width=200, minwidth=80)
		tree.column("col3", width=200, minwidth=80)
		tree.heading("#0", text="ID")
		tree.heading("col1", text="Nombre")
		tree.heading("col2", text="Email")
		tree.heading("col3", text="Nota")
		tree.grid(row=10, column=0, columnspan=4)
		return tree

	def ventana_principal(self, root:Tk, alta, modificar, borrar, insertar_datos_default, resetear_tabla) -> ttk.Treeview:
		'''
			Genera la vista principal.
			Utiliza las funciones 'alta', 'modificar', 'borrar', 'insertar_datos_default' y 'resetear_tabla' del modelo.
		'''
		root.title("CRUD de estudiantes")
		
				
		titulo = Label(root, text = "Ingrese la informacion del alumno", 
					bg = "dark green", fg = "thistle1", height = 1, width = 60)
		titulo.grid(row = 0, column = 0, columnspan = 4, padx = 1, pady = 1, sticky = W+E)

		estudiante = Label(root, text = "Nombre")
		estudiante.grid(row = 1, column = 0, sticky = W)
		email = Label(root, text = "Email")
		email.grid(row = 2, column = 0, sticky = W)
		nota = Label(root, text = "Nota")
		nota.grid(row = 3, column = 0, sticky = W)

		# Defino variables para tomar valores de campos de entrada
		nombre_var, email_var, nota_var = StringVar(), StringVar(), DoubleVar()
		ANCHO_ENTRADAS = 20

		entrada1 = Entry(root, textvariable = nombre_var, width = ANCHO_ENTRADAS) 
		entrada1.grid(row = 1, column = 1)
		entrada2 = Entry(root, textvariable = email_var, width = ANCHO_ENTRADAS) 
		entrada2.grid(row = 2, column = 1)
		entrada3 = Entry(root, textvariable = nota_var, width = ANCHO_ENTRADAS) 
		entrada3.grid(row = 3, column = 1)

		tree = self.crear_treeview(root)

		# Alta
		boton_alta = Button(root, text = "Alta", command = lambda : self.alta_aux(nombre_var, email_var, nota_var, tree, alta)) 
		boton_alta.grid(row = 6, column = 1)

		# Modificacion
		boton_modificar = Button(root, text = "Modificar", command = lambda : self.modificar_aux(nombre_var, email_var, nota_var, tree, modificar))
		boton_modificar.grid(row = 7, column = 1)

		# Borrado
		boton_borrar = Button(root, text = "Borrar", command = lambda : borrar(tree)) 
		boton_borrar.grid(row = 8, column = 1)

		# Insercion de datos dummy
		boton_reset = Button(root, text = "Poblar tabla BD", command = lambda : insertar_datos_default(tree)) 
		boton_reset.grid(row = 6, column = 3)

		# Limpieza de la tabla, borrado de todos los datos
		boton_reset = Button(root, text = "Resetear tabla BD", command = lambda : resetear_tabla(tree)) 
		boton_reset.grid(row = 7, column = 3)

		return tree