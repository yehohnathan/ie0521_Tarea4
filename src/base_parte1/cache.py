from math import log2, floor


class cache:
    def __init__(self, cache_capacity, cache_assoc, block_size, repl_policy):
        self.total_access = 0
        self.total_misses = 0
        self.total_reads = 0
        self.total_read_misses = 0
        self.total_writes = 0
        self.total_write_misses = 0
        self.cache_capacity = int(cache_capacity)
        self.cache_assoc = int(cache_assoc)
        self.block_size = int(block_size)
        self.repl_policy = repl_policy
        self.byte_offset_size = log2(self.block_size)
        self.num_sets = int((self.cache_capacity * 1024) / (self.block_size * self.cache_assoc))
        self.index_size = int(log2(self.num_sets))
        self.valid_table = [[False for _ in range(self.cache_assoc)] for _ in range(self.num_sets)]
        self.tag_table = [[0 for _ in range(self.cache_assoc)] for _ in range(self.num_sets)]
        self.repl_table = [[0 for _ in range(self.cache_assoc)] for _ in range(self.num_sets)]

    def print_info(self):
        print("Parámetros del caché:")
        print("\tCapacidad:\t\t\t" + str(self.cache_capacity) + "kB")
        print("\tAssociatividad:\t\t\t" + str(self.cache_assoc))
        print("\tTamaño de Bloque:\t\t\t" + str(self.block_size) + "B")
        print("\tPolítica de Reemplazo:\t\t\t" + str(self.repl_policy))

    def print_stats(self):
        print("Resultados de la simulación:")
        miss_rate = (100.0*self.total_misses) / self.total_access
        miss_rate = "{:.3f}".format(miss_rate)
        result_str = str(self.total_misses)+","+miss_rate+"%"
        print(result_str)

    def access(self, access_type, address):
        byte_offset = int(address % (2 ** self.byte_offset_size))
        index = int(floor(address / (2 ** self.byte_offset_size)) % (2 ** self.index_size))
        tag = int(floor(address / (2 ** (self.byte_offset_size + self.index_size))))
        hit = self.find(index, tag)
        miss_occurred = False

        if hit == -1:
            self.bring_to_cache(index, tag)
            self.total_misses += 1
            if access_type == "r":
                self.total_read_misses += 1
            else:
                self.total_write_misses += 1
            miss_occurred = True

        self.total_access += 1
        if access_type == "r":
            self.total_reads += 1
        else:
            self.total_writes += 1

        return miss_occurred

    def find(self, index, tag):
        for assoc in range(self.cache_assoc):
            if self.valid_table[index][assoc] and self.tag_table[index][assoc] == tag:
                return assoc
        return -1

    def bring_to_cache(self, index, tag):
        empty_slot = -1
        for assoc in range(self.cache_assoc):
            if not self.valid_table[index][assoc]:
                self.valid_table[index][assoc] = True
                self.tag_table[index][assoc] = tag
                self.repl_table[index][assoc] = self.cache_assoc - 1
                empty_slot = assoc
                break

        if self.repl_policy == "l":
            lru_slot = 999999
            for assoc in range(self.cache_assoc):
                if self.repl_table[index][assoc] < lru_slot:
                    lru_slot = assoc
            self.valid_table[index][lru_slot] = True
            self.tag_table[index][lru_slot] = tag
            self.repl_table[index][lru_slot] = self.cache_assoc - 1
            empty_slot = lru_slot

            for assoc in range(self.cache_assoc):
                if assoc == empty_slot:
                    continue
                else:
                    self.repl_table[index][assoc] -= 1
