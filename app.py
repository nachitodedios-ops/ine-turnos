import streamlit as st
import time

# Configuración de la página móvil
st.set_page_config(page_title="Módulo INE - Turnos Virtuales", page_icon="🇲🇽", layout="centered")

# Inicializar la base de datos de turnos en la memoria del servidor si no existe
if "lista_espera" not in st.session_state:
    st.session_state.lista_espera = []  # Lista de turnos activos
if "turno_actual" not in st.session_state:
    st.session_state.turno_actual = None  # Turno en ventanilla
if "contador_turnos" not in st.session_state:
    st.session_state.contador_turnos = 0  # Contador incremental

# Diseño de la interfaz
st.title("🇲🇽 Módulo de Atención INE")
st.subheader("Sistema de Turnos para Ciudadanos Sin Cita")

# Crear pestañas para separar la vista del ciudadano y del operador
tab_ciudadano, tab_operador = st.tabs(["📱 Vista Ciudadano", "💼 Panel Operador INE"])

# --- VISTA CIUDADANO ---
with tab_ciudadano:
    st.write("Bienvenido al módulo. Si acudiste sin cita, obtén tu turno digital aquí para evitar hacer fila de pie.")
    
    # Formulario para obtener turno
    with st.form("registro_turno"):
        nombre = st.text_input("Tu Nombre o Iniciales:", placeholder="Ej. Carlos M.")
        tramite = st.selectbox("Selecciona tu trámite:", [
            "Inscripción (Primera Vez)", 
            "Corrección de Datos", 
            "Cambio de Domicilio", 
            "Reposición / Renovación"
        ])
        
        # Validación de documentos (Checklist)
        st.write("⚠️ **Verificación de documentos indispensables:**")
        doc1 = st.checkbox("Llevo Acta de Nacimiento original")
        doc2 = st.checkbox("Llevo Identificación con foto vigente")
        doc3 = st.checkbox("Llevo Comprobante de Domicilio reciente (no mayor a 3 meses)")
        
        boton_turno = st.form_submit_button("Generar Mi Turno Digital")
        
        if boton_turno:
            if not nombre:
                st.error("Por favor, ingresa tu nombre.")
            elif not (doc1 and doc2 and doc3):
                st.error("Debes contar con los 3 documentos en original para poder ser atendido.")
            else:
                st.session_state.contador_turnos += 1
                nuevo_turno = {
                    "id": st.session_state.contador_turnos,
                    "nombre": nombre,
                    "tramite": tramite
                }
                st.session_state.lista_espera.append(nuevo_turno)
                st.success(f"¡Turno generado con éxito! Tu número es el: **#{st.session_state.contador_turnos}**")
                st.balloons()

    st.divider()
    
    # Estado de la fila en tiempo real
    st.markdown("### 📊 Estado de la Fila Actual")
    
    if st.session_state.turno_actual:
        st.info(f"📢 **EN VENTANILLA AHORA:** Turno **#{st.session_state.turno_actual['id']}** ({st.session_state.turno_actual['nombre']})")
    else:
        st.warning("Aún no se han llamado turnos el día de hoy.")
        
    personas_adelante = len(st.session_state.lista_espera)
    st.metric(label="Personas esperando en la fila", value=personas_adelante)
    
    if personas_adelante > 0:
        tiempo_estimado = personas_adelante * 12 # 12 minutos promedio por persona
        st.write(f"⏱️ Tiempo estimado de espera aproximado: **{tiempo_estimado} minutos**.")
        st.caption("Puedes sentarte o retirarte unos minutos; refresca esta pantalla para monitorear tu lugar.")
    
    if st.button("🔄 Actualizar Fila"):
        st.rerun()

# --- PANEL OPERADOR ---
with tab_operador:
    st.markdown("### 🔑 Control de Turnos (Solo Personal del INE)")
    st.write("Usa este panel en una tablet o computadora para avanzar la fila de usuarios sin cita.")
    
    if st.button("🔔 LLAMAR SIGUIENTE TURNO", type="primary"):
        if len(st.session_state.lista_espera) > 0:
            st.session_state.turno_actual = st.session_state.lista_espera.pop(0)
            st.success(f"Llamando al Turno #{st.session_state.turno_actual['id']} - {st.session_state.turno_actual['nombre']}")
        else:
            st.warning("No hay más ciudadanos en la fila de espera.")
            
    st.divider()
    st.write("📋 **Próximos en la fila:**")
    if len(st.session_state.lista_espera) > 0:
        for idx, t in enumerate(st.session_state.lista_espera):
            st.write(f"**{idx+1}.** Turno #{t['id']} - {t['nombre']} ({t['tramite']})")
    else:
        st.write("*Fila vacía*")
