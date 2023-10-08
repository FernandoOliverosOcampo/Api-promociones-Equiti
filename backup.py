from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import psycopg2
import requests

# URL base de Supabase
url = "https://mmphzayxvvhdtrtcvjsq.supabase.co"

# Nombre de la tabla que deseas buscar
table_name = "usuario"

# Credenciales de autenticación de Supabase
apikey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1tcGh6YXl4dnZoZHRydGN2anNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODI2MDY3NDYsImV4cCI6MTk5ODE4Mjc0Nn0.QZWfmiw-KMFgHOTSyxNGFlcOZvDRa305OkZH-YHTzDI"
headers = {
    "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1tcGh6YXl4dnZoZHRydGN2anNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODI2MDY3NDYsImV4cCI6MTk5ODE4Mjc0Nn0.QZWfmiw-KMFgHOTSyxNGFlcOZvDRa305OkZH-YHTzDI",
    "Content-Type": "application/json",
}

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret' # Clave secreta para firmar los JWT
jwt = JWTManager(app)

def get_db_connection():
    conn = psycopg2.connect(host='db.mmphzayxvvhdtrtcvjsq.supabase.co',
                            database='postgres',
                            port=5432,
                            user='postgres',
                            password='yAdz7SdwJuvhsJaT')
    return conn

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Criterios de búsqueda
    query = {
        "usuario": username,
        "contrasena": password,
    }

    # Realizar la solicitud HTTP a la API de Supabase
    response = requests.get(f"{url}/rest/v1/{table_name}", headers=headers, params=query)

    # Manejar la respuesta
    if response.status_code == 200:
        # La solicitud fue exitosa, el registro se encuentra en response.json()
        print(response.json())
        return (jsonify({"funciono": "sixd"}))
    else:
                # La solicitud falló, manejar el error
        print(f"Error: {response.status_code} - {response.reason}")
        # Aquí iría la lógica para verificar si el usuario y contraseña son válidos
    #if username == "jeanxd" and password == "3008":
        # Si las credenciales son correctas, se genera un JWT y se devuelve como respuesta
     #   access_token = create_access_token(identity=username)
      #  print(access_token)
      #  return jsonify(access_token=access_token)
    #if not username or not password:
     #   return jsonify({"msg": "Por favor, ingrese su usuario y contraseña"}), 401


@app.route('/protegido', methods=['GET'])
@jwt_required()
def protegido():
    # Si se llega a esta ruta, significa que el JWT es válido y se puede acceder a la información protegida
    return jsonify({"msg": "Información protegida"})

def pagina_no_encontrada(error):
    
    return "<h1>La pagina a la que intentas acceder no existe...</h1>"



if __name__=="__main__":
    app.register_error_handler(404 , pagina_no_encontrada)
    ##app.run(debug=True, host="0.0.0.0")
    app.run(port=5000, debug=True)