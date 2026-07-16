from flask import Flask, jsonify
import serial
import threading
import numpy as np
import csv
from datetime import datetime

app = Flask(__name__)

# 🔌 CAMBIA COM SI ES NECESARIO
esp = serial.Serial('COM3', 115200)

# 📊 datos
ventana = []
valor_actual = 0

# 🧠 calibración
calibrando = True
muestras_calibracion = []
media_base = 0
std_base = 0

# 💾 CSV
def guardar_csv(x, y, z, mag):
    with open("datos_vibracion.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), x, y, z, mag])

# 🔄 reset calibración
def reiniciar_calibracion():
    global calibrando, muestras_calibracion, media_base, std_base

    calibrando = True
    muestras_calibracion = []
    media_base = 0
    std_base = 0

# 📡 lectura ESP32
def loop_esp():
    global valor_actual, calibrando, media_base, std_base

    while True:
        try:
            linea = esp.readline().decode().strip()

            partes = linea.replace("Aceleración X:", "") \
                           .replace("Y:", "") \
                           .replace("Z:", "") \
                           .split()

            x = float(partes[0])
            y = float(partes[1])
            z = float(partes[2])

            mag = np.sqrt(x**2 + y**2 + z**2)
            valor_actual = mag

            # 🧠 CALIBRACIÓN
            if calibrando:
                muestras_calibracion.append(mag)

                if len(muestras_calibracion) > 100:
                    media_base = np.mean(muestras_calibracion)
                    std_base = np.std(muestras_calibracion)
                    calibrando = False

            # 📊 NORMAL
            else:
                ventana.append(mag)
                if len(ventana) > 50:
                    ventana.pop(0)

            guardar_csv(x, y, z, mag)

        except:
            pass

@app.route("/data")
def data():
    global ventana, calibrando

    if calibrando:
        estado = "CALIBRANDO"
    else:
        if len(ventana) > 10:
            variacion = abs(valor_actual - media_base)

            if variacion < std_base * 1.5:
                estado = "NORMAL"
            elif variacion < std_base * 3:
                estado = "ADVERTENCIA"
            else:
                estado = "FALLA"
        else:
            estado = "NORMAL"

    return jsonify({
        "estado": estado,
        "valor": valor_actual,
        "serie": ventana,
        "calibrando": calibrando
    })

@app.route("/reset")
def reset():
    reiniciar_calibracion()
    return jsonify({"status": "ok"})

threading.Thread(target=loop_esp, daemon=True).start()

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Vibración ESP32</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>

<body style="margin:0;font-family:Arial;background:#0f172a;color:white;text-align:center;">

<h1>📡 Sistema de Vibración Industrial</h1>

<button onclick="recalibrar()"
style="padding:10px 20px;margin:10px;background:#1f2937;color:white;border:1px solid white;border-radius:8px;">
🔄 Recalibrar sistema
</button>

<h2 id="estado">Cargando...</h2>

<div id="led" style="width:90px;height:90px;border-radius:50%;margin:auto;background:gray;box-shadow:0 0 20px gray;"></div>

<h3 id="valor"></h3>

<canvas id="grafica" width="900" height="350"></canvas>

<script>
let ctx = document.getElementById("grafica").getContext("2d");

let chart = new Chart(ctx, {
    type: "line",
    data: {
        labels: [],
        datasets: [{
            label: "Vibración",
            data: [],
            borderColor: "cyan",
            pointRadius: 0,
            tension: 0.2
        }]
    }
});

function recalibrar(){
    fetch("/reset")
    .then(r => r.json())
    .then(() => {
        alert("Recalibrando sistema...");
    });
}

function actualizar(){
    fetch("/data")
    .then(r => r.json())
    .then(d => {

        if(d.calibrando){
            document.getElementById("estado").innerText = "CALIBRANDO...";
            document.getElementById("led").style.background = "gray";
            return;
        }

        document.getElementById("estado").innerText = d.estado;
        document.getElementById("valor").innerText = "Valor: " + d.valor.toFixed(2);

        let color = "gray";
        if(d.estado == "NORMAL") color = "green";
        if(d.estado == "ADVERTENCIA") color = "orange";
        if(d.estado == "FALLA") color = "red";

        document.getElementById("led").style.background = color;
        document.getElementById("led").style.boxShadow = "0 0 25px " + color;

        chart.data.labels = d.serie.map((_,i)=>i);
        chart.data.datasets[0].data = d.serie;
        chart.update();

    });
}

setInterval(actualizar, 500);
</script>

</body>
</html>
"""

app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
