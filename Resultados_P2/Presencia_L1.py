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
    results_pattern = r'AMAT un nivel de caché: (\d+\.\d+)'
    
    traces = re.split(trace_pattern, content)[1:]
    data = []
    
    for i in range(0, len(traces), 2):
        trace_name = traces[i].strip()
        trace_data = traces[i+1]
         # Buscar resultados de simulación en los datos del trace
        results = re.findall(results_pattern, trace_data)
        
        for valor in results:
            data.append([trace_name, float(valor)])
        df = pd.DataFrame(data, columns=['Trace', 'Valor AMAT'])
        df = df.sort_values(by="Valor AMAT")
    return df

# Parseamos el archivo
file_path = 'Presencia_L1.txt'  # Reemplace con el nombre de su archivo
data = parse_trace_file(file_path)

# Verificamos que los datos se hayan parseado correctamente
if data.empty:
    print("No se encontraron datos en el archivo.")
else:
    print(data)

# Paso 2: Calcular la Media Geométrica
mean_amat = gmean(data['Valor AMAT'])



# Mostramos la media geométrica del AMAT
print("Media Geométrica de AMAT:",mean_amat)

# Definimos el directorio donde se guardarán los archivos
output_dir = 'Tablas'

# Creamos el directorio si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)



# Paso 3: Creación de tabla Latex
def create_latex_table(data, filename):
    latex_table = "\\begin{table}[H]\n\\centering\n\\begin{tabular}{|c|c|c|c|}\n\\hline\n"
    latex_table += "Trace  & AMAT  & Trace  & AMAT  \\\\\n\\hline\n"
    
    num_row = len(data)
    for i in range(0, num_row, 2):
        # Extraer datos del primer resultado en la fila
        trace_name_1 = data.iloc[i]['Trace']
        amat_1 = data.iloc[i]['Valor AMAT']
        
        if i + 1 < num_row:
            # Extraer datos del segundo resultado en la fila si existe
            trace_name_2 = data.iloc[i + 1]['Trace']
            amat_2 = data.iloc[i + 1]['Valor AMAT']
        else:
            # Si no hay un segundo resultado, dejar la celda vacía
            trace_name_2 = ""
            amat_2 = ""
        
        # Verificar si amat_2 es un valor numérico
        if isinstance(amat_1, (int, float)):
            amat_1_str = f"{amat_1:.3f}"
        else:
            amat_1_str = str(amat_1)
        
        if isinstance(amat_2, (int, float)):
            amat_2_str = f"{amat_2:.3f}"
        else:
            amat_2_str = str(amat_2)
        
        # Añadir la fila a la tabla LaTeX
        latex_table += f"{trace_name_1} & {amat_1_str} & {trace_name_2} & {amat_2_str} \\\\\\hline\n"
    
    latex_table += "\\end{tabular}\n\\caption{Resultados de la simulación de presencia del L1}\n\\label{tab:amatL1}\n\\end{table}"
    
    # Guardamos la tabla en un archivo .tex
    with open(filename, 'w') as file:
        file.write(latex_table)
    print(f"La tabla en formato LaTeX se ha guardado correctamente en {filename}.")
# Guardamos los datos en una hoja de cálculo
data.to_csv(os.path.join(output_dir, f'{file_path}.csv'), index=False)
# Guardamos la tabla para todos los traces
create_latex_table(data, os.path.join(output_dir, 'PresenciaL1.tex'))
