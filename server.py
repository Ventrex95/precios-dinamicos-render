from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URL del JSON en GitHub Pages
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

    total_precio = 0.0  # Asegurar que el precio es flotante desde el inicio

    for item in precios:
        if item["parking"] == parking and item["fecha"] == fecha:
            # Si el tiempo tiene horas y días
            if "hour" in tiempo and "day" in tiempo:
                try:
                    partes = tiempo.split(" ")
                    horas = int(partes[0]) if "hour" in partes[1] else 0
                    dias = int(partes[2]) if "day" in partes[3] else 0
                    
                    for i in precios:
                        if i["parking"] == parking and i["fecha"] == fecha:
                            if i["tiempo"] == f"{horas} hours":
                                total_precio += float(i["price"])
                            if i["tiempo"] == f"{dias} days":
                                total_precio += float(i["price"])
                    
                    print(f"Precio total calculado: {total_precio}")  # Debug
                    return jsonify({"price": total_precio})

                except Exception as e:
                    return jsonify({"error": f"Error en la conversión de tiempo: {str(e)}"}), 400
            
            # Si el tiempo es exacto
            if item["tiempo"] == tiempo:
                return jsonify({"price": float(item["price"])})
    
    return jsonify({"error": "No se encontró un precio para esos parámetros"}), 404
