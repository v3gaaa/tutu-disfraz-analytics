import streamlit as st
import pandas as pd
from io import BytesIO
import os
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2 import service_account

creds = Credentials.from_service_account_file('sheets_credentials.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])

SPREADSHEET_ID = '1nsohqKheE8i2BJ3IdohrJ09GTVIU9u5Ufbgj1pPWyWE'

service = build('sheets', 'v4', credentials=creds)


def create_toggle_menu_talla(column,df,sheet_id):

    # Buscar automáticamente la columna de "Pantalones" en el DataFrame
    column_index = df.columns.get_loc(column) + 1
    

    # Configurar las reglas de validación para el menú desplegable
    data_validation_rule = {
        "condition": {
            "type": "ONE_OF_LIST",
            "values": [
                {"userEnteredValue": "NA"},
                {"userEnteredValue": "C"},
                {"userEnteredValue": "M"},
                {"userEnteredValue": "G"},
            ],
        },
        "inputMessage": "Selecciona un valor de la lista desplegable",
        "showCustomUi": True,
    }

    # Aplicar la regla de validación a la columna
    request = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body={
        'requests': [{
            'setDataValidation': {
                'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': df.shape[0]+1, 'startColumnIndex': column_index-1, 'endColumnIndex': column_index},
                'rule': data_validation_rule
            }
        }]
    })
    response = request.execute()

def create_toggle_menu_estado_produccion(column, df, sheet_id):

    # Buscar automáticamente la columna de "Estado de Producción" en el DataFrame
    column_index = df.columns.get_loc(column) + 1

    # Configurar las reglas de validación para el menú desplegable
    data_validation_rule = {
        "condition": {
            "type": "ONE_OF_LIST",
            "values": [
                {"userEnteredValue": "No empezado"},
                {"userEnteredValue": "En proceso"},
                {"userEnteredValue": "Terminado"},
            ],
        },
        "inputMessage": "Selecciona un valor de la lista desplegable",
        "showCustomUi": True,
    }

    # Aplicar la regla de validación a la columna
    request = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body={
        'requests': [{
            'setDataValidation': {
                'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': df.shape[0]+1, 'startColumnIndex': column_index-1, 'endColumnIndex': column_index},
                'rule': data_validation_rule
            }
        }]
    })
    response = request.execute()



def create_toggle_menu_genero(column,df,sheet_id):

    # Buscar automáticamente la columna de "Pantalones" en el DataFrame
    column_index = df.columns.get_loc(column) + 1
    

    # Configurar las reglas de validación para el menú desplegable
    data_validation_rule = {
        "condition": {
            "type": "ONE_OF_LIST",
            "values": [
                {"userEnteredValue": "M"},
                {"userEnteredValue": "F"},
                {"userEnteredValue": "NA"}
            ],
        },
        "inputMessage": "Selecciona un valor de la lista desplegable",
        "showCustomUi": True,
    }

    # Aplicar la regla de validación a la columna
    request = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body={
        'requests': [{
            'setDataValidation': {
                'range': {'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': df.shape[0]+1, 'startColumnIndex': column_index-1, 'endColumnIndex': column_index},
                'rule': data_validation_rule
            }
        }]
    })
    response = request.execute()


def write_to_google_sheets(df, sheet_name):
    try:
        # Convertir DataFrame a formato de lista para escribir en Sheets
        values = [df.columns.tolist()] + df.values.tolist()

        body = {
            'values': values
        }

        # Crear una nueva hoja para el evento
        request = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body={
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': sheet_name,
                    }
                }
            }]
        })
        response = request.execute()

        # Escribir los datos en la nueva hoja
        write_range = f'{sheet_name}!A1'
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=write_range,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()

        # Crear menús desplegables en la nueva hoja
        create_toggle_menu_talla("Pantalones", df, response['replies'][0]['addSheet']['properties']['sheetId'])
        create_toggle_menu_talla("Camisa", df, response['replies'][0]['addSheet']['properties']['sheetId'])
        create_toggle_menu_talla("Vestido", df, response['replies'][0]['addSheet']['properties']['sheetId'])
        create_toggle_menu_genero("Genero", df, response['replies'][0]['addSheet']['properties']['sheetId'])
        create_toggle_menu_estado_produccion("Estado de Producción", df, response['replies'][0]['addSheet']['properties']['sheetId'])
        st.success(f"¡Los datos han sido enviados exitosamente a una nueva hoja de Google Sheets llamada '{sheet_name}'!")

    except HttpError as e:
        error_message = e.content.decode("utf-8")
        if "A sheet with the name" in error_message:
            st.error(f"Ya existe una hoja con el nombre '{sheet_name}'. Por favor, elige otro nombre para el evento.")
        else:
            st.error("Error al escribir en Google Sheets. Por favor, inténtalo de nuevo más tarde.")



def create_sheets_by_group(df):

    # Obtener la lista de grupos únicos en el DataFrame
    groups = df['Grupo'].unique()

    # Iterar sobre cada grupo y crear una hoja para cada uno
    for group in groups:
        group_df = df[df['Grupo'] == group]
        group_df = group_df.drop(columns=['Grupo'])
        values = [group_df.columns.tolist()] + group_df.values.tolist()

        body = {
            'values': values
        }

        # Crear una nueva hoja para el grupo
        request = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body={
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': group,
                    }
                }
            }]
        })
        response = request.execute()

        # Escribir los datos en la nueva hoja
        write_range = f'{group}!A1'
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=write_range,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()



def app():
    st.header('Sube tus archivos', divider='grey')
    st.write('Aquí debes subir todos tus grupos de alumnos en formato .xlsx (Excel).')
    st.write('Después de un pequeño procesamiento, se generará una base de datos con todos los alumnos de todos los grupos. Y se subirá a Google Sheets.')

    st.warning('RECUERDA: Tú aún debes rellenar los datos manualmente. Aquí solo subirás las listas de alumnos 1 sola vez. Después tú deberás rellenar los datos manualmente en Google Sheets.')

    # Ingresar el nombre del evento
    event_name = st.text_input("Ingresa el nombre del evento:")
    
    # Subir archivos de Excel
    files = st.file_uploader("Subir archivo EXCEL", type=['xlsx'], accept_multiple_files=True)
    
    if files and event_name:
        # Lista para almacenar los DataFrames de cada archivo
        dfs = []

        # Leer cada archivo y almacenar su DataFrame en la lista
        for file in files:
            df = pd.read_excel(file)
            df = df.drop(df.index[:8])
            dfs.append(df)

            # Agregar la columna 'Grupo' con el nombre del archivo
            file_name_without_extension, _ = os.path.splitext(file.name)
            df['Grupo'] = file_name_without_extension

        # Combinar todos los DataFrames en uno solo
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df = combined_df.iloc[:, [0, 1, -1]]
        combined_df.columns = ['Numero de lista', 'Nombre', 'Grupo']

        # Agregar columnas adicionales al final y rellenarlas con NaN
        new_columns = ['Genero', 'Temática', 'Personaje', 'Pantalones', 'Color Pantalón', 'Camisa', 'Color Camisa', 'Vestido', 'Color Vestido']
        combined_df['Estado de Producción'] = 'No empezado'
        combined_df = pd.concat([combined_df, pd.DataFrame(columns=new_columns)], axis=1)
        combined_df.fillna('NA', inplace=True)

        # Mostrar el DataFrame combinado con la nueva columna 'Grupo'
        st.write("Base de datos:")
        st.write(combined_df)

        # Pregunta al usuario si desea enviar los datos a Google Sheets
        if st.button("Enviar a Google Sheets"):
            # Escribe el DataFrame a Google Sheets con el nombre del evento como hoja
            write_to_google_sheets(combined_df, event_name)
            #create_sheets_by_group(combined_df)
