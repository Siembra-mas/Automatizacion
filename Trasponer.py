import os
import pandas as pd

# Carpeta de entrada y salida
carpeta_entrada = "CsvLimpio"
carpeta_salida = "CsvMesComoFila"

os.makedirs(carpeta_salida, exist_ok=True)
archivos_procesados = 0

for subcarpeta in os.listdir(carpeta_entrada):
    ruta_subcarpeta = os.path.join(carpeta_entrada, subcarpeta)

    if os.path.isdir(ruta_subcarpeta):
        for archivo_csv in os.listdir(ruta_subcarpeta):
            if archivo_csv.endswith(".csv"):
                ruta_csv = os.path.join(ruta_subcarpeta, archivo_csv)

                # Leer el archivo CSV
                df = pd.read_csv(ruta_csv)

                # Establecer "AÑO" como índice
                df.set_index("AÑO", inplace=True)

                # Transponer el DataFrame: meses como filas, años como columnas
                df_t = df.T
                df_t.index.name = "MES"

                # Convertir el índice (meses) a entero por si es string
                df_t.index = df_t.index.astype(int)

                # Resetear índice para que MES sea columna
                df_t.reset_index(inplace=True)

                # Guardar archivo con nuevo nombre
                nombre_sin_ext = os.path.splitext(archivo_csv)[0]
                nombre_traspuesto = nombre_sin_ext + "_MesComoFila.csv"
                carpeta_salida_sub = os.path.join(carpeta_salida, subcarpeta)
                os.makedirs(carpeta_salida_sub, exist_ok=True)
                ruta_salida = os.path.join(carpeta_salida_sub, nombre_traspuesto)

                df_t.to_csv(ruta_salida, index=False)
                archivos_procesados += 1

                print(f"✅ Guardado: {ruta_salida}")

print(f"\n📈 Se generaron {archivos_procesados} archivos con meses como números (1 al 12).")
