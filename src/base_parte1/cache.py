from math import log2, floor

class cache:
    def __init__(self, cache_capacity, cache_assoc, block_size, repl_policy):
        #Escriba aquí el init de la clase
        self.total_access = 0
        self.total_misses = 0
 
        self.cache_capacity = int(cache_capacity)
        self.cache_assoc = int(cache_assoc)
        self.block_size = int(block_size)
        self.repl_policy = repl_policy

    def print_info(self):
        print("Parámetros del caché:")
        print("\tCapacidad:\t\t\t"+str(self.cache_capacity)+"kB")
        print("\tAssociatividad:\t\t\t"+str(self.cache_assoc))
        print("\tTamaño de Bloque:\t\t\t"+str(self.block_size)+"B")
        print("\tPolítica de Reemplazo:\t\t\t"+str(self.repl_policy))

    def print_stats(self):
        print("Resultados de la simulación")
        miss_rate = (100.0*self.total_misses) / self.total_access
        miss_rate = "{:.3f}".format(miss_rate)
        result_str = str(self.total_misses)+","+miss_rate+"%"
        print(result_str)

    def access(self, access_type, address):
        #Escriba aquí el código para procesar el acceso al caché
        #La siguiente línea es solo para que funcione la prueba
        #Quítela para implementar su código
        print("Esto es un acceso")
