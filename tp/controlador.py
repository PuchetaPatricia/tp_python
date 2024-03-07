'''
controlador.py:
	Modulo controlador, el cual funciona mendiante un Modelo y una Vista
	mediando en su interaccion.
'''

from tkinter import Tk
from modelo import Modelo
from vista import Vista

class Controlador():
	''' 
		Clase Controlador. 
		Controla la interaccion entre la vista y el modelo.
	'''
	def __init__(self, modelo:Modelo, vista:Vista):
		'''
		Constructor: Toda instancia de controlador esta definido por un modelo 
		y una vista en particular.
		:param modelo: Instancia de Modelo
		:param vista: Instancia de Vista
		'''
		self.m = modelo
		self.v = vista

	def iniciar_ejecucion(self):
		'''
		Crea y actualiza la ventana principal de la aplicacion e 
		inicia la ejecucion de la aplicacion.
		:returns: None
		'''
		root_tk = Tk()

		tree = self.v.ventana_principal(root_tk, self.m.alta, self.m.modificar, self.m.borrar, self.m.insertar_datos_default, self.m.resetear_tabla) # vista, devuelve objeto treeview

		self.m.actualizar_treeview(tree) # modelo
		root_tk.mainloop()