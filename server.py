from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://ventrex95.github.io/precios_dinamicos"

@app.route("/precio", methods=["GET"])
def obtener_precio():
    # Obtener parámetros de la consulta
    entrada = request.args.get("entrada")  # Fecha y hora de entrada
    salida = request.args.get("salida")    # Fecha y hora de salida
    parking = request.args.get("parking")
    
    if not entrada or not salida or not parking:
        return jsonify({"error": "Faltan parámetros requeridos (entrada, salida, parking)"}), 400
    
    # Construir la URL dinámica del JSON
    json_url = f"{BASE_URL}/{entrada}/{salida}.json"
    
    # Obtener los datos desde la URL generada
    response = requests.get(json_url)
    if response.status_code != 200:
        return jsonify({"error": "No se pudo obtener la información desde la URL dinámica"}), 500
    
    precios = response.json()
    
    # Buscar el precio según el parking
    for item in precios:
        if item["parking"] == parking:
            return jsonify(item)  # Devolver toda la información del JSON si hay coincidencia
    
    return jsonify({"error": "No se encontró un precio para esos parámetros"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
