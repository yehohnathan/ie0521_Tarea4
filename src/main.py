""" Importa la clase Automatizador"""
from Automatizador import Automatizador


def main():
    automatizadorP1 = Automatizador()
    # Verifica la tabla:
    automatizadorP1.table_example()

    # Realiza todas las pruebas solicitadas
    automatizadorP1.mod_size_cache()
    automatizadorP1.mod_assoc_cache()
    automatizadorP1.mod_size_block()
    automatizadorP1.mod_repl_policy()


""" ======================== Ejecución del main ======================= """
if __name__ == "__main__":
    main()
