
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
file_path = "datos_paises_procesados (2).xlsx"
df = pd.read_excel(file_path)

st.set_page_config(page_title="Análisis de Países", layout="wide")

# Función para la página de descripción
def descripcion():
    st.title("Descripción del Proyecto")
    st.write("""
    Esta aplicación permite analizar y visualizar datos de países, proporcionando 
    información sobre población, área, número de idiomas, zonas horarias y más. 
    Los datos han sido procesados y están listos para explorarse.
    """)
    st.write("### Variables principales:")
    st.write("""
    - **Nombre del País**: Nombre común del país.
    - **Región Geográfica**: Región a la que pertenece el país.
    - **Población Total**: Número total de habitantes.
    - **Área (km²)**: Tamaño del territorio en kilómetros cuadrados.
    - **Número de Fronteras**: Cantidad de países limítrofes.
    - **Número de Idiomas**: Idiomas oficiales del país.
    - **Número de Zonas Horarias**: Cantidad de zonas horarias asociadas.
    """)

# Función para la página de datos
def datos():
    st.title("Interacción con los Datos")
    st.dataframe(df)

    # Selección de columna
    columna = st.selectbox("Seleccionar columna para análisis", df.select_dtypes(include="number").columns)
    st.write(f"**Media**: {df[columna].mean():,.2f}")
    st.write(f"**Mediana**: {df[columna].median():,.2f}")
    st.write(f"**Desviación estándar**: {df[columna].std():,.2f}")

    # Ordenar los datos
    orden = st.radio("Ordenar los datos", ["Ascendente", "Descendente"])
    df_ordenado = df.sort_values(by=columna, ascending=(orden == "Ascendente"))
    st.write("Datos ordenados:")
    st.dataframe(df_ordenado)

    # Filtrar los datos
    filtro_valor = st.slider(f"Filtrar {columna}", 
                             float(df[columna].min()), 
                             float(df[columna].max()), 
                             (float(df[columna].min()), float(df[columna].max())))
    df_filtrado = df[(df[columna] >= filtro_valor[0]) & (df[columna] <= filtro_valor[1])]
    st.write("Datos filtrados:")
    st.dataframe(df_filtrado)

    # Botón para descargar datos filtrados
    if st.button("Descargar Datos Filtrados"):
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button("Descargar CSV", csv, "datos_filtrados.csv", "text/csv")

# Función para la página de gráficos
def graficos():
    st.title("Visualización de Datos")

    # Selección de ejes
    x = st.selectbox("Seleccionar eje X", df.select_dtypes(include="number").columns)
    y = st.selectbox("Seleccionar eje Y", df.select_dtypes(include="number").columns)

    # Selección de tipo de gráfico
    tipo = st.radio("Seleccionar tipo de gráfico", ["Línea", "Barras", "Dispersión"])

    # Rango personalizado para los ejes
    rango_x = st.slider(f"Rango del eje X ({x})", 
                        float(df[x].min()), float(df[x].max()), 
                        (float(df[x].min()), float(df[x].max())))
    rango_y = st.slider(f"Rango del eje Y ({y})", 
                        float(df[y].min()), float(df[y].max()), 
                        (float(df[y].min()), float(df[y].max())))

    # Crear gráfico
    fig, ax = plt.subplots()
    if tipo == "Línea":
        ax.plot(df[x], df[y])
    elif tipo == "Barras":
        ax.bar(df[x], df[y])
    elif tipo == "Dispersión":
        ax.scatter(df[x], df[y])

    ax.set_xlim(rango_x)
    ax.set_ylim(rango_y)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    st.pyplot(fig)

    # Descargar gráfico
    if st.button("Descargar Gráfico"):
        from io import BytesIO
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        buffer.seek(0)
        st.download_button("Descargar Gráfico", buffer, file_name="grafico.png", mime="image/png")

# Navegación entre páginas
paginas = {
    "Descripción": descripcion,
    "Datos": datos,
    "Gráficos": graficos,
}

st.sidebar.title("Navegación")
pagina = st.sidebar.radio("Seleccionar página", list(paginas.keys()))
paginas[pagina]()
