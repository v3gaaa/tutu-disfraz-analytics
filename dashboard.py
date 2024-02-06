import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import plotly.express as px
import plotly.io as pio
from PIL import Image, ImageDraw, ImageFont
import io
import base64


font_path = "fonts/DejaVuSans.ttf"

# Función para obtener datos desde Google Sheets
def get_data_from_sheets(spreadsheet_id, range_name):

    try:
        creds = service_account.Credentials.from_service_account_file('etc/secrets/credentials.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
        service = build('sheets', 'v4', credentials=creds)
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])

        if not values:
            return pd.DataFrame()
        else:
            df = pd.DataFrame(values[1:], columns=values[0])
            return df
    except Exception as e:
        print('Error:', e)
        return None
    
# Función para crear la imagen con etiquetas
def create_images_with_labels(df):
    # Tamaño de la imagen y cantidad máxima de etiquetas por imagen
    image_width = 800
    image_height = 600
    max_labels_per_image = 12

    # Fuente para las etiquetas
    font = ImageFont.truetype(font_path, size=12)

    # Contador para realizar un seguimiento del número de imágenes creadas
    image_count = 1

    # Crear una nueva imagen
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    # Coordenadas iniciales y tamaño de las etiquetas
    x = 50
    y = 50
    label_width = 300  # Ancho más corto
    label_height = 80  # Altura más alta

    # Espaciado entre las etiquetas
    y_spacing = 10

    # Contador para realizar un seguimiento del número de etiquetas en la imagen actual
    labels_count = 0

    # Lista para almacenar las imágenes en formato de bytes
    images_byte_array = []

    # Iterar sobre las filas del DataFrame y agregar etiquetas a la imagen
    for _, row in df.iterrows():
        label = f"{row['Nombre']}\nGrupo: {row['Grupo']}\nNumero de Lista: {row['Numero de lista']}\nDisfraz: {row['Personaje']}"

        # Dibujar un rectángulo con borde negro
        draw.rectangle([x, y, x + label_width, y + label_height], outline="black")

        # Dibujar la etiqueta dentro del rectángulo
        draw.text((x + 5, y + 5), label, font=font, fill="black")

        # Actualizar las coordenadas y el contador para la siguiente etiqueta
        y += label_height + y_spacing
        labels_count += 1

        # Si llegamos al final de la imagen, ajustar las coordenadas
        if y + label_height + y_spacing > image_height:
            y = 50
            x += label_width + 50

        # Si se alcanza el número máximo de etiquetas por imagen, guardar la imagen actual y reiniciar
        if labels_count >= max_labels_per_image:
            # Guardar la imagen
            image_byte_array = io.BytesIO()
            image.save(image_byte_array, format='PNG')
            images_byte_array.append(image_byte_array.getvalue())
            image_count += 1

            # Crear una nueva imagen
            image = Image.new("RGB", (image_width, image_height), "white")
            draw = ImageDraw.Draw(image)

            # Reiniciar las coordenadas y el contador
            x = 50
            y = 50
            labels_count = 0

    # Guardar la última imagen si hay etiquetas restantes
    if labels_count > 0:
        # Convertir la imagen en bytes
        image_byte_array = io.BytesIO()
        image.save(image_byte_array, format='PNG')
        images_byte_array.append(image_byte_array.getvalue())

    # Crear el enlace de descarga para el archivo PDF
    st.markdown(get_pdf_download_link(images_byte_array), unsafe_allow_html=True)

# Función para generar el enlace de descarga del archivo PDF
def get_pdf_download_link(images_byte_array):
    pdf_buffer = io.BytesIO()
    # Crear un archivo PDF a partir de las imágenes
    images = [Image.open(io.BytesIO(image_data)) for image_data in images_byte_array]
    images[0].save(pdf_buffer, save_all=True, append_images=images[1:], format='PDF')
    pdf_buffer.seek(0)
    b64_pdf = base64.b64encode(pdf_buffer.read()).decode()
    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="etiquetas.pdf">Descargar todas las etiquetas</a>'
    return href

def app():
    st.header('Visualización de datos', divider='grey')

    # Permitir al usuario seleccionar el evento
    event_name = st.text_input("Ingresa el nombre del evento:")
    if not event_name:
        st.warning("Por favor, ingresa el nombre del evento.")
        return

    # ID de la hoja de cálculo y rango
    spreadsheet_id = '1nsohqKheE8i2BJ3IdohrJ09GTVIU9u5Ufbgj1pPWyWE'
    range_name = f'{event_name}'  # Ajusta esto según la hoja y rango específicos

    # Obtener datos desde Google Sheets
    df = get_data_from_sheets(spreadsheet_id, range_name)
    if df is None:
        st.error('Error al obtener datos desde Google Sheets, no hay datos o no existe la hoja.')
        return
    
    #Boton para actualizar datos
    st.warning('Si haces cambios en el archivo de Google Sheets mientras esta aplicación está abierta, puedes actualizar los datos con el siguiente botón:')
    
    if st.button('Actualizar datos'):
        df = get_data_from_sheets(spreadsheet_id, range_name)

    # Mostrar los datos de estado de producción
    # Contar disfraces terminados, en proceso y que faltan
    total_disfraces = df.shape[0]
    disfraces_terminados = df[df['Estado de Producción'] == 'Terminado'].shape[0]
    disfraces_en_proceso = df[df['Estado de Producción'] == 'En proceso'].shape[0]
    disfraces_faltan = total_disfraces - disfraces_terminados

    # Mostrar los rectángulos
    col1, col2, col3 = st.columns(3)
    col1.metric("Disfraces Terminados", disfraces_terminados, delta=None)
    col2.metric("Disfraces en Proceso", disfraces_en_proceso, delta=None)
    col3.metric("Disfraces que Faltan", disfraces_faltan, delta=None)

    

    with st.sidebar:
        st.markdown("## Filtros")
        selected_state = st.multiselect("Estado de Producción", df['Estado de Producción'].unique())
        selected_group = st.multiselect("Grupo", df['Grupo'].unique())
        selected_gender = st.multiselect("Género", df['Genero'].unique())
        selected_pants_size = st.multiselect("Talla de Pantalón", df['Pantalones'].unique())
        selected_pants_color = st.multiselect("Color de Pantalón", df['Color Pantalón'].unique())
        selected_shirt_size = st.multiselect("Talla de Camisa", df['Camisa'].unique())
        selected_shirt_color = st.multiselect("Color de Camisa", df['Color Camisa'].unique())
        selected_dress_size = st.multiselect("Talla de Vestido", df['Vestido'].unique())
        selected_dress_color = st.multiselect("Color de Vestido", df['Color Vestido'].unique())
        selected_theme = st.multiselect("Temática", df['Temática'].unique())
        selected_character = st.multiselect("Personaje", df['Personaje'].unique())

    # Aplicar filtros
    filtered_df = df.copy()
    if selected_state:
        filtered_df = filtered_df[filtered_df['Estado de Producción'].isin(selected_state)]
    if selected_group:
        filtered_df = filtered_df[filtered_df['Grupo'].isin(selected_group)]
    if selected_gender:
        filtered_df = filtered_df[filtered_df['Genero'].isin(selected_gender)]
    if selected_pants_size:
        filtered_df = filtered_df[filtered_df['Pantalones'].isin(selected_pants_size)]
    if selected_pants_color:
        filtered_df = filtered_df[filtered_df['Color Pantalón'].isin(selected_pants_color)]
    if selected_shirt_size:
        filtered_df = filtered_df[filtered_df['Camisa'].isin(selected_shirt_size)]
    if selected_shirt_color:
        filtered_df = filtered_df[filtered_df['Color Camisa'].isin(selected_shirt_color)]
    if selected_dress_size:
        filtered_df = filtered_df[filtered_df['Vestido'].isin(selected_dress_size)]
    if selected_dress_color:
        filtered_df = filtered_df[filtered_df['Color Vestido'].isin(selected_dress_color)]
    if selected_theme:
        filtered_df = filtered_df[filtered_df['Temática'].isin(selected_theme)]
    if selected_character:
        filtered_df = filtered_df[filtered_df['Personaje'].isin(selected_character)]


    st.write(filtered_df)
    # Mostrar el número de niños después de aplicar los filtros
    st.subheader(f'Número de niños que aplican a estos filtros: {filtered_df.shape[0]}')
   

   # Botón para crear la imagen con etiquetas
    st.write('Si deseas crear un pdf con las etiquetas de los disfraces correspondientes a los filtros seleccionados, haz clic en el siguiente botón:')
    if st.button("Crear Etiquetas"):
        if filtered_df is not None:
            # Crear la imagen con etiquetas
            create_images_with_labels(filtered_df)
            st.success("Etiquetas creadas con éxito! Puedes descargar el archivo PDF usando el enlace de abajo.")

    st.subheader('Gráficos', divider='grey')

    col1, col2 = st.columns(2)

    # Gráfico de pastel por género
    pio.templates.default = "plotly_white"  
    fig_genre = px.pie(filtered_df[filtered_df['Genero'] != 'NA'], names='Genero', title='Por Género')
    fig_genre.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',  
        title_font=dict(color='black')  
    )
    fig_genre.update_traces(textposition='inside', textinfo='percent+label')  
    col1.plotly_chart(fig_genre, use_container_width=True)  # Ajustar al ancho del contenedor

    # Gráfico de pastel por color de pantalón
    fig_pants_color = px.pie(filtered_df[filtered_df['Color Pantalón'] != 'NA'], names='Color Pantalón', title='Por Color de Pantalón')
    fig_pants_color.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',  
        title_font=dict(color='black')  
    )
    fig_pants_color.update_traces(textposition='inside', textinfo='percent+label') 
    col2.plotly_chart(fig_pants_color, use_container_width=True)  # Ajustar al ancho del contenedor

    # Añadir espacio entre las filas
    st.markdown("<br>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    # Gráfico de pastel por color de camisa
    fig_shirt_color = px.pie(filtered_df[filtered_df['Color Camisa'] != 'NA'], names='Color Camisa', title='Por Color de Camisa')
    fig_shirt_color.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',  
        title_font=dict(color='black')  
    )
    fig_shirt_color.update_traces(textposition='inside', textinfo='percent+label') 
    col3.plotly_chart(fig_shirt_color, use_container_width=True)  # Ajustar al ancho del contenedor

    # Gráfico de pastel por color de vestido
    fig_dress_color = px.pie(filtered_df[filtered_df['Color Vestido'] != 'NA'], names='Color Vestido', title='Por Color de Vestido')
    fig_dress_color.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',  
        title_font=dict(color='black'), 
    )
    fig_dress_color.update_traces(textposition='inside', textinfo='percent+label')  
    col4.plotly_chart(fig_dress_color, use_container_width=True)  # Ajustar al ancho del contenedor


