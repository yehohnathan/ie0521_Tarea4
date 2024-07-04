# Tarea 4: Simulador de Memoria Caché
## Ejecución del programa

### Parte 1. Caché de un único nivel

Para ejecutar el simulador de memoria caché de la Parte 1 de manera personalizada, sigue estos pasos:

1. **Ubicación del directorio:**
   Dirígete a la carpeta raíz del proyecto `ie0521_Tarea4`. Supondremos que esta carpeta contiene todos los programas y archivos relacionados con la tarea.

   ```bash
   user@user:~/ie0521_Tarea4$
   ```

2. **Comando de ejecución:**
   Ejecuta el simulador utilizando el siguiente comando como ejemplo:

   ```bash
   python3 src/base_parte1/cache_sim.py -s 128 -a 16 -b 64 -r l -t Traces/470.lbm-1274B.trace.txt.gz
   ```

   Donde los argumentos de entrada (`-s`, `-a`, `-b`, `-r`, `-t`) tienen los siguientes significados:

   - `-s`: Capacidad del caché en kilobytes. Debe ser un número entero que indica la capacidad total del caché, usando potencias de 2 (2, 4, 8, 16, 64, 128, etc.).
   - `-a`: Asociatividad del caché. Es un número entero que indica la cantidad de vías (`ways`) en cada conjunto (`set`). Por ejemplo, 1 indica mapeo directo, 8 indica 8-way set associative, etc., usando potencias de 2 (1, 2, 4, 8, 16, etc.).
   - `-b`: Tamaño del bloque en bytes. Es un número entero que indica cuántos bytes por bloque tiene el caché, usando potencias de 2 (2, 4, 8, 16, 64, 128, etc.).
   - `-r`: Política de reemplazo. Un carácter que indica la política para expulsar bloques del caché. "l" (ele) para LRU (Least Recently Used), "r" (erre) para aleatoria.
   - `-t`: Archivo de traza que contiene las direcciones de memoria a simular.

3. **Resultados esperados:**
   Después de ejecutar el comando, si la simulación es exitosa, deberías ver información similar a la siguiente en la terminal:

   ```
   Resultados de la simulación
   24494, 2.449%
   ```

   Este resultado variará dependiendo de los valores proporcionados en los argumentos de entrada.

Para crear la Parte 2 del programa simulador de memoria caché según los requisitos proporcionados, puedes seguir estos pasos:

### Parte 2. Caché multinivel
#### Ejecución del programa:

1. **Comandos de Ejecución:**

   - Para un caché de primer nivel (L1):
     ```bash
     python3 src/base_parte2/cache_sim.py --l1_s 128 --l1_a 16 -t Traces/401.bzip2-226B.trace.txt.gz
     ```

   - Para un caché de dos niveles (L1 y L2):
     ```bash
     python3 src/base_parte2/cache_sim.py --l1_s 128 --l1_a 16 --l2_s 128 --l2_a 16 -t Traces/401.bzip2-226B.trace.txt.gz
     ```

   - Para un caché de tres niveles (L1, L2 y L3):
     ```bash
     python3 src/base_parte2/cache_sim.py --l1_s 128 --l1_a 16 --l2_s 128 --l2_a 16 --l3_s 128 --l3_a 16 -t Traces/401.bzip2-226B.trace.txt.gz
     ```

2. **Argumentos de Entrada:**

   - Capacidad del caché L1 en kB (`--l1_s`): Número entero que indica la capacidad total del caché L1.
   - Asociatividad del caché L1 (`--l1_a`): Número entero que indica la cantidad de "ways" en cada set del caché L1.
   - Presencia de nivel de caché L2 (`--l2`) y L3 (`--l3`): Banderas que indican la presencia de L2 y L3 respectivamente.
   - Capacidad y asociatividad de los cachés L2 y L3 (`--l2_s`, `--l2_a`, `--l3_s`, `--l3_a`): Definidos de manera similar a L1.
   - Tamaño del bloque en bytes (`-b`): Entero que indica cuántos bytes por bloque tiene cada nivel de caché.
   - Política de reemplazo (`-r`): Carácter que indica la política para expulsar bloques del caché. Únicamente se usará la política LRU.


### Ejecución de Pruebas con Parámetros Definidos

Para realizar un análisis completo de la Parte 1 y la Parte 2 de la tarea, se han automatizado diversas pruebas utilizando los métodos de dos clases: `Automatizador.py` y `AutomatizadorMulticache.py`. Estos métodos son invocados desde el archivo `main.py`, el cual permite al usuario seleccionar qué pruebas desea ejecutar, ya sea para un caché de un solo nivel, cachés multinivel, o ambos de manera secuencial.

**Instrucciones de Ejecución:**

```bash
python3 src/main.py
```

**Interfaz de Usuario:**

Al ejecutar el comando anterior, se muestra la siguiente información en la terminal:

```
Seleccione la prueba que desea ejecutar:
1. Modificar tamaño de caché
2. Modificar asociatividad del caché
3. Modificar tamaño de bloque
4. Modificar política de reemplazo
5. Presencia de caché L1
6. Presencia de caché L2 (configuración a)
7. Presencia de caché L2 (configuración b)
8. Presencia de caché L3 (configuración a)
9. Presencia de caché L3 (configuración b)
Ingrese los números de las pruebas que desea ejecutar separados por espacios:
```

**Ejemplo de Selección de Pruebas:**

El usuario puede ingresar los números de las pruebas que desea ejecutar separados por espacios:

```bash
Ingrese los números de las pruebas que desea ejecutar separados por espacios: 3 5 7
```

Esto ejecutará las pruebas correspondientes, comenzando con "Modificar tamaño de caché" y finalizando con "Presencia de caché L2 (configuración b)". Los resultados de cada prueba se almacenarán en la carpeta `Resultados_P1` para las pruebas de caché de un solo nivel y en `Resultados_P2` para las pruebas de cachés multinivel dentro del directorio `ie0521_Tarea4`.

**Ejemplo de Estructura de Carpetas y Archivos Generados:**

```bash
> ie0521_Tarea4
    > Resultados_P1
        Efecto_tamaño_cache.txt
    > Resultados_P2
        Presencia_L1.txt
        Presencia_L2_b.txt
```

Esta estructura organiza claramente los resultados de las pruebas realizadas según la parte correspondiente del simulador de memoria caché.

Aquí un ejemplo de cómo se debería ver los resultados obtenidos desde un `Efecto_tamaño_cache.txt` (de la misma forma para los demás .txt):

```txt
================= Efecto de tamaño del caché =================
Parámetros fijos:
cache_assoc = 8
block_size = 64
repl_policy = l

+++++++++ Trace 400.perlbench-41B.trace.txt.gz +++++++++
+ Variación de tamaño del caché: 8 +
Resultados de la simulación
1282, 0.128%

+ Variación de tamaño del caché: 16 +
Resultados de la simulación
471, 0.047%

...

```