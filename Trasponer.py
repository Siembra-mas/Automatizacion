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

                # Leer CSV
                df = pd.read_csv(ruta_csv)

                # Asegurar que AÑO sea índice
                df.set_index("AÑO", inplace=True)

                # Transponer (meses como filas, años como columnas)
                df_t = df.T
                df_t.index.name = "MES"

                # Rellenar NaN con el promedio de cada columna
                df_t = df_t.fillna(df_t.mean(numeric_only=True))

                # Asegurar que MES sea numérico
                df_t.index = df_t.index.astype(int)
                df_t.reset_index(inplace=True)  # MES como columna

                # Ruta de salida con el mismo nombre que el archivo original
                carpeta_salida_sub = os.path.join(carpeta_salida, subcarpeta)
                os.makedirs(carpeta_salida_sub, exist_ok=True)
                ruta_salida = os.path.join(carpeta_salida_sub, archivo_csv)

                # Guardar archivo
                df_t.to_csv(ruta_salida, index=False)
                archivos_procesados += 1

                print(f"✅ Guardado: {ruta_salida}")

print(f"\n📈 Se procesaron {archivos_procesados} archivos. Meses como filas, sin renombrar archivos.")
