import pandas as pd
import matplotlib.pyplot as plt
import os
# Leer el archivo CSV
file_path = 'MejoresAMATL1_L2_L3.csv'  
df = pd.read_csv(file_path)

# Función para simplificar el nombre del trace
def simplificar_nombre_trace(trace):
    base_name = trace.split('-')[0]  # Tomar la primera parte del nombre
    return base_name

# Aplicar la función a la columna 'Trace'
df['Trace Simplificado'] = df['Trace'].apply(simplificar_nombre_trace)

# Crear la gráfica
plt.figure(figsize=(14, 8))

# Graficar AMAT L1
plt.plot(df['Trace Simplificado'], df['AMAT L1'], marker='o', linestyle='-', label='AMAT L1')

# Graficar AMAT L2
plt.plot(df['Trace Simplificado'], df['AMAT L2'], marker='o', linestyle='-', label='AMAT L2')

# Graficar AMAT L3
plt.plot(df['Trace Simplificado'], df['AMAT L3'], marker='o', linestyle='-', label='AMAT L3')

# Configurar la gráfica
plt.xlabel('Trace')
plt.ylabel('AMAT')
plt.title('Comparación de AMAT en L1, L2 y L3')
plt.xticks(rotation=90)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Guardar la gráfica
output_dir = 'Graficas'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
plt.savefig(os.path.join(output_dir, 'comparacion_amat.png'))
plt.show()