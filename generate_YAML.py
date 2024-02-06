import yaml
import hashlib
import streamlit_authenticator as stauth

# Datos proporcionados
names = ["Sebastian Vega", "Berenice Saint"]
usernames = ["svsm03", "bsaint71"]
passwords = ["XXX", "XXX"]
passwords = stauth.Hasher(passwords).generate()

# Estructura del diccionario
data = {
    "credentials": {
        "usernames": {}
    },
    "cookie": {
        "expiry_days": 30,
        "key": "random_signature_key",
        "name": "random_cookie_name"
    },
    "preauthorized": {
        "emails": []
    }
}

# Agregar información de usuarios
for name, username, password in zip(names, usernames, passwords):
    data["credentials"]["usernames"][username] = {
        "email": f"{username}@gmail.com",
        "name": name,
        "password": password
    }

# Agregar correo preautorizado
data["preauthorized"]["emails"] = ["svega03@hotmail.com"]

# Generar archivo YAML
with open("config.yaml", "w") as yaml_file:
    yaml.dump(data, yaml_file, default_flow_style=False)

print("Archivo YAML generado con éxito.")
