import streamlit as st
import oracledb

# Usar modo thin (sin necesidad de Oracle Client)
oracledb.init_oracle_client(lib_dir=None)  # No hace nada en modo thin

# Conexión a Oracle
def conectar_oracle():
    conn = oracledb.connect(
        user=st.secrets["oracle"]["user"],
        password=st.secrets["oracle"]["password"],
        dsn=f"{st.secrets['oracle']['host']}:{st.secrets['oracle']['port']}/{st.secrets['oracle']['service']}",
        mode=oracledb.DEFAULT_AUTH
    )
    return conn

# Interfaz del formulario
st.title("Formulario de Registro")

nombre = st.text_input("Nombre completo")
correo = st.text_input("Correo electrónico")
edad = st.number_input("Edad", min_value=0, max_value=120, step=1)

if st.button("Guardar"):
    try:
        conn = conectar_oracle()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO RM_pruebas_usuarios (nombre, correo, edad)
            VALUES (:1, :2, :3)
        """, (nombre, correo, edad))
        conn.commit()
        st.success("✅ Registro guardado con éxito.")
    except Exception as e:
        st.error(f"❌ Error al guardar: {e}")
    finally:
        cursor.close()
        conn.close()
