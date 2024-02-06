import streamlit as st

def app():

    st.header('Tutorial', divider='grey')
    st.subheader('Preparate', divider='grey')

    st.write('1. Asegúrate de tener una cuenta de Google y que esté activa.')
    st.write('Esto por que ahi es donde se subirán los datos de los alumnos y donde los administadores podrán editarlos.')
    st.write('2. Asegúrate de tener tu cuenta y contraseña de este software a la mano ya que no se puede recuperar ni crear una nueva cuenta.')
    st.write('3. Asegúrate de tener tus listas de alumnos en formato .xlsx (Excel) listas.')
    st.write('Tienen que tener como nombre el nombre del grupo que representan.')
    st.image('images/Excel.png')

    st.subheader('Subir tus archivos', divider='grey')
    st.write('1. Ingresa el nombre del evento que estas llevando a cabo.')
    st.write('Este nombre sera el nombre de la hoja de calculo en Google Sheets.')
    st.image('images/NombreEvento.png')
    st.write('2. Sube tus archivos de Excel.')
    st.write('Puedes subir todos los archivos a la vez.')
    st.image('images/SubirArch.png')
    st.write('Despues de subirlos se uniran en una sola base de datos la cual puedes revisar antes de subirla a Google Sheets.')
    st.write('3. Envia tus archivos.')
    st.write('Despues de revisar que todo este correcto puedes enviar tus archivos a Google Sheets.')
    st.image('images/Enviar.png')
    st.write('Si el evento ya existe, la pagina te dira y te pedira que cambies el nombre del evento.')
    st.image('images/ErrorYaExiste.png')
    st.write('Si todo esta correcto, la pagina te dira que se subieron los datos correctamente.')
    st.image('images/EnviadosCorrect.png')

    st.subheader('Rellenar Datos', divider='grey')
    st.write('1. Ingresa a Google Sheets.')
    st.write('Una vez que tus datos esten subidos, puedes ingresar a Google Sheets para rellenar los datos de los alumnos MANUALMENTE, segun los vayas obteniendo.')
    st.write('La liga para ingresar a Google Sheets es la siguiente:')
    st.write('https://docs.google.com/spreadsheets/d/1nsohqKheE8i2BJ3IdohrJ09GTVIU9u5Ufbgj1pPWyWE/edit?usp=sharing')
    st.write('Todos pueden entrar a ver los datos, pero solo los administradores pueden editarlos.')
    st.write('2. Dentro de Google Sheets, busca la hoja de calculo con el nombre del evento que ingresaste.')
    st.image('images/Sheets.png')
    st.write('3. Rellena los datos de los alumnos.')
    st.image('images/SheetsListo.png')
    st.write('Una vez todos los datos esten rellenados ya puedes visualizarlos.')

    st.subheader('Visualizar Datos', divider='grey')
    st.write('1. Ingresa a la pagina de visualizacion de datos.')
    st.image('images/Visualizacion.png')
    st.write('2. Selecciona el evento que quieres visualizar.')
    st.image('images/IngresarEvent.png')
    st.write('Una vez seleccionado el evento, se mostraran los datos en el siguiente Dashboard.')
    st.image('images/Dashboard.png')


    st.subheader('Dashboard', divider='grey')
    st.write('1. En la parte superior puedes encontrar unas metricas de los disfraces terminados/en proceso/faltantes.')
    st.image('images/Metricas.png')
    st.write('2. En la parte izquierda dentro de la barra lateral, puedes seleccionar filtros para visualizar los datos.')
    st.image('images/Filtros.png')
    st.write('3. Una vez aplicados los filtros, se alteraran la tabla y las graficas para mostrar los datos que seleccionaste.')
    st.image('images/FiltroAplicado.png')
    st.warning('Recuerda que los datos no se actualizan en tiempo real si haces un cambio en el sheets mientras estas en la pagina de visualizacion, tienes que recargar la pagina para ver los cambios o presionar el boton de actualizar.')
    st.image('images/Actualizar.png')
    st.write('4. Finalmente, puedes descargar los datos filtrados en forma de etiquetas para los disfraces en formato .pdf.')
    st.image('images/Etiquetas.png')

    

