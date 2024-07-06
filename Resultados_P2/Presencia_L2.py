import os
import re
import pandas as pd
import numpy as np
from scipy.stats import gmean
import matplotlib.pyplot as plt

# Definimos una función para parsear el archivo
def parse_trace_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Expresiones regulares para encontrar los diferentes bloques de datos
    trace_pattern = r'\+\+\+\+\+\+\+\+\+ Trace ([\w\.\-]+) \+\+\+\+\+\+\+\+\+'
    amat_l1_pattern = r'AMAT un nivel de caché: (\d+\.\d+)'
    amat_l2_pattern = r'AMAT dos niveles de caché: (\d+\.\d+)'
    
    traces = re.split(trace_pattern, content)[1:]
    data = []
    
    for i in range(0, len(traces), 2):
        trace_name = traces[i].strip()
        trace_data = traces[i+1]
        # Buscar resultados de AMAT en los datos del trace
        amat_l1 = re.search(amat_l1_pattern, trace_data)
        amat_l2 = re.search(amat_l2_pattern, trace_data)
        
        # Agregar los valores encontrados a la lista de datos
        if amat_l1 and amat_l2:
            data.append([trace_name, float(amat_l1.group(1)), float(amat_l2.group(1))])
        elif amat_l1:
            data.append([trace_name, float(amat_l1.group(1)), np.nan])
        elif amat_l2:
            data.append([trace_name, np.nan, float(amat_l2.group(1))])
        else:
            data.append([trace_name, np.nan, np.nan])
    
    return pd.DataFrame(data, columns=['Trace', 'Valor AMAT L1', 'Valor AMAT L2'])


# Parseamos el archivo
# Solicitar al usuario que ingrese el nombre del archivo
file_path = input("Por favor, ingrese el nombre del archivo a simular (incluya la extensión .txt): ")
# Verificar si el archivo existe
if not os.path.isfile(file_path):
    print(f"El archivo {file_path} no existe. Por favor, verifique el nombre y la ubicación del archivo.")
else:
    # Parseamos el archivo
    data = parse_trace_file(file_path)
# Verificamos que los datos se hayan parseado correctamente
if data.empty:
    print("No se encontraron datos en el archivo.")
else:
    print(data)

configuration = input("Por favor ingrese que configuración está analizando (a, b c, d): ")
# Paso 2: Calcular la Media Geométrica, excluyendo valores NaN
mean_amatL1 = gmean(data['Valor AMAT L1'].dropna())
mean_amatL2 = gmean(data['Valor AMAT L2'].dropna())

# Mostramos la media geométrica del AMAT
print("Media Geométrica de AMAT L1:", mean_amatL1)
print("Media Geométrica de AMAT L2:", mean_amatL2)

# Definimos el directorio donde se guardarán los archivos
output_dir = 'Tablas'
# Creamos el directorio si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)




import os
import pandas as pd
import numpy as np

# Paso 3: Creación de tabla Latex
def create_latex_table(data, filename, configuration, mean_amatL1, mean_amatL2):
    latex_table = "\\begin{table}[H]\n\\centering\n\\begin{tabular}{|c|c|c|c|c|c|}\n\\hline\n"
    latex_table += "Trace & AMAT L1 & AMAT L2 & Trace & AMAT L1 & AMAT L2\\\\\n\\hline\n"
    
    # Organizar los datos
    num_row = len(data)
    row_data = []

    for i in range(0, num_row, 2):
        # Extraer datos del primer resultado en la fila
        trace_name1 = data.iloc[i]['Trace']
        amatL1_1 = data.iloc[i]['Valor AMAT L1']
        amatL2_1 = data.iloc[i]['Valor AMAT L2']

        # Extraer datos del segundo resultado en la fila (si existe)
        if i + 1 < num_row:
            trace_name2 = data.iloc[i + 1]['Trace']
            amatL1_2 = data.iloc[i + 1]['Valor AMAT L1']
            amatL2_2 = data.iloc[i + 1]['Valor AMAT L2']
        else:
            trace_name2 = ""
            amatL1_2 = ""
            amatL2_2 = ""

        # Verificar si amatL1_1 y amatL2_1 son valores numéricos
        if isinstance(amatL1_1, (int, float)) and isinstance(amatL2_1, (int, float)):
            amatL1_1_str, amatL2_1_str = f"{amatL1_1:.3f}", f"{amatL2_1:.3f}"
        else:
            amatL1_1_str, amatL2_1_str = str(amatL1_1), str(amatL2_1)

        # Verificar si amatL1_2 y amatL2_2 son valores numéricos
        if isinstance(amatL1_2, (int, float)) and isinstance(amatL2_2, (int, float)):
            amatL1_2_str, amatL2_2_str = f"{amatL1_2:.3f}", f"{amatL2_2:.3f}"
        else:
            amatL1_2_str, amatL2_2_str = str(amatL1_2), str(amatL2_2)

        # Añadir la fila a la tabla LaTeX
        latex_table += f"{trace_name1} & {amatL1_1_str} & {amatL2_1_str} & {trace_name2} & {amatL1_2_str} & {amatL2_2_str} \\\\\\hline\n"

    latex_table += f"Media Geométrica & {mean_amatL1:.2f} & {mean_amatL2:.2f} & & &\\\\\\hline\n"
    latex_table += "\\end{tabular}\n\\caption{Resultados de la simulación en presencia del L2 utilizando la configuración " + configuration + "}\n\\label{tab:amatL1}\n\\end{table}"

    # Guardamos la tabla en un archivo .tex
    with open(filename, 'w') as file:
        file.write(latex_table)
    print(f"La tabla en formato LaTeX se ha guardado correctamente en {filename}.")

create_latex_table(data, os.path.join(output_dir, f'PresenciaL2_{configuration}.tex'), configuration, mean_amatL1, mean_amatL2)
