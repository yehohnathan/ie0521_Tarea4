import os
import re
import pandas as pd
import numpy as np
from scipy.stats import gmean
import matplotlib.pyplot as plt
import argparse

# Definimos una función para parsear el archivo
def parse_trace_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Expresiones regulares para encontrar los diferentes bloques de datos
    trace_pattern = r'\+\+\+\+\+\+\+\+\+ Trace ([\w\.\-]+) \+\+\+\+\+\+\+\+\+'
    policy_replacement = r'\+ Política de reemplazo: ([\w\s]+) \+'
    results_pattern = r'Resultados de la simulación\n(\d+), ([\d\.]+)%'
    
    traces = re.split(trace_pattern, content)[1:]
    data = []
    
    for i in range(0, len(traces), 2):
        trace_name = traces[i].strip()
        trace_data = traces[i+1]
        replacement_policy = re.findall(policy_replacement, trace_data)
        results = re.findall(results_pattern, trace_data)
        
        for policy, (misses, miss_rate) in zip(replacement_policy, results):
            data.append([trace_name, policy.strip(), int(misses), float(miss_rate)])
    
    return pd.DataFrame(data, columns=['Trace', 'Politica de Reemplazo', 'Total Misses', 'Miss Rate'])

# Función para crear tabla en formato LaTeX
def create_latex_table(data, filename):
    latex_table = "\\begin{table}[H]\n\\centering\n\\begin{tabular}{|c|c|c|c|c|c|}\n\\hline\n"
    latex_table += "Trace & Total Misses & Miss Rate Total & Trace & Total Misses & Miss Rate Total \\\\\n\\hline\n"
    
    # Organizar los datos por política de reemplazo
    replacement_policy = data['Politica de Reemplazo'].unique()
    for policy in replacement_policy:
        policy_data = data[data['Politica de Reemplazo'] == policy]
        num_rows = len(policy_data)
        
        for i in range(0, num_rows, 2):
            row_data = []
            for j in range(2):
                if i + j < num_rows:
                    trace_name = policy_data.iloc[i + j]['Trace']
                    total_misses = policy_data.iloc[i + j]['Total Misses']
                    miss_rate = policy_data.iloc[i + j]['Miss Rate']
                    row_data.append(f"{trace_name} & {total_misses} & {miss_rate:.2f}\\%")
                else:
                    row_data.append("& & & ")
            
            latex_table += " & ".join(row_data) + " \\\\\hline\n"
    
    latex_table += "\\hline\n\\end{tabular}\n\\caption{Resultados de la Simulación del Cache}\n\\label{tab:cache_results}\n\\end{table}"
    
    # Guardamos la tabla en un archivo .tex
    with open(filename, 'w') as file:
        file.write(latex_table)
    print(f"La tabla en formato LaTeX se ha guardado correctamente en {filename}.")

# Función principal
def main(args):
    # Parseamos el archivo
    data = parse_trace_file(args.file)

    # Verificamos que los datos se hayan parseado correctamente
    if data.empty:
        print("No se encontraron datos en el archivo.")
        return
    
    # Paso 2: Calcular la Media Geométrica
    replacement_policy = data['Politica de Reemplazo'].unique()
    mean_miss_rates = []

    for policy in replacement_policy:
        rates = data[data['Politica de Reemplazo'] == policy]['Miss Rate']
        mean_miss_rate = gmean(rates)
        mean_miss_rates.append([policy, mean_miss_rate])

    # Convertimos a DataFrame para facilitar el manejo
    mean_miss_rates_df = pd.DataFrame(mean_miss_rates, columns=['Politica de Reemplazo', 'Mean Miss Rate'])

    # Mostramos la media geométrica del miss rate
    print(mean_miss_rates_df)

    # Definimos el directorio donde se guardarán los archivos
    output_dir = 'Archivos'

    # Creamos el directorio si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Paso 3: Crear la Hoja de Cálculo
    mean_miss_rates_df.to_csv(os.path.join(output_dir, 'mean_miss_rates_politica.csv'), index=False)
    data.to_csv(os.path.join(output_dir, 'trace_data_politica.csv'), index=False)

    # Paso 4: Graficar los Datos
    plt.figure(figsize=(10, 6))
    plt.plot(mean_miss_rates_df['Politica de Reemplazo'], mean_miss_rates_df['Mean Miss Rate'], marker='o')
    plt.title(args.title)
    plt.xlabel(args.x_label)
    plt.ylabel(args.y_label)
    plt.xticks(rotation=45)
    plt.yticks(mean_miss_rates_df['Mean Miss Rate'])
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'politica_vs_miss_rate.png'))
    plt.show()

    # Paso 5: Guardar la Tabla en Formato LaTeX Personalizado
    create_latex_table(data, os.path.join(output_dir, 'trace_data_politica.tex'))

    # Paso 6: Análisis del Trace Específico
    specific_trace_data = data[data['Trace'] == args.trace]

    if specific_trace_data.empty:
        print(f"No se encontraron datos para el trace {args.trace}.")
    else:
        print(specific_trace_data)

        plt.figure(figsize=(10, 6))
        plt.plot(specific_trace_data['Politica de Reemplazo'], specific_trace_data['Miss Rate'], marker='o')
        plt.title(f'{args.title} para {args.trace}')
        plt.xlabel(args.x_label)
        plt.ylabel(args.y_label)
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, f'politica_vs_miss_rate_{args.trace}.png'))
        plt.show()
        
        create_latex_table(specific_trace_data, os.path.join(output_dir, 'specific_trace_data.tex'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Procesa y grafica los datos de simulación de caché.")
    parser.add_argument('--file', type=str, required=True, help='Archivo de entrada con los datos de simulación.')
    parser.add_argument('--trace', type=str, required=True, help='Nombre del trace específico para analizar.')
    parser.add_argument('--x_label', type=str, required=True, help='Título del eje X para las gráficas.')
    parser.add_argument('--y_label', type=str, required=True, help='Título del eje Y para las gráficas.')
    parser.add_argument('--title', type=str, required=True, help='Título de la gráfica.')
    
    args = parser.parse_args()
    main(args)
