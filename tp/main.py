''' 
	Programa "principal". 
	Instancia al controlador, el modelo y la vista.
'''

from controlador import Controlador
from modelo import Modelo
from vista import Vista

if __name__ == '__main__':
	print('Inicio ejecucion del programa')
	m = Modelo()
	v = Vista()
	c = Controlador(m, v)
	c.iniciar_ejecucion()
	print('Fin ejecucion del programa')