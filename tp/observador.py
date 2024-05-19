import os
from datetime import datetime

class Sujeto:
    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def quitar(self, obj):
        self.observadores.remove(obj)

    def notificar(self, *args):
        for observador in self.observadores:
            observador.update(*args)
            observador.guardar_log_observer(*args)


class Observador:
    def update(self, *args):
        raise NotImplementedError("Delegación de actualización")
    
    def guardar_log_observer(*args):
        BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
        ruta = os.path.join(BASE_DIR, "observador_logs.txt")
        log_function = open(ruta, "a")
        print(
            datetime.now().strftime("%H:%M:%S--%d/%m/%y"),
            "- Observador",
            "\nDatos:",
            args[1],
            "\n",
            file=log_function,
        )


class ConcreteObserverA(Observador):
    def __init__(self, obj):
        self.observado_a = obj
        self.observado_a.agregar(self)

    def update(self, *args):
        print('---'*25)
        print("Observador -- Actualización de estado")
        print("Aquí están los parámetros: ", args[0])
        print('---'*25)
