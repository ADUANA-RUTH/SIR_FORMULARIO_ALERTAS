import streamlit as st
import oracledb
import psycopg2
from datetime import datetime

def conectar_postgres():
    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        port=st.secrets["postgres"]["port"],
        dbname=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"]
    )

def crear_tabla_si_no_existe():
    conn = conectar_postgres()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS registros_temp (
            id SERIAL PRIMARY KEY,
            nombre TEXT,
            correo TEXT,
            edad INTEGER,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    
crear_tabla_si_no_existe()

import streamlit as st
import psycopg2
from datetime import datetime

def conectar_postgres():
    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        port=st.secrets["postgres"]["port"],
        dbname=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"]
    )

st.title("Formulario prueba")

nombre = st.text_input("Nombre")
correo = st.text_input("Correo")
edad = st.number_input("Edad", min_value=0, max_value=120, step=1)

if st.button("Guardar"):
    try:
        conn = conectar_postgres()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO registros_temp (nombre, correo, edad)
            VALUES (%s, %s, %s)
        """, (nombre, correo, edad))
        conn.commit()
        st.success("✅ Registro guardado en base temporal")
    except Exception as e:
        st.error(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()
