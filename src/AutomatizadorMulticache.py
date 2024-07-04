""" Librerías Utilizadas """
import os
import subprocess
from pathlib import Path


class AutomatizadorMulticache:
    def __init__(self):
        """
        Inicializador de atributos de la clase Automatizador.
        """
        # Se obtiene la dirección del script actual
        self.repo_dir = Path(__file__).resolve().parent.parent

        # Ahora se obtienen las direcciones a utilizar:
        self.traces_dir = self.repo_dir / "Traces"
        self.results_parte2_dir = self.repo_dir / "Resultados_P2"
        self.base_parte2_dir = self.repo_dir / "src/base_parte2/cache_sim.py"

        # Crea las carpetas resultados (si no existen)
        self.results_parte2_dir.mkdir(parents=True, exist_ok=True)

        # Crea una lista de dirección de todos los traces y los ordena
        self.traces = sorted(
            os.listdir(self.traces_dir),
            key=lambda x: int(x.split('.')[0])
        )

    def run_code(self, l1_capacity, l1_assoc, l2_capacity, l2_assoc,
                 l3_capacity, l3_assoc, block_size, trace_file):
        # Se obtiene la dirección del trace a ejecutar
        trace_path = self.traces_dir / trace_file

        # Si el trace no existe, muestra un mensaje de error y para el código.
        if not trace_path.exists():
            raise FileNotFoundError("No se encontró el archivo de traza:" +
                                    f"{trace_path}")

        # Se modifica la lista que será el comando a ejecutar
        command = [
            "python3", str(self.base_parte2_dir),
            "--l1_s", str(l1_capacity),
            "--l1_a", str(l1_assoc),
        ]

        if l2_capacity is not None and l2_assoc is not None:
            command += [
                "--l2_s", str(l2_capacity),
                "--l2_a", str(l2_assoc)
            ]

        if l3_capacity is not None and l3_assoc is not None:
            command += [
                "--l3_s", str(l3_capacity),
                "--l3_a", str(l3_assoc)
            ]

        command += ["-b", str(block_size), "-t", str(trace_path)]

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

    def run_tests(self, param_name, fixed_params, output_filename):
        """
        Ejecuta una serie de pruebas variando un parámetro del caché y
        manteniendo otros parámetros fijos.

        Args:
            param_name (str): El nombre del parámetro que se está variando
            (para fines de impresión).
            fixed_params (dict): Un diccionario de parámetros fijos para la
            simulación del caché.
            output_filename (str): El nombre del archivo donde se guardarán
            los resultados.
        """
        # Genera el mensaje inicial con los parámetros fijos.
        message = f"================= Efecto de {param_name} ================="
        message += "\nParámetros fijos:\n"
        message += "\n".join([f"{k} = {v}" for k, v in fixed_params.items()])
        message += "\n"
        print(message)

        # Itera sobre cada archivo de trace de Traces.
        for trace_file in self.traces:
            trace_message = f"\n+++++++++ Trace {trace_file} +++++++++"

            result = self.run_code(
                fixed_params.get('l1_capacity'),
                fixed_params.get('l1_assoc'),
                fixed_params.get('l2_capacity'),
                fixed_params.get('l2_assoc'),
                fixed_params.get('l3_capacity'),
                fixed_params.get('l3_assoc'),
                fixed_params.get('block_size'),
                trace_file
            )
            # Añade los resultados al mensaje.
            trace_message += result

            # Añade los resultados del trace al mensaje general.
            message += trace_message

        # Guarda todos los resultados en un archivo .txt
        output_file = self.results_parte2_dir / output_filename
        with open(output_file, 'w') as f:
            f.write(message)

    def presencia_L1(self):
        """
        Ejecuta pruebas para la presencia de caché L1.
        """
        fixed_params = {
            'l1_capacity': 32,
            'l1_assoc': 8,
            'l2_capacity': None,
            'l2_assoc': None,
            'l3_capacity': None,
            'l3_assoc': None,
            'block_size': 64  # Ajustar según sea necesario
        }
        self.run_tests("Presencia de caché L1", fixed_params,
                       "Presencia_L1.txt")

    def presencia_L2_a(self):
        """
        Ejecuta pruebas para la presencia de caché L2 (configuración a).
        """
        fixed_params = {
            'l1_capacity': 32,
            'l1_assoc': 8,
            'l2_capacity': 64,
            'l2_assoc': 8,
            'l3_capacity': None,
            'l3_assoc': None,
            'block_size': 64  # Ajustar según sea necesario
        }
        self.run_tests("Presencia de caché L2 (a)", fixed_params,
                       "Presencia_L2_a.txt")

    def presencia_L2_b(self):
        """
        Ejecuta pruebas para la presencia de caché L2 (configuración b).
        """
        fixed_params = {
            'l1_capacity': 32,
            'l1_assoc': 8,
            'l2_capacity': 128,
            'l2_assoc': 16,
            'l3_capacity': None,
            'l3_assoc': None,
            'block_size': 64  # Ajustar según sea necesario
        }
        self.run_tests("Presencia de caché L2 (b)", fixed_params,
                       "Presencia_L2_b.txt")

    def presencia_L3_a(self):
        """
        Ejecuta pruebas para la presencia de caché L3 (configuración a).
        """
        fixed_params = {
            'l1_capacity': 32,
            'l1_assoc': 8,
            'l2_capacity': 256,
            'l2_assoc': 8,
            'l3_capacity': 512,
            'l3_assoc': 16,
            'block_size': 64  # Ajustar según sea necesario
        }
        self.run_tests("Presencia de caché L3 (a)", fixed_params,
                       "Presencia_L3_a.txt")

    def presencia_L3_b(self):
        """
        Ejecuta pruebas para la presencia de caché L3 (configuración b).
        """
        fixed_params = {
            'l1_capacity': 32,
            'l1_assoc': 8,
            'l2_capacity': 256,
            'l2_assoc': 8,
            'l3_capacity': 1024,
            'l3_assoc': 32,
            'block_size': 64  # Ajustar según sea necesario
        }
        self.run_tests("Presencia de caché L3 (b)", fixed_params,
                       "Presencia_L3_b.txt")
