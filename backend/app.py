from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from openai import OpenAI  # Importamos la nueva clase

app = Flask(__name__)
CORS(app)

# Inicializa el cliente de OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Verifica si la clave de API está configurada al inicio
if not client.api_key:
    print("Error: La clave de API de OpenAI no está configurada como variable de entorno.")
    print("Por favor, asegúrate de seguir las instrucciones para configurar la variable OPENAI_API_KEY en tu terminal o sistema operativo.")

# Define la ruta para generar nombres
@app.route('/generar_nombres', methods=['POST'])
def generar():
    # Verifica nuevamente la clave de API dentro de la función (por seguridad)
    if not client.api_key:
        return jsonify({'error': 'La clave de API de OpenAI no está configurada en el servidor. Asegúrate de configurarla en la terminal o sistema operativo antes de ejecutar la aplicación.'}), 500

    # Obtiene los datos JSON de la petición
    data = request.get_json()
    # Extrae la descripción del proyecto
    descripcion = data.get('descripcion')

    # Procesa la descripción si se proporciona
    if descripcion:
        try:
            # Llama a la API de OpenAI para generar nombres usando la nueva interfaz
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # ¡Elige el modelo que prefieras!
                messages=[
                    {"role": "user", "content": f"Genera nombres creativos para un proyecto que se describe como: {descripcion}. Proporciona una lista de 5 nombres."}
                ],
                max_tokens=50,
                n=5,
                stop=None,
                temperature=0.7,
            )
            # Extrae los nombres generados de la respuesta (la estructura ha cambiado)
            nombres = [choice.message.content.strip() for choice in response.choices]
            # Retorna la lista de nombres como JSON con código de estado 200 (OK)
            return jsonify({'nombres': nombres})
        except Exception as e:
            # Maneja cualquier error al comunicarse con OpenAI y retorna un error 500
            return jsonify({'error': str(e)}), 500
    else:
        # Retorna un error 400 (Bad Request) si no se proporciona la descripción
        return jsonify({'error': 'Descripción no proporcionada'}), 400

# Inicia el servidor Flask solo si el script se ejecuta directamente
if __name__ == '__main__':
    app.run(debug=True)