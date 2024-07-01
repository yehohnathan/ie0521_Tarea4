from math import log2, floor
from random import randint


class cache:
    def __init__(self, cache_capacity, cache_assoc, block_size, repl_policy):
        """
        Inicializador de atributos de la clase caché de la parte 1.
        """
        # Contador del total de accesos que ha tenido el caché
        self.total_access = 0
        # Contador del total de misses que ha tenido el caché
        self.total_misses = 0

        # Atributos que contienen las entradas de la clase (se entiende su uso)
        self.cache_capacity = int(cache_capacity)
        self.cache_assoc = int(cache_assoc)
        self.block_size = int(block_size)
        self.repl_policy = repl_policy

        # Bit del offset = log2(Tamaño del bloque)
        self.bits_offset = log2(self.block_size)
        # Número de bloques = Capacidad de caché / Tamaño del bloque
        self.num_blocks = (self.cache_capacity * 1024) / self.block_size
        # Número de sets (conjuntos) = Número de bloques / Asociatividad
        self.num_sets = int(self.num_blocks / self.cache_assoc)
        # Bits de índice = log2(Número de sets)
        self.bits_index = int(log2(self.num_sets))

        # Creación de las tablas:
        # |-- INDEX --|-- V --|-- TAG --|-- DATA --| -> Mapeo directo
        # INDEX nunca varia.
        # V, TAG, DATA: row = num_sets ^ column = asociatividad
        # El manejo de DATA varía según la política de reemplazo
        self.valid_table = [[False] * self.cache_assoc
                            for row in range(self.num_sets)]
        self.tag_table = [[0] * self.cache_assoc
                          for row in range(self.num_sets)]
        self.repl_data_table = [[0] * self.cache_assoc
                                for row in range(self.num_sets)]

    def print_info(self):
        """
        Muestra los parámetros usados para la simulación
        """
        print("Parámetros del caché:")
        print("\tCapacidad:\t\t"+str(self.cache_capacity)+"kB")
        print("\tAssociatividad:\t\t"+str(self.cache_assoc))
        print("\tTamaño de Bloque:\t"+str(self.block_size)+"B")
        print("\tPolítica de Reemplazo:\t", end="")
        print("LRU") if self.repl_policy == "l" else print("Random")

    def print_stats(self):
        """
        Muestra los resultados obtenidos de la simulación

        Returna:
            string: Porcentaje misses y miss rate obtenidos.
        """
        print("Resultados de la simulación")
        miss_rate = (100.0*self.total_misses) / self.total_access
        miss_rate = "{:.3f}".format(miss_rate)
        result_str = str(self.total_misses)+","+miss_rate+"%"
        print(result_str)

    def access(self, access_type, address):
        # Se encuentra la palabra dentro del bloque. Obtiene los últimos
        # k bits de address.
        # byte_offset = int(address % (2 ** self.bits_offset))

        # Se utiliza para encontrar la posición del bloque en el caché. Elimina
        # los últimos k bits de address, luego obtiene los siguientes i bits de
        # address.
        index = int(floor(address / (2 ** self.bits_offset)) %
                    (2 ** self.bits_index))
        # Identifica la dirección exacta que está almacenada en esa posición.
        # Elimina los últimos k + i bits de address, luego obtiene los
        # siguientes t bits de address.
        tag = int(floor(address / (2 ** (self.bits_offset + self.bits_index))))

        # Toma com suposición que no hubo miss. Antes de verificar hit.
        miss_occurred = False

        # Toma decisiones según el resultado del hit
        if self.hit_ask(index, tag) == -1:
            # Pone el dato en el caché por haber miss
            self.put_in_cache(index, tag)
            # Incrementa el total de misses
            self.total_misses += 1
            # Indica que al final si hubo miss
            miss_occurred = True

        # Incrementa la cantidad de accesos
        self.total_access += 1

        # Retorna el resultado del acceso
        return miss_occurred

    def hit_ask(self, index, tag):
        """
        Verifica en las direcciones obtenidas si hubo un hit o no.

        Args:
            index (int): Se utiliza para encontrar la posición del bloque en
            el caché.
            tag (int): Identifica la dirección exacta que está almacenada en
            esa posición.
        Returns:
            int: posición de la columna donde hubo hit, sino returna -1.
        """
        # Busca si hubo hit en una de las columnas de la fila
        for column in range(self.cache_assoc):
            # Se pregunta si la entrada de valid es True (hay dato) y luego si
            # coincide con el tag (se llegó a la dirección exacta).
            if self.valid_table[index][column] and self.tag_table[index][column] == tag:
                # Hubo hit en la columna de asociatividad:
                return column
            # En términos de hit, no hubo hit.
        return -1

    def put_in_cache(self, index, tag):
        # Se supone que no hay valor vació:
        empty_block = False
        block = -1

        # Verifica si en la posición dada por la dirección hay datos, sino,
        # actualiza el tag e indica que ahora si hay un dato (True).
        for column in range(self.cache_assoc):
            if not self.valid_table[index][column]:
                self.tag_table[index][column] = tag
                self.valid_table[index][column] = True
                # Se indica que es el bloque más recientemente usado
                self.repl_data_table[index][column] = self.cache_assoc - 1
                empty_block = True
                block = column
                break

        if not empty_block:
            # Se procede a actualizar el caché según LRU:
            if self.repl_policy == "l":
                # Se obtiene un valor más grande que la asociatividad
                min_lru = self.cache_assoc + 1

                # Se busca la columna con el LRU más bajo en la fila
                for column in range(self.cache_assoc):
                    if self.repl_data_table[index][column] < min_lru:
                        min_lru = column

                self.tag_table[index][min_lru] = tag
                self.repl_data_table[index][min_lru] = self.cache_assoc - 1
                self.valid_table[index][min_lru] = True

            # Politica Random
            elif self.repl_policy == "r":
                # Se obtiene un valor random de columna a eliminar
                column = randint(0, self.cache_assoc - 1)
                self.tag_table[index][column] = tag
                self.repl_data_table[index][column] = self.cache_assoc - 1

        if self.repl_policy == 'l':
            for column in range(self.cache_assoc):
                # Se coincide con la columna del valor recien reemplazado lo
                # ignora
                if column == block:
                    continue
                else:
                    self.repl_data_table[index][column] -= 1
