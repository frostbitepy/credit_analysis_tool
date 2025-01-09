import streamlit as st
from calculos import calcular_calificacion_final, calcular_edad
from datetime import datetime 
import pandas as pd
import openpyxl

# Opciones válidas para la antigüedad laboral
opciones_antiguedad = [
    "6 meses a un año",
    "1 a 2 años",
    "3 a 5 años",
    "Más de 5 años"
]
# Opciones válidas para la garantía
opciones_garantia = ["ASF", "Hipotecaria", "Prendaria", "Codeudoría"]
# Opciones validas para perfil comercial
opciones_perfil_comercial = ['Asalariado', 'Profesional Independiente' ]
# Opciones validas bienes
opciones_bienes = ['No', 'Vehículo', 'Inmueble', 'Vehículo e Inmueble']


# Título de la aplicación
st.title("Evaluación Financiera - Dictamen Final")

# Sección: Datos del Cliente
st.header("Datos del Cliente")

col1, col2 = st.columns(2)
with col1:
    persona = st.selectbox("Persona", ['Física', 'Jurídica'])
    nombre = st.text_input("Nombre y Apellido")
    ci = st.text_input("Cédula de Identidad/RUC")

with col2:
    # Mostrar perfil comercial solo si persona es "física"
    if persona == 'Física':
        perfil_comercial = st.selectbox("Perfil Comercial", opciones_perfil_comercial)
    fecha_nacimiento = st.date_input("Fecha de Nacimiento/Constitución", format="DD/MM/YYYY")
    # Calcular y mostrar la edad debajo de la fecha de nacimiento
    if fecha_nacimiento:
        edad = calcular_edad(fecha_nacimiento)
        st.write(f"Edad: {edad} años")

# Sección: Datos de Evaluación
st.header("Datos de Evaluación")

col3, col4 = st.columns(2)
with col3:
    ingresos = st.number_input("Ingresos", min_value=0, step=1)
    antiguedad_laboral = st.selectbox("Antigüedad Laboral:", [
        "6 meses a un año",
        "1 a 2 años",
        "3 a 5 años",
        "Más de 5 años"
    ])

with col4:
    posee_bienes = st.selectbox("Posee Bienes", opciones_bienes)
    empresa = st.text_input("Empresa")
    faja = st.text_input("Faja Scoring Informconf")

# Sección: Datos de Operación
st.header("Datos Operación")

col5, col6 = st.columns(2)
with col5:
    producto = st.selectbox(
        "Seleccione un Producto",
        ["Producto 1", "Producto 2", "Producto 3"],
        index=0
    )
    monto_solicitado = st.number_input("Monto Solicitado", min_value=1, step=1, value=1)
    cuota = st.number_input("Cuota", min_value=0, step=1, value=1)

with col6:
    plazo = st.number_input("Plazo (meses)", min_value=1, step=1, value=12)
    garantia = st.selectbox("Seleccione el tipo de garantía:", opciones_garantia)


# Sección: Subir Planillas Excel
st.header("Cargar Planillas Excel")
col1, col2 = st.columns(2)

archivo_1 = st.file_uploader("Subir Planilla de Deuda Financiera", type=["xlsx"])
if archivo_1:
    df1 = pd.read_excel(archivo_1)
    st.write("Deuda Financiera:")
    st.dataframe(df1)  # Muestra las primeras filas para verificar
    deuda_financiera = df1.iloc[:, 4].dropna().astype(float).sum()

archivo_2 = st.file_uploader("Subir Planilla de Deuda Comercial", type=["xlsx"])
if archivo_2:
    df2 = pd.read_excel(archivo_2)
    st.write("Deuda Comercial:")
    st.dataframe(df2)  # Muestra las primeras filas para verificar
    deuda_comercial = df2.iloc[:, 4].dropna().astype(float).sum()


# Botón para calcular
if st.button("Calcular Dictamen Final"):
    # Simulación de parámetros adicionales
    dti = 30  # Ejemplo: ratio deuda/ingreso fijo

    # Llamada a la función de cálculo final
    puntaje, dictamen = calcular_calificacion_final(
        edad=edad,
        ingresos=ingresos,
        faja=faja,
        antiguedad=antiguedad_laboral,
        activos=posee_bienes,
        deudas=deuda_financiera+deuda_comercial
    )

    # Mostrar resultados
    st.subheader("Resultado de la Evaluación")
    st.write(f"Puntaje Final: {puntaje}")
    st.write(f"Dictamen Final: {dictamen}")
    st.write(f"Nombre: {nombre}")
    st.write(f"Edad: {edad}")
    st.write(f"CI/RUC: {ci}")
    st.write(f"Ingresos: {ingresos}")
    st.write(f"Deuda Total: {deuda_comercial+deuda_financiera}")
