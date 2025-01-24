import streamlit as st
from calculos import calcular_calificacion_final, calcular_edad, calcular_dti
from datetime import datetime 
from pdf_maker import generate_detailed_pdf
from io import BytesIO
import pandas as pd
import openpyxl

# Opciones válidas
opciones_antiguedad = ["6 meses a un año", "1 a 2 años", "3 a 5 años", "Más de 5 años"]
opciones_garantia = ["ASF", "Hipotecaria", "Prendaria", "Codeudoría"]
opciones_perfil_comercial = ['Asalariado', 'Profesional Independiente']
opciones_bienes = ['No', 'Vehículo', 'Inmueble', 'Vehículo e Inmueble']

# Título de la aplicación
st.title("Evaluación Financiera - Dictamen Final")

# Datos del Cliente
st.header("Datos del Cliente")
col1, col2 = st.columns(2)
with col1:
    persona = st.selectbox("Persona", ['Física', 'Jurídica'])
    nombre = st.text_input("Nombre y Apellido")
    ci = st.text_input("Cédula de Identidad/RUC")
with col2:
    if persona == 'Física':
        perfil_comercial = st.selectbox("Perfil Comercial", opciones_perfil_comercial)
    fecha_nacimiento = st.date_input("Fecha de Nacimiento/Constitución", format="DD/MM/YYYY")
    if fecha_nacimiento:
        edad = calcular_edad(fecha_nacimiento)
        st.write(f"Edad: {edad} años")

# Datos de Evaluación
st.header("Datos de Evaluación")
col3, col4 = st.columns(2)
with col3:
    ingresos = st.number_input("Ingresos", min_value=1, step=1, value=1)
    antiguedad_laboral = st.selectbox("Antigüedad Laboral:", opciones_antiguedad)
with col4:
    posee_bienes = st.selectbox("Posee Bienes", opciones_bienes)
    empresa = st.text_input("Empresa")
    faja = st.text_input("Faja Scoring Informconf")

# Datos de Operación
st.header("Datos Operación")
col5, col6 = st.columns(2)
with col5:
    producto = st.selectbox("Seleccione un Producto", ["Producto 1", "Producto 2", "Producto 3"], index=0)
    monto_solicitado = st.number_input("Monto Solicitado", min_value=1, step=1, value=1)
    cuota = st.number_input("Cuota", min_value=0, step=1, value=1)
with col6:
    plazo = st.number_input("Plazo (meses)", min_value=1, step=1, value=12)
    garantia = st.selectbox("Seleccione el tipo de garantía:", opciones_garantia)

# Subir Planillas Excel
st.header("Cargar Planillas Excel")
archivo_1 = st.file_uploader("Subir Planilla de Deudas", type=["xlsx"])
if archivo_1:
    df1 = pd.read_excel(archivo_1)
    st.write("Deuda Financiera:")
    st.dataframe(df1)
    deuda_financiera = df1.iloc[:, 5].dropna().astype(float).sum()
else:
    deuda_financiera = 0

# Comentarios
comentarios = st.text_area("Comentarios")

# Botón para calcular y generar PDF
if st.button("Calcular Dictamen Final y Generar PDF"):
    deudas = deuda_financiera
    puntaje, dictamen = calcular_calificacion_final(
        edad=edad,
        ingresos=ingresos,
        faja=faja,
        antiguedad=antiguedad_laboral,
        activos=posee_bienes,
        deudas=deudas,
        cuota=cuota
    )

    # Guardar resultados en session_state
    st.session_state['resultado'] = {
        "puntaje": puntaje,
        "dictamen": dictamen,
        "deudas": deudas,
        "dti": calcular_dti(deudas, ingresos, cuota)
    }

    # Generar PDF detallado
    pdf_buffer = generate_detailed_pdf(
        nombre=nombre,
        profesion=perfil_comercial,
        ingresos=ingresos,
        fecha_nacimiento=fecha_nacimiento,
        empresa=empresa,
        perfil_comercial=perfil_comercial,
        producto=producto,
        monto_solicitado=monto_solicitado,
        plazo=plazo,
        cuota=cuota,
        garantia=garantia,
        scoring=faja,
        deuda_financiera=deuda_financiera,
        ratio_deuda_ingresos=st.session_state['resultado']['dti'],
        puntaje=puntaje,
        dictamen=dictamen,
        comentarios=comentarios
    )
    st.download_button(
        label="Download PDF",
        data=pdf_buffer,
        file_name="financial_report.pdf",
        mime="application/pdf"
    )

# Mostrar resultados si están guardados
if 'resultado' in st.session_state:
    st.subheader("Resultado de la Evaluación")
    resultado = st.session_state['resultado']
    st.write(f"Puntaje Final: {resultado['puntaje']}")
    st.write(f"Dictamen Final: {resultado['dictamen']}")
    st.write(f"Deudas Totales: {resultado['deudas']}")
    st.write(f"DTI: {resultado['dti']}")