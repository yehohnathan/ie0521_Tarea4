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
    amat_l3_pattern = r'AMAT tres niveles de caché: (\d+\.\d+)'
    
    traces = re.split(trace_pattern, content)[1:]
    data = []
    
    for i in range(0, len(traces), 2):
        trace_name = traces[i].strip()
        trace_data = traces[i+1]
        # Buscar resultados de AMAT en los datos del trace
        amat_l1 = re.search(amat_l1_pattern, trace_data)
        amat_l2 = re.search(amat_l2_pattern, trace_data)
        amat_l3 = re.search(amat_l3_pattern, trace_data)
        # Agregar los valores encontrados a la lista de datos
        if amat_l1 and amat_l2 and amat_l3:
            data.append([trace_name, float(amat_l1.group(1)), float(amat_l2.group(1)),float(amat_l3.group(1))])
        else:
            data.append([trace_name, np.nan, np.nan,np.nan])
        df = pd.DataFrame(data, columns=['Trace', 'AMAT L1', 'AMAT L2', 'AMAT L3'])
        df['Speedup'] = df['AMAT L2'] / df['AMAT L3']
        df = df.sort_values(by=('AMAT L1'))
    
    return df


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
mean_amatL1 = gmean(data['AMAT L1'].dropna())
mean_amatL2 = gmean(data['AMAT L2'].dropna())
mean_amatL3 = gmean(data['AMAT L3'].dropna())
mean_speedup = gmean(data['Speedup'].dropna())
# Mostramos la media geométrica del AMAT
print("Media Geométrica de AMAT L1:", mean_amatL1)
print("Media Geométrica de AMAT L2:", mean_amatL2)
print("Media Geométrica de AMAT L2:", mean_amatL3)
print("Media Geométrica de Speedup:", mean_speedup)
# Definimos el directorio donde se guardarán los archivos
output_dir = 'Tablas'
# Creamos el directorio si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)



# Guardamos los datos en una hoja de cálculo
data.to_csv(os.path.join(output_dir, f'{file_path}.csv'), index=False)
#Paso 3: Creación de tabla Latex
def create_latex_table(data, filename):
    latex_table = "\\begin{table}[H]\n\\centering\n\\begin{tabular}{|c|c|c|c|c|}\n\\hline\n"
    latex_table += "Trace & AMAT L1 & AMAT L2 & AMAT L3 & Speedup\\\\\n\\hline\n"
    #organizar los datos
    
    num_row =len(data)
    row_data = []
    for i in range(num_row): 
        trace_name  =  data.iloc[i]['Trace']
        amatL1      =       data.iloc[i]['AMAT L1']
        amatL2      =       data.iloc[i]['AMAT L2']
        amatL3      =       data.iloc[i]['AMAT L3']
        speedup     =       data.iloc[i]['Speedup']

        row_data.append(f"{trace_name} & {amatL1:.3f}& {amatL2:.3f}& {amatL3:.3f}& {speedup:.3f}\\\\\hline\n")
  
    
        # Añadir la fila  a la tabla LaTeX
        latex_table += f"{trace_name} & {amatL1:.3f} & {amatL2:.3f} &  {amatL3:.3f} & {speedup:.3f}\\\\\\hline\n"
    latex_table += f"Media Geométrica & {mean_amatL1:.2f} & {mean_amatL2:.2f}& {mean_amatL3:.2f} & {mean_speedup:.2f}\\\\\\hline\n"
    latex_table += "\\end{tabular}\n\\caption{Resultados de la simulación en presencia del L2 utilizando la configuración " +configuration+"}\n\\label{tab:amatL3"+configuration+"}\n\\end{table}"
    # Guardamos la tabla en un archivo .tex
    with open(filename, 'w') as file:
        file.write(latex_table)
    print(f"La tabla en formato LaTeX se ha guardado correctamente en {filename}.")

# Guardamos la tabla para todos los traces
create_latex_table(data, os.path.join(output_dir, f'{file_path}.tex'))