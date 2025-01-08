import streamlit as st
from calculos import calcular_calificacion_final
from datetime import datetime 

# Título de la aplicación
st.title("Evaluación Financiera - Dictamen Final")

# Sección: Datos del Cliente
st.header("Datos del Cliente")
persona = st.selectbox("Persona", ['física', 'jurídica'])
# Mostrar perfil comercial solo si persona es "física"
perfil_comercial = None
if persona == 'física':
    perfil_comercial = st.selectbox("Perfil Comercial", ['asalariado', 'profesional independiente', 'empresario'])
nombre = st.text_input("Nombre")
apellido = st.text_input("Apellido")
fecha_nacimiento = st.date_input("Fecha de Nacimiento", format="DD/MM/YYYY")
ci = st.text_input("Cédula de Identidad")

# Sección: Datos de Evaluación
st.header("Datos de Evaluación")
ingresos = st.number_input("Ingresos (en millones)", min_value=0, step=1)
posee_bienes = st.selectbox("Posee Bienes", ['no', 'vehículo', 'inmueble', 'vehículo e inmueble'])
antiguedad_laboral = st.number_input("Antigüedad Laboral (en años)", min_value=0, step=1)

# Sección: Datos de Operación
st.header("Datos Operación")
producto = st.selectbox(
    "Seleccione un Producto",
    ["Producto 1", "Producto 2", "Producto 3"],
    index=0  # Opción seleccionada por defecto
)
monto_solicitado = st.number_input("Monto Solicitado", min_value=1, step=1, value=1)
plazo = st.number_input("Plazo (meses)", min_value=1, step=1, value=12)
garantia = st.number_input("Garantía", min_value=0, step=1, value=1)
cuota = st.number_input("Cuota", min_value=0.0, step=0.01, value=1.0)



# Botón para calcular
if st.button("Calcular Dictamen Final"):
    # Simulación de parámetros adicionales
    edad = 30  # Ejemplo: edad fija
    faja = 'I-L'  # Ejemplo: rango de scoring fijo
    dti = 30  # Ejemplo: ratio deuda/ingreso fijo

    # Llamada a la función de cálculo final
    puntaje, dictamen = calcular_calificacion_final(
        edad=edad,
        ingresos=ingresos,
        faja=faja,
        antiguedad=antiguedad_laboral,
        activos=posee_bienes,
        dti=dti
    )

    # Mostrar resultados
    st.subheader("Resultado de la Evaluación")
    st.write(f"Puntaje Final: {puntaje}")
    st.write(f"Dictamen Final: {dictamen}")
