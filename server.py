from flask import Flask, request, jsonify
import requests
from threading import Timer

app = Flask(__name__)

# URL del JSON en GitHub
JSON_URL = "https://ventrex95.github.io/precios_dinamicos/precios.json"

# Cargar precios en memoria
def cargar_precios():
    response = requests.get(JSON_URL)
    if response.status_code == 200:
        print("✅ JSON cargado correctamente.")
        return response.json()
    print("⚠️ Error al cargar el JSON.")
    return []

PRECIOS = cargar_precios()  # Se carga al iniciar el servidor

# Actualizar precios cada 10 minutos
def actualizar_precios():
    global PRECIOS
    PRECIOS = cargar_precios()
    Timer(600, actualizar_precios).start()  # Se actualiza cada 600 segundos (10 min)

actualizar_precios()  # Iniciar actualización automática

@app.route("/precio", methods=["GET"])
def obtener_precio():
    parking = request.args.get("parking")
    fecha = request.args.get("fecha")
    tiempo = request.args.get("tiempo")

    print(f"🔎 Buscando precio para: parking={parking}, fecha={fecha}, tiempo={tiempo}")

    total_precio = 0.0
    horas = 0
    dias = 0
    partes = tiempo.split(" ")

    try:
        for i in range(0, len(partes), 2):
            valor = int(partes[i])
            unidad = partes[i + 1]
            if "hour" in unidad:
                horas = valor
            elif "day" in unidad:
                dias = valor
    except Exception as e:
        return jsonify({"error": f"Formato de tiempo inválido: {str(e)}"}), 400

    print(f"⏳ Extraído: {horas} horas, {dias} días")

    precio_horas = None
    precio_dias = None

    for item in PRECIOS:  # Usamos la lista en memoria en vez de hacer una petición
        if item["parking"] == parking and item["fecha"] == fecha:
            if item["tiempo"] == f"{horas} hours":
                precio_horas = float(item["price"])
                print(f"✅ Precio encontrado para {horas} horas: {precio_horas}")
            if item["tiempo"] == f"{dias} days":
                precio_dias = float(item["price"])
                print(f"✅ Precio encontrado para {dias} días: {precio_dias}")

    if precio_horas is not None and precio_dias is not None:
        total_precio = precio_horas + precio_dias
        print(f"💰 Precio total calculado: {total_precio}")
        return jsonify({"price": round(total_precio, 2)})

    return jsonify({"error": "No se encontró un precio para esos parámetros"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
