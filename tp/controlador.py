'''
	Modulo controlador. 
'''

from tkinter import Tk
from modelo import Modelo
from vista import Vista

class Controlador():
	def __init__(self, modelo:Modelo, vista:Vista):
		self.m = modelo
		self.v = vista

	def iniciar_ejecucion(self):
		'''
			Crea y actualiza la ventana principal de la aplicacion e 
			inicia la ejecucion de la aplicacion.
		'''
		root_tk = Tk()

		tree = self.v.ventana_principal(root_tk, self.m.alta, self.m.modificar, self.m.borrar, self.m.insertar_datos_default, self.m.resetear_tabla) # vista, devuelve objeto treeview

		self.m.actualizar_treeview(tree) # modelo
		root_tk.mainloop()