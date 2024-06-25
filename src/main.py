""" Importa la clase Automatizador"""
from Automatizador import Automatizador


def main():
    automatizador = Automatizador()
    automatizador.mod_size_cache()
    automatizador.mod_assoc_cache()
    automatizador.mod_size_block()
    automatizador.mod_repl_policy()


""" ======================== Ejecución del main ======================= """
if __name__ == "__main__":
    main()
