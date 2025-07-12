import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Limpieza de datos", layout="centered")
st.title("Limpieza y conversión de archivos")

opcion = st.radio("¿Qué tipo de archivo vas a subir?", ["Archivo TXT", "Archivo CSV"])

archivo = st.file_uploader("📁 Selecciona tu archivo", type=["txt", "csv"])

if archivo:
    if opcion == "Archivo TXT":
        bloque = st.text_input("🔍 Nombre del bloque a extraer (ej. LLUVIA MÁXIMA 24 H.)", "")
        anio_inicio = st.number_input("Año inicial", min_value=1900, max_value=2100, value=2015)
        anio_fin = st.number_input("Año final", min_value=1900, max_value=2100, value=2025)

        if anio_inicio > anio_fin:
            st.error("❌ El año inicial no puede ser mayor que el año final.")
        elif bloque:
            if st.button("Procesar archivo TXT"):
                contenido = archivo.read().decode('utf-8', errors='ignore').splitlines()
                extraer = False
                datos = []

                for linea in contenido:
                    linea = linea.strip()
                    if bloque.upper() in linea.upper():
                        extraer = True
                        continue
                    if extraer and linea.upper().startswith("AÑO"):
                        encabezados = linea.split()
                        datos.append(encabezados)
                        continue
                    if extraer:
                        if linea and linea[0:4].isdigit():
                            anio = int(linea[0:4])
                            if anio_inicio <= anio <= anio_fin:
                                fila = linea.split()
                                datos.append(fila)
                        elif not linea or not linea[0:4].isdigit():
                            break

                if datos:
                    df = pd.DataFrame(datos[1:], columns=datos[0])
                    
                    # --- Vista previa del DataFrame ---
                    st.subheader("Vista Previa del Archivo Extraído")
                    st.dataframe(df)

                    # Input para el nombre del archivo final
                    nombre_archivo = st.text_input("✍️ Escribe el nombre para el archivo extraído (sin extensión)", value="bloque_extraido")
                    if nombre_archivo.strip():
                        csv_buffer = io.StringIO()
                        df.to_csv(csv_buffer, index=False)
                        st.success("✅ Archivo procesado correctamente.")
                        st.download_button(
                            "📥 Descargar CSV",
                            data=csv_buffer.getvalue(),
                            file_name=f"{nombre_archivo.strip()}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("Por favor, escribe un nombre válido para el archivo de descarga.")
                else:
                    st.error("❌ No se encontraron datos para ese bloque.")
        else:
            st.info("Por favor, ingresa el nombre del bloque a extraer.")

    elif opcion == "Archivo CSV":
        if st.button("Limpiar archivo CSV"):
            try:
                df = pd.read_csv(archivo)

                st.write("Columnas originales:", list(df.columns))

                # --- Lógica para eliminar columnas (más robusta) ---
                eliminar_keywords = ['ACUM', 'PROM', 'MESES'] # Palabras clave a buscar
                cols_a_eliminar = []
                for col_name in df.columns:
                    # Normalizar nombre de columna: eliminar todos los espacios y convertir a mayúsculas
                    normalized_col_name_no_space = "".join(col_name.split()).upper()
                    for keyword in eliminar_keywords:
                        if keyword in normalized_col_name_no_space: # Si la palabra clave está contenida en el nombre de la columna (sin espacios)
                            cols_a_eliminar.append(col_name)
                            break # Pasa a la siguiente columna una vez que se encuentra una coincidencia

                if cols_a_eliminar:
                    # Eliminar columnas, usando set para asegurar unicidad si una columna coincide con varias palabras clave
                    df = df.drop(columns=list(set(cols_a_eliminar)))
                    st.write("Columnas eliminadas:", list(set(cols_a_eliminar)))
                else:
                    st.write("No se encontraron columnas como 'ACUM', 'PROM' o 'MESES' para eliminar.")

                # --- Lógica para renombrar columnas de meses (más precisa) ---
                columnas = list(df.columns)
                if len(columnas) < 2:
                    st.error("❌ No hay columnas suficientes para renombrar después de la eliminación.")
                else:
                    # Mapeo de abreviaturas y nombres completos de meses en español a números
                    meses_map = {
                        'ENE': '1', 'FEB': '2', 'MAR': '3', 'ABR': '4', 'MAY': '5', 'JUN': '6',
                        'JUL': '7', 'AGO': '8', 'SEP': '9', 'OCT': '10', 'NOV': '11', 'DIC': '12',
                        'ENERO': '1', 'FEBRERO': '2', 'MARZO': '3', 'ABRIL': '4', 'MAYO': '5', 'JUNIO': '6',
                        'JULIO': '7', 'AGOSTO': '8', 'SEPTIEMBRE': '9', 'OCTUBRE': '10', 'NOVIEMBRE': '11', 'DICIEMBRE': '12'
                    }
                    
                    nuevas_columnas = []
                    for i, col in enumerate(df.columns):
                        if i == 0 and col.strip().upper() == 'AÑO': # Mantener 'AÑO' tal cual
                            nuevas_columnas.append(col)
                        else:
                            # Normalizar el nombre de la columna para buscar en el mapa de meses
                            normalized_col = col.strip().upper()
                            renamed = False
                            for month_abbr, month_num in meses_map.items():
                                # Verificar si el nombre de la columna comienza con la abreviatura o nombre completo del mes
                                if normalized_col.startswith(month_abbr):
                                    nuevas_columnas.append(month_num)
                                    renamed = True
                                    break
                            if not renamed:
                                nuevas_columnas.append(col) # Si no es un mes reconocido, mantener su nombre original

                    df.columns = nuevas_columnas
                    st.write("Nuevos nombres de columnas:", list(df.columns))

                    # --- Vista previa del DataFrame ---
                    st.subheader("Vista Previa del Archivo Limpio")
                    st.dataframe(df)

                    # Input para nombre del archivo final
                    nombre_archivo = st.text_input("✍️ Escribe el nombre para el archivo limpio (sin extensión)", value="archivo_limpio")

                    if nombre_archivo.strip():
                        csv_buffer = io.StringIO()
                        df.to_csv(csv_buffer, index=False)
                        st.success("✅ Archivo limpiado correctamente.")
                        st.download_button(
                            "📥 Descargar CSV limpio",
                            data=csv_buffer.getvalue(),
                            file_name=f"{nombre_archivo.strip()}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("Por favor, escribe un nombre válido para el archivo de descarga.")

            except Exception as e:
                st.error(f"❌ Error al procesar el archivo: {e}")
