from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

JSON_URL_PRECIOS = "https://ventrex95.github.io/precios_dinamicos/precios.json"
JSON_URL_HORAS = "https://ventrex95.github.io/precios_dinamicos/horas.json"

@app.route("/precio", methods=["GET"])
def obtener_precio():
    response_precios = requests.get(JSON_URL_PRECIOS)
    response_horas = requests.get(JSON_URL_HORAS)
    
    if response_precios.status_code != 200 or response_horas.status_code != 200:
        return jsonify({"error": "No se pudo obtener la información"}), 500

    precios = response_precios.json()
    horas = response_horas.json()

    parking = request.args.get("parking")
    fecha = request.args.get("fecha")
    tiempo = request.args.get("tiempo")

    print(f"Parametros recibidos: parking={parking}, fecha={fecha}, tiempo={tiempo}")
    print(f"Datos de precios: {precios}")
    print(f"Datos de horas: {horas}")

    for item in precios:
        for hora in horas:
            print(f"Comparando: item['parking']={item['parking']}, item['fecha']={item['fecha']}, hora['tiempo']={hora['tiempo']}")
            if item["parking"] == parking and item["fecha"] == fecha and hora["tiempo"] == tiempo:
                arrival = f"{item['fecha']} {hora['hora']}"
                return jsonify({
                    "priceId": item["priceId"],
                    "parking": item["parking"],
                    "fecha": item["fecha"],
                    "tiempo": item["tiempo"],
                    "price": item["price"],
                    "product": item["product"],
                    "availablePlaces": item["availablePlaces"],
                    "arrival": arrival
                })

    return jsonify({"error": "No se encontró un precio para esos parámetros"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
