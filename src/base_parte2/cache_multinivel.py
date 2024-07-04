from cache import cache


class CacheMultinivel:
    def __init__(self, block_size, l1_capacity=False, l1_assoc=False,
                 l2_capacity=False, l2_assoc=False,
                 l3_capacity=False, l3_assoc=False):
        self.block_size = int(block_size)
        # Inicializar el caché de nivel 1, si está definido
        if l1_capacity and l1_assoc:
            self.l1_cache = cache(l1_capacity, l1_assoc, self.block_size, "l")
        else:
            self.l1_cache = None

        # Inicializar el caché de nivel 2, si está definido
        if l2_capacity and l2_assoc:
            self.l2_cache = cache(l2_capacity, l2_assoc, self.block_size, "l")
        else:
            self.l2_cache = None

        # Inicializar el caché de nivel 3, si está definido
        if l3_capacity and l3_assoc:
            self.l3_cache = cache(l3_capacity, l3_assoc, self.block_size, "l")
        else:
            self.l3_cache = None

    def access(self, access_type, address):
        """
        Accede a la dirección especificada en los niveles de caché disponibles.
        Devuelve True si ocurrió un miss en todos los niveles de caché.
        """
        miss_occurred = False

        # Acceso en el nivel 1 de caché
        if self.l1_cache:
            miss_occurred = self.l1_cache.access(access_type, address)
            if not miss_occurred:
                return False

        # Acceso en el nivel 2 de caché si hubo un miss en L1
        if self.l2_cache:
            l2_miss_occurred = self.l2_cache.access(access_type, address)
            if not l2_miss_occurred:
                # Si hubo hit en L2, actualizar L1
                self.l1_cache.access("w", address)
                return False

        # Acceso en el nivel 3 de caché si hubo un miss en L2
        if self.l3_cache:
            l3_miss_occurred = self.l3_cache.access(access_type, address)
            if not l3_miss_occurred:
                # Si hubo hit en L3, actualizar L2 y L1
                if self.l2_cache:
                    self.l2_cache.access("w", address)
                if self.l1_cache:
                    self.l1_cache.access("w", address)
                return False

        # Si se alcanzó aquí, hubo un miss en todos los niveles
        return True

    def print_stats(self):
        """
        Muestra las estadísticas de los niveles de caché y calcula el AMAT.
        """
        if self.l1_cache:
            print("\nEstadísticas del caché L1:")
            l1_hit_time = 4  # Hit time de L1
            l1_miss_penalty = 500  # Miss penalty de L1
            l1_miss_rate = float(self.l1_cache.print_stats())/100
            l1_amat = l1_hit_time + l1_miss_rate * l1_miss_penalty
            l1_amat = "{:.3f}".format(l1_amat)
            print(f"AMAT un nivel de caché: {l1_amat}")

        if self.l2_cache:
            print("\nEstadísticas del caché L2:")
            l2_hit_time = 12  # Hit time de L2
            l2_miss_penalty = 500  # Miss penalty de L2
            l2_miss_rate = float(self.l2_cache.print_stats())/100
            l2_amat = l1_hit_time + l1_miss_rate * (
                      l2_hit_time + l2_miss_rate * l2_miss_penalty)
            l2_amat = "{:.3f}".format(l2_amat)
            print(f"AMAT dos niveles de caché: {l2_amat}")

        if self.l3_cache:
            print("\nEstadísticas del caché L3:")
            l3_hit_time = 60  # Hit time de L3
            l3_miss_penalty = 500  # Miss penalty de L3
            l3_miss_rate = float(self.l3_cache.print_stats())/100
            l3_amat = l1_hit_time + l1_miss_rate * (
                      l2_hit_time + l2_miss_rate * (
                        l3_hit_time + l3_miss_rate * l3_miss_penalty))
            l3_amat = "{:.3f}".format(l3_amat)
            print(f"AMAT tres niveles de caché: {l3_amat}")

    def print_info(self):
        """
        Muestra la información de configuración de los niveles de caché.
        """
        if self.l1_cache:
            print("Información del caché L1:")
            self.l1_cache.print_info()
        if self.l2_cache:
            print("Información del caché L2:")
            self.l2_cache.print_info()
        if self.l3_cache:
            print("Información del caché L3:")
            self.l3_cache.print_info()
