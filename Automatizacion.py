import os
import pandas as pd
import csv

# Ruta del archivo de origen
ruta_archivo = r"TXT/AZUETA.txt"

# Diccionario con los nombres a buscar y sus etiquetas de salida
bloques_datos = {
    "LLUVIA MÁXIMA 24 H.": "LLUVIA MÁXIMA 24 H.",
    "LLUVIA TOTAL MENSUAL": "LLUVIA TOTAL MENSUAL",
    "EVAPORACIÓN MENSUAL": "EVAPORACIÓN MENSUAL",
    "TEMPERATURA MÁXIMA PROMEDIO": "TEMP MÁX PROM",
    "TEMPERATURA MÁXIMA EXTREMA": "TEMP MÁX EXT",
    "TEMPERATURA MÍNIMA PROMEDIO": "TEMP MÍN PROM",
    "TEMPERATURA MÍNIMA EXTREMA": "TEMP MÍN EXT",
    "TEMPERATURA MEDIA MENSUAL": "TEMP MEDIA",
}

# Carpeta de salida para CSV limpio
CarpetaNom = "AZUETA"

for Nombre, Etiqueta in bloques_datos.items():
    datos = []
    extraer = False

    NombreN = Etiqueta + "-" + CarpetaNom

    # Leer archivo línea por línea
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea = linea.strip()

            if Nombre in linea.upper():
                extraer = True
                continue

            if extraer and linea.upper().startswith("AÑO"):
                encabezados = linea.split()
                datos.append(encabezados)
                continue

            if extraer:
                if linea and linea[0:4].isdigit():
                    anio = int(linea[0:4])
                    if 2015 <= anio <= 2025:
                        fila = linea.split()
                        datos.append(fila)
                elif linea == "":
                    break

    # Guardar CSV intermedio
    ruta_csv_temporal = f"TXT/{NombreN}.csv"
    with open(ruta_csv_temporal, "w", newline='', encoding='utf-8') as salida:
        escritor = csv.writer(salida)
        escritor.writerows(datos)

    print(f"✅ Datos extraídos y guardados temporalmente: {NombreN}")

    # Limpieza del CSV
    df = pd.read_csv(ruta_csv_temporal)

    # Elimina columnas si existen
    for col in ['ACUM', 'PROM', 'MESES']:
        if col in df.columns:
            df = df.drop(columns=[col])

    # Renombra columnas (ENE → 1, FEB → 2, etc.)
    nuevas_columnas = ['AÑO'] + [str(i) for i in range(1, len(df.columns))]
    df.columns = nuevas_columnas

    # Crear carpeta de salida si no existe
    carpeta_salida = os.path.join("CsvLimpio", CarpetaNom)
    os.makedirs(carpeta_salida, exist_ok=True)

    ruta_csv_final = os.path.join(carpeta_salida, f"{NombreN}.csv")
    df.to_csv(ruta_csv_final, index=False)

    # Eliminar CSV temporal
    os.remove(ruta_csv_temporal)
    print(f"✅ Archivo limpio guardado como: {ruta_csv_final}")
    print(f"🗑️ Archivo temporal eliminado: {ruta_csv_temporal}\n")

print("🏁 Procesamiento completo de todos los bloques.")
