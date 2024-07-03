from optparse import OptionParser
import gzip
from cache_multinivel import CacheMultinivel

parser = OptionParser()
parser.add_option("--l1_s", dest="l1_s")    # L1_s
parser.add_option("--l1_a", dest="l1_a")    # L1_a
parser.add_option("--l2", action="store_true", dest="has_l2")
parser.add_option("--l2_s", dest="l2_s")    # L2_s
parser.add_option("--l2_a", dest="l2_a")    # L2_a
parser.add_option("--l3", action="store_true", dest="has_l3")
parser.add_option("--l3_s", dest="l3_s")    # L3_s
parser.add_option("--l3_a", dest="l3_a")    # L3_a
parser.add_option("-b", dest="block_size", default="64")
parser.add_option("-t", dest="TRACE_FILE")

(options, args) = parser.parse_args()

# Crear el objeto CacheMultinivel con las opciones proporcionadas
cache_multi = CacheMultinivel(
    options.block_size,
    options.l1_s,
    options.l1_a,
    options.l2_s,
    options.l2_a,
    options.l3_s,
    options.l3_a
)

i = 0  # SOLO PARA DEBUG

# Info del caché
# cache_multi.print_info()

with gzip.open(options.TRACE_FILE, 'rt') as trace_fh:
    for line in trace_fh:
        line = line.rstrip()
        access_type, hex_str_address = line.split(" ")
        address = int(hex_str_address, 16)
        cache_multi.access(access_type, address)

cache_multi.print_stats()
