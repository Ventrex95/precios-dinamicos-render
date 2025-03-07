from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

JSON_URL = "https://ventrex95.github.io/precios_dinamicos/precios.json"

@app.route("/precio", methods=["GET"])
def obtener_precio():
    response = requests.get(JSON_URL)
    if response.status_code != 200:
        return jsonify({"error": "No se pudo obtener la información"}), 500

    precios = response.json()

    parking = request.args.get("parking")
    fecha = request.args.get("fecha")
    tiempo = request.args.get("tiempo")

    for item in precios:
        if item["parking"] == parking and item["fecha"] == fecha and item["tiempo"] == tiempo:
            return jsonify({"price": item["price"]})

    return jsonify({"error": "No se encontró un precio para esos parámetros"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
