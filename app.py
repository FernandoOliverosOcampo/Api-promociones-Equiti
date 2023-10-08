from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS, cross_origin
import supabase


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret' # Clave secreta para firmar los JWT
CORS(app)
jwt = JWTManager(app)

SUPABASE_URL = 'https://xjztrplrkyssesmkzaae.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhqenRycGxya3lzc2VzbWt6YWFlIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTU0ODQzNDEsImV4cCI6MjAxMTA2MDM0MX0.Is_I0GcJEBh799c4Psb_JbFjmyed61zfG8Ls-M5R51I'

@app.route('/formulario', methods=['POST'])
def login():
    username = request.json.get('correo')
    password = request.json.get('contraseña')

    # Conectamos con Supabase
    client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

    # Buscamos el usuario en la tabla 'users'
    query = client.table('formulario').select('*').eq('correo', username).eq('contraseña', password)
    res = query.execute()

    # Si el usuario existe y la contraseña es correcta, se devuelve un token JWT
    if len(res.data) == 1:
        access_token = create_access_token(identity=username)
        print(access_token)
        return jsonify(access_token=access_token), 200

    # Si no se encontró el usuario o la contraseña es incorrecta, se devuelve un error 401
    return jsonify({"msg": "Credenciales inválidas"}), 401

@app.route('/protegido', methods=['GET'])
@jwt_required()
def protegido():
    # Si se llega a esta ruta, significa que el JWT es válido y se puede acceder a la información protegida
    return jsonify({"msg": "Información protegida"})


if __name__=="__main__":
    ##app.run(debug=True, host="0.0.0.0")
    app.run(port=5000, debug=True)