import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import dashboard, upload, home
import base64


# Establecer la configuración de la página (incluido el color de fondo)
st.set_page_config(
    page_title="Tutu Disfraz - Analytics",  # Título de la pestaña
    page_icon="👗",  # Puedes cambiar esto por el ícono que desees
    layout="wide",  # Opciones: "wide" o "centered"
    initial_sidebar_state="expanded",  # Opciones: "auto", "expanded", "collapsed"
    menu_items={
        'About': f'Pagina Web creada por Sebastian Vega para Tutu Disfraz. Linkedin: https://www.linkedin.com/in/svsm03/',
        'Get help': 'mailto:svsm03@hotmail.com.com?subject=Tutu Disfraz - Analytics Help&body=Por favor, describe tu problema o pregunta aquí. Adjunta capturas de pantalla si es necesario.',
        'Report a bug': "https://www.github.com/svsm03/tutu-disfraz-analytics/issues/new",
    }
)




page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-color: white;
color: black;
}}

[data-testid="stSidebar"] > div:first-child {{
background-color: #AABD7B;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
color: black;
}}


[data-testid="stToolbar"] {{
right: 2rem;
color: black;
}}

[data-testid="baseButton-secondary"] {{
background-color: #AABD7B;
color: white;
}}


[data-testid="stFileUploadDropzone"] {{
background-color: #858F6C;

}}

[data-testid="stNotificationContentSuccess"] {{
color: black;
}}

[data-testid="stNotificationContentError"] {{
color: black;
}}

[data-testid="stNotificationContentWarning"] {{
color: black;
}}

[data-testid="baseButton-headerNoPadding"] {{
background-color: #AABD7B;
color: white;
}}


</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Step 1: Cargar la configuración desde el archivo YAML
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Step 2: Crear el objeto autenticador
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login('main',2)

# Configuración del logo 
logo_path = 'images/logo_complete.png'
logo_height = 80  # Ajusta la altura según tus necesidades


# Establecer el logo en la barra de navegación
st.sidebar.image(logo_path)

if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'HOLA! *{st.session_state["name"]}* {"👋🏻"}')
    st.markdown('💹Bienvenido/a a la aplicación de Tutu Disfraz - Analytics!')
    

    # Step 3: Crear el menú de navegación
    menu = {
        "Inicio": home,
        "Subir archivos": upload,
        "Visualizacion de datos": dashboard,
    }

    # Step 4: Crear el menú de navegación
    st.sidebar.title('Navegación')
    selection = st.sidebar.radio("Ir a...", list(menu.keys()))
    

    # Step 5: Mostrar la aplicación seleccionada
    app = menu[selection]
    app.app()

             

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')