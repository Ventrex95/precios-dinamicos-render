from flask import Flask, request, jsonify
import requests
import pandas as pd

app = Flask(__name__)

JSON_URL_PRECIOS = "https://ventrex95.github.io/precios_dinamicos/precios.json"
JSON_URL_HORAS = "https://ventrex95.github.io/precios_dinamicos/horas.json"

@app.route("/merged_data", methods=["GET"])
def obtener_datos_combinados():
    response_precios = requests.get(JSON_URL_PRECIOS)
    response_horas = requests.get(JSON_URL_HORAS)
    
    if response_precios.status_code != 200 or response_horas.status_code != 200:
        return jsonify({"error": "No se pudo obtener la información"}), 500
    
    # Convertir las respuestas JSON en DataFrames de pandas
    df_precios = pd.DataFrame(response_precios.json())
    df_horas = pd.DataFrame(response_horas.json())
    
    # Agregar una clave temporal a ambos DataFrames
    df_precios["key"] = 1
    df_horas["key"] = 1
    
    # Realizar el merge
    df_combined = pd.merge(df_horas, df_precios, on="key").drop("key", axis=1)
    
    # Convertir el resultado de vuelta a JSON
    combined_json = df_combined.to_dict(orient="records")
    
    return jsonify(combined_json)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
