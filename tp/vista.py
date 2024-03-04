# ##############################################
# VISTA
# ##############################################
from tkinter import Tk, Label, W, E, Entry, Button, StringVar, DoubleVar, ttk
from tkinter.messagebox import showinfo, showwarning


class Vista():
	def limpiar_campos(self, nombre:StringVar, email:StringVar, nota:DoubleVar):
		nombre.set('')
		email.set('')
		nota.set(0.0)

	# TODO 1: Agregar mensaje de razon de falla (ej, email incorrecto)
	# TODO 2: Repetir esta misma funcion pero para modificar/eliminar
	def alta_aux(self, nombre:StringVar, email:StringVar, nota:DoubleVar, tree: ttk.Treeview, alta):
		''' "alta" es una funcion que viene del modelo '''
		confirmacion_alta = alta(nombre.get(), email.get(), nota.get(), tree) #type: bool
		if confirmacion_alta:
			print('ALTA CORRECTA')
			showinfo('Mensaje','Alta correcta')
			self.limpiar_campos(nombre, email, nota)
		else:
			print('ALTA FALLIDA')
			showwarning('Mensaje','Alta fallida')

	def crear_treeview(self, root: Tk) -> ttk.Treeview:
		# --------------------------------------------------
		# TREEVIEW
		# --------------------------------------------------
		tree = ttk.Treeview(root)
		# print('t1 imprimiendo arbol (tree):',tree.)     #.!treeview
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

	def ventana_principal(self, root:Tk, alta, modificar, borrar, insertar_datos_default, resetear_tabla):
		'''
			Genera la vista principal.
			
			alta, modificar, borrar, insertar_datos_default y resetear_tabla son funciones
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

		boton_alta = Button(root, text = "Alta", command = lambda : self.alta_aux(nombre_var, email_var, nota_var, tree, alta)) 
		boton_alta.grid(row = 6, column = 1)

		boton_modificar = Button(root, text = "Modificar", command = lambda : modificar(nombre_var.get(), email_var.get(), nota_var.get(), tree)) 
		boton_modificar.grid(row = 7, column = 1)

		boton_borrar = Button(root, text = "Borrar", command = lambda:borrar(tree)) 
		boton_borrar.grid(row = 8, column = 1)

		boton_reset = Button(root, text = "Poblar tabla BD", command = lambda:insertar_datos_default(tree)) 
		boton_reset.grid(row = 6, column = 3)

		boton_reset = Button(root, text = "Resetear tabla BD", command = lambda:resetear_tabla(tree)) 
		boton_reset.grid(row = 7, column = 3)

		return tree