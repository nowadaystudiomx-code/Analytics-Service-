import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import clientes.nowadays_studio as nowadays_studio
import clientes.botanerolimon as botanerolimon
import clientes.nuelengiere as nue

# --- Cargar configuración ---
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# --- Inicializar authenticator ---
authenticator = stauth.Authenticate(
    config['credentials']['usernames'],
    config.get('cookie', {}).get('name', 'cookie-name'),
    config.get('cookie', {}).get('key', 'cookie-key'),
    config.get('cookie', {}).get('expiry_days', 30)
)

# --- Mostrar el widget de login ---
# Usamos la versión que escribe el estado en st.session_state
try:
    # Algunas versiones usan (name, auth_status, username) = authenticator.login(...)
    # pero tu flujo actual utiliza st.session_state. Llamamos al login y luego leemos st.session_state.
    authenticator.login(location='sidebar')
except Exception:
    # fallback a llamada con parámetros nombrados si la firma difiere
    authenticator.login("Login", "sidebar")

# --- Leer estado seguro desde session_state ---
auth_status = st.session_state.get("authentication_status", None)
name = st.session_state.get("name", "")
username = st.session_state.get("username", "")

if auth_status:
    authenticator.logout("Salir", location='sidebar')
    st.sidebar.title(f"Bienvenido, {name}")
    opcion = st.sidebar.selectbox("Sección", ["Dashboard"])

    if opcion == "Dashboard":
        # Redirige por username a su módulo correspondiente
        if username == "leona":
            nowadays_studio.mostrar()
        elif username == "botanerolimon":
            botanerolimon.mostrar()
        elif username == "nue":
            nue.mostrar()
        else:
            # default o usuario admin
            nowadays_studio.mostrar()

elif auth_status is False:
    st.error("Usuario o contraseña incorrectos")
elif auth_status is None:
    st.warning("Ingresa tus credenciales")
