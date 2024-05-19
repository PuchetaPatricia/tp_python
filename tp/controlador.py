'''
	controlador.py:
		Modulo controlador, el cual funciona mendiante un Modelo y una Vista
		mediando en su interaccion.
'''

from tkinter import Tk
from modelo import Modelo
from vista import Vista
import observador 

class Controlador():
	''' 
		Clase Controlador. 
		Controla la interaccion entre la vista y el modelo.
	'''
	def __init__(self, modelo:Modelo, vista:Vista):
		'''
		Constructor: Toda instancia de controlador esta definido por un modelo 
		y una vista en particular.
		'''
		self.m = modelo
		self.v = vista

		

	def iniciar_ejecucion(self):
		'''
		Crea y actualiza la ventana principal de la aplicacion e 
		inicia la ejecucion de la aplicacion.
		'''
		root_tk = Tk()

		tree = self.v.ventana_principal(root_tk, self.m.alta, self.m.modificar, self.m.borrar, self.m.insertar_datos_default, self.m.resetear_tabla) # vista, devuelve objeto treeview
		
		self.observador = observador.ConcreteObserverA(self.v.objeto_Crud)
		self.m.actualizar_treeview(tree) # modelo
		root_tk.mainloop()
		self.v.stop_server()