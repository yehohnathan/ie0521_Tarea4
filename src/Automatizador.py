""" Librerías Utilizadas """
import os
import subprocess
from pathlib import Path


class Automatizador:
    def __init__(self):
        """
        Inicializador de atributos de la clase Automatizador.
        """
        # Se obtiene la dirección del script actual
        self.repo_dir = Path(__file__).resolve().parent.parent

        # Ahora se obtienen las direcciones a utilizar:
        self.traces_dir = self.repo_dir / "Traces"
        self.results_parte1_dir = self.repo_dir / "Resultados_P1"
        self.base_parte1_dir = self.repo_dir / "src/base_parte1/cache_sim.py"

        # Crea las carpetas resultados (si no existen)
        self.results_parte1_dir.mkdir(parents=True, exist_ok=True)

        # Crea una lista de dirección de todos los traces y los ordena
        self.traces = sorted(
            os.listdir(self.traces_dir),
            key=lambda x: int(x.split('.')[0])
        )

    def run_code(self, cache_capacity, cache_assoc, block_size, repl_policy,
                 trace_file):
        # Se obtiene la dirección del trace a ejecutar
        trace_path = self.traces_dir / trace_file

        # Si el trace no existe, muestra un mensaje de error y para el código.
        if not trace_path.exists():
            raise FileNotFoundError("No se encontró el archivo de traza:" +
                                    f"{trace_path}")

        # Se modifica la lista que será el comando a ejecutar
        command = [
            "python3", str(self.base_parte1_dir),
            "-s", str(cache_capacity),
            "-a", str(cache_assoc),
            "-b", str(block_size),
            "-r", repl_policy,
            "-t", str(trace_path)
        ]

        # Se muestra el comando que se está ejecutando
        print("=== Ejecutando comando: ====", " ".join(command))

        # Muestra el resultado de ejecutar el comando, o, su fallo.
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            output = f"Error ejecutando el comando: {result.stderr}"
            print(output)
        else:
            output = result.stdout
            print(output)

        return output

    def run_tests(self, param_name, fixed_params, var_param, var_values,
                  output_filename):
        """
        Ejecuta una serie de pruebas variando un parámetro del caché y
        manteniendo otros parámetros fijos.

        Args:
            param_name (str): El nombre del parámetro que se está variando
                              (para fines de impresión).

            fixed_params (dict): Un diccionario de parámetros fijos para la
                                 simulación del caché.

            var_param (str): El nombre del parámetro que se va a variar.

            var_values (list): Una lista de valores para el parámetro variable.

            output_filename (str): El nombre del archivo donde se guardarán los
                                   resultados.

        """
        # Genera el mensaje inicial con los parámetros fijos.
        message = f"================= Efecto de {param_name} ================="
        message += "\nParámetros fijos:\n"
        message += "\n".join([f"{k} = {v}" for k, v in fixed_params.items()])
        message += "\n"
        print(message)

        # Itera sobre cada archivo de trace de Traces.
        for trace_file in self.traces:
            message += f"\n+++++++++ Trace {trace_file} +++++++++"
            # Itera sobre cada valor del parámetro variable.
            for value in var_values:
                # Combina los parámetros fijos con el parámetro variable.
                params = {**fixed_params, var_param: value}

                # Ejecuta el código de simulación con los parámetros actuales.
                result = (self.run_code(params['cache_capacity'],
                                        params['cache_assoc'],
                                        params['block_size'],
                                        params['repl_policy'],
                                        trace_file))

                # Añade los resultados al mensaje.
                message += f"\n+ Variación de {param_name}: {value} +\n"
                message += result

        # Guarda todos los resultados en un archivo .txt
        output_file = self.results_parte1_dir / output_filename
        with open(output_file, 'w') as f:
            f.write(message)

    def table_example(self):
        """
        Ejecuta pruebas variando el tamaño del caché y mantiene otros
        parámetros fijos.
        """
        self.run_tests(
            "tamaño del caché",
            {'cache_assoc': 16, 'block_size': 64, 'repl_policy': 'l'},
            'cache_capacity', [128],
            "Comprobacion_Tabla.txt"
        )

    def mod_size_cache(self):
        """
        Ejecuta pruebas variando el tamaño del caché y mantiene otros
        parámetros fijos.
        """
        self.run_tests(
            "tamaño del caché",
            {'cache_assoc': 8, 'block_size': 64, 'repl_policy': 'l'},
            'cache_capacity',
            [2**i for i in range(3, 8)],
            "Efecto_tamaño_cache.txt"
        )

    def mod_assoc_cache(self):
        """
        Ejecuta pruebas variando la asociatividad del caché y mantiene otros
        parámetros fijos.
        """
        self.run_tests(
            "asociatividad del caché",
            {'cache_capacity': 32, 'block_size': 64, 'repl_policy': 'l'},
            'cache_assoc',
            [2**i for i in range(0, 5)],
            "Efecto_asociatividad_cache.txt"
        )

    def mod_size_block(self):
        """
        Ejecuta pruebas variando el tamaño del bloque del caché y mantiene
        otros parámetros fijos.
        """
        self.run_tests(
            "tamaño del bloque en el caché",
            {'cache_capacity': 32, 'cache_assoc': 8, 'repl_policy': 'l'},
            'block_size',
            [2**i for i in range(4, 8)],
            "Efecto_tamaño_bloque_cache.txt"
        )

    def mod_repl_policy(self):
        """
        Ejecuta pruebas variando la política de reemplazo del caché y mantiene
        otros parámetros fijos.
        """
        # Define los parámetros fijos.
        fixed_params = {'cache_capacity': 32,
                        'cache_assoc': 8,
                        'block_size': 64}

        param_name = "política de reemplazo"

        # Genera el mensaje inicial con los parámetros fijos.
        message = f"================= Efecto de {param_name} ================="
        message += "\nParámetros fijos:\n"
        message += "\n".join([f"{k} = {v}" for k, v in fixed_params.items()])
        message += "\n"
        print(message)

        # Itera sobre cada archivo de traza.
        for trace_file in self.traces:
            message += f"\n+++++++++ Trace {trace_file} +++++++++"

            # Itera sobre las políticas de reemplazo
            for policy in ['r', 'l']:
                # Ejecuta el código de simulación con la política actual.
                result = (self.run_code(fixed_params['cache_capacity'],
                                        fixed_params['cache_assoc'],
                                        fixed_params['block_size'],
                                        policy,
                                        trace_file))

                # Añade los resultados al mensaje.
                policy_name = "Random" if policy == 'r' else "LRU"
                message += f"\n+ Política de reemplazo: {policy_name} +\n"
                message += result

        # Guarda todos los resultados en un archivo .txt
        output_file = self.results_parte1_dir / "Efecto_politica_reemplazo.txt"
        with open(output_file, 'w') as f:
            f.write(message)
