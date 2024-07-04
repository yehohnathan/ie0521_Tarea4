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
    cache_size_pattern = r'\+ Variación de tamaño del caché: (\d+) \+'
    results_pattern = r'Resultados de la simulación\n(\d+), ([\d\.]+)%'
    
    traces = re.split(trace_pattern, content)[1:]
    data = []
    
    for i in range(0, len(traces), 2):
        trace_name = traces[i].strip()
        trace_data = traces[i+1]
        cache_sizes = re.findall(cache_size_pattern, trace_data)
        results = re.findall(results_pattern, trace_data)
        
        for size, (misses, miss_rate) in zip(cache_sizes, results):
            data.append([trace_name, int(size), int(misses), float(miss_rate)])
    
    return pd.DataFrame(data, columns=['Trace', 'Cache Size', 'Total Misses', 'Miss Rate'])

# Parseamos el archivo
file_path = 'Efecto_tamaño_cache.txt'  # Reemplace con el nombre de su archivo
data = parse_trace_file(file_path)

# Verificamos que los datos se hayan parseado correctamente
if data.empty:
    print("No se encontraron datos en el archivo.")
else:
    print(data)

# Paso 2: Calcular la Media Geométrica

# Calculamos la media geométrica del miss rate para cada tamaño de caché
cache_sizes = data['Cache Size'].unique()
mean_miss_rates = []

for size in cache_sizes:
    rates = data[data['Cache Size'] == size]['Miss Rate']
    mean_miss_rate = gmean(rates)
    mean_miss_rates.append([size, mean_miss_rate])

# Convertimos a DataFrame para facilitar el manejo
mean_miss_rates_df = pd.DataFrame(mean_miss_rates, columns=['Cache Size', 'Mean Miss Rate'])

# Mostramos la media geométrica del miss rate
print(mean_miss_rates_df)

# Definimos el directorio donde se guardarán los archivos
output_dir = 'Archivos'

# Creamos el directorio si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Paso 3: Crear la Hoja de Cálculo

# Guardamos los datos en una hoja de cálculo
mean_miss_rates_df.to_csv(os.path.join(output_dir, 'mean_miss_rates.csv'), index=False)
data.to_csv(os.path.join(output_dir, 'trace_data_cache.csv'), index=False)

# Paso 4: Graficar los Datos

# Graficamos los datos
plt.figure(figsize=(10, 6))
plt.plot(mean_miss_rates_df['Cache Size'], mean_miss_rates_df['Mean Miss Rate'], marker='o')
plt.title(' Tamaño del Caché vs Miss Rate Total Promedio')
plt.xlabel('Tamaño del Caché (KB)')
plt.ylabel('Miss Rate Total Promedio (%)')
plt.xticks(mean_miss_rates_df['Cache Size'])
plt.yticks(mean_miss_rates_df['Mean Miss Rate'])
plt.grid(True)



plt.savefig(os.path.join(output_dir, 'miss_rate_vs_cache_size.png'))
plt.show()

# Paso 5: Guardar la Tabla en Formato LaTeX Personalizado

# Creamos una tabla en formato LaTeX personalizado
def create_latex_table(data, filename):
    latex_table = "\\begin{table}[H]\n\\centering\n\\begin{tabular}{|c|c|c|c|c|c|}\n\\hline\n"
    latex_table += "Trace & Total Misses & Miss Rate Total & Trace & Total Misses & Miss Rate Total \\\\\n\\hline\n"
    
    # Organizar los datos por tamaños de caché
    cache_sizes = data['Cache Size'].unique()
    for size in cache_sizes:
        cache_data = data[data['Cache Size'] == size]
        num_rows = len(cache_data)
        
        for i in range(0, num_rows, 2):
            row_data = []
            for j in range(2):
                if i + j < num_rows:
                    trace_name = cache_data.iloc[i + j]['Trace']
                    total_misses = cache_data.iloc[i + j]['Total Misses']
                    miss_rate = cache_data.iloc[i + j]['Miss Rate']
                    row_data.append(f"{trace_name} & {total_misses} & {miss_rate:.2f}\\%")
                else:
                    row_data.append("& & & ")
            
            latex_table += " & ".join(row_data) + " \\\\\hline\n"
    
    latex_table += "\\hline\n\\end{tabular}\n\\caption{Resultados de la Simulación del Cache}\n\\label{tab:cache_results}\n\\end{table}"
    
    # Guardamos la tabla en un archivo .tex
    with open(filename, 'w') as file:
        file.write(latex_table)
    print(f"La tabla en formato LaTeX se ha guardado correctamente en {filename}.")

# Guardamos la tabla para todos los traces
create_latex_table(data, os.path.join(output_dir, 'trace_data_cache.tex'))

# Paso 6: Análisis del Trace "465.tonto-1769B.trace.txt.gz"

# Filtramos los datos para el trace específico
specific_trace = '465.tonto-1769B.trace.txt.gz'
specific_trace_data = data[data['Trace'] == specific_trace]

# Verificamos si el trace específico tiene datos
if specific_trace_data.empty:
    print(f"No se encontraron datos para el trace {specific_trace}.")
else:
    print(specific_trace_data)

    # Graficamos los datos del trace específico
    plt.figure(figsize=(10, 6))
    plt.plot(specific_trace_data['Cache Size'], specific_trace_data['Miss Rate'], marker='o')
    plt.title(f'Tamaño del Caché para vs Miss Rate  {specific_trace}')
    plt.xlabel('Tamaño del Caché')
    plt.ylabel('Miss Rate (%)')
    plt.xticks(specific_trace_data['Cache Size'])
    plt.yticks(specific_trace_data['Miss Rate'])
    plt.grid(True)
    
    plt.xticks(specific_trace_data['Cache Size'])

    plt.savefig(os.path.join(output_dir, f'miss_rate_cache{specific_trace}.png'))
    plt.show()
    
    # Guardamos la tabla para el trace específico
    create_latex_table(specific_trace_data, os.path.join(output_dir, 'specific_trace_data_cache.tex'))
