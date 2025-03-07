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

    print(f"Parámetros recibidos: parking={parking}, fecha={fecha}, tiempo={tiempo}")

    total_precio = 0.0  # Asegurar que el precio es un número desde el inicio

    # Manejo de tiempos combinados (ej: "2 hours 3 days")
    horas = 0
    dias = 0
    partes = tiempo.split(" ")

    try:
        for i in range(0, len(partes), 2):  # Leer de dos en dos (número + unidad)
            valor = int(partes[i])
            unidad = partes[i + 1]
            if "hour" in unidad:
                horas = valor
            elif "day" in unidad:
                dias = valor
    except Exception as e:
        return jsonify({"error": f"Formato de tiempo inválido: {str(e)}"}), 400

    print(f"Valores extraídos: Horas={horas}, Días={dias}")

    # Buscar precios específicos de horas y días en el JSON
    precio_horas = None
    precio_dias = None

    for item in precios:
        if item["parking"] == parking and item["fecha"] == fecha:
            if item["tiempo"] == f"{horas} hours":
                precio_horas = float(item["price"])
                print(f"Precio encontrado para {horas} horas: {precio_horas}")

            if item["tiempo"] == f"{dias} days":
                precio_dias = float(item["price"])
                print(f"Precio encontrado para {dias} días: {precio_dias}")

    # Sumar solo si ambos precios fueron encontrados
    if precio_horas is not None and precio_dias is not None:
        total_precio = precio_horas + precio_dias
        print(f"Precio total calculado: {total_precio}")
        return jsonify({"price": round(total_precio, 2)})

    return jsonify({"error": "No se encontró un precio para esos parámetros"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
