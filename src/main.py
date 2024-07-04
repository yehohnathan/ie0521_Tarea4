from Automatizador import Automatizador
from AutomatizadorMulticache import AutomatizadorMulticache


def main():
    automatizadorP1 = Automatizador()
    automatizadorMultiple = AutomatizadorMulticache()

    # Opciones de pruebas
    opciones = {
        1: ("Modificar tamaño de caché",
            automatizadorP1.mod_size_cache),
        2: ("Modificar asociatividad del caché",
            automatizadorP1.mod_assoc_cache),
        3: ("Modificar tamaño de bloque",
            automatizadorP1.mod_size_block),
        4: ("Modificar política de reemplazo",
            automatizadorP1.mod_repl_policy),
        5: ("Presencia de caché L1",
            automatizadorMultiple.presencia_L1),
        6: ("Presencia de caché L2 (configuración a)",
            automatizadorMultiple.presencia_L2_a),
        7: ("Presencia de caché L2 (configuración b)",
            automatizadorMultiple.presencia_L2_b),
        8: ("Presencia de caché L3 (configuración a)",
            automatizadorMultiple.presencia_L3_a),
        9: ("Presencia de caché L3 (configuración b)",
            automatizadorMultiple.presencia_L3_b)
    }

    # Imprimir opciones de prueba
    print("Seleccione la prueba que desea ejecutar:")
    for key, (descripcion, _) in opciones.items():
        print(f"{key}. {descripcion}")

    # Obtener la selección del usuario
    selecciones = input("Ingrese los números de las pruebas que desea" +
                        " ejecutar separados por espacios: ")
    selecciones = selecciones.split()

    for seleccion_str in selecciones:
        seleccion = int(seleccion_str)
        if seleccion in opciones:
            print(f"Ejecutando prueba: {opciones[seleccion][0]}")
            opciones[seleccion][1]()
        else:
            print(f"Selección inválida: {seleccion}. Se omitirá esta",
                  "selección.")

    print("Todas las pruebas seleccionadas han sido ejecutadas.")


""" ======================== Ejecución del main ======================= """
if __name__ == "__main__":
    main()
