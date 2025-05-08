from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import json


# gRPC imports
import grpc
from concurrent import futures
import metrics_pb2
import metrics_pb2_grpc
import threading


import sys
sys.stdout.reconfigure(line_buffering=True)


# --- Publicar en el MQTT ---
import paho.mqtt.client as mqtt

mqtt_client = mqtt.Client()
mqtt_client.connect("mosquitto", 1883)  # El nombre del contenedor en docker-compose


# --- FLASK + WEBSOCKETS ---
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")


@app.route("/sensors/metrics", methods=["POST"])
def recibir_metrica_http():
    data = request.json
    print(f"[HTTP] Métrica recibida: {json.dumps(data, indent=2)}", flush=True)
    mqtt_client.publish("sensors/heartrate", json.dumps(data))
    return jsonify({"status": "ok"}), 200


@socketio.on("message", namespace="/sensors/metrics")
def recibir_metrica_ws(data):
    print(f"[WS] Métrica recibida: {json.dumps(data, indent=2)}", flush=True)
    mqtt_client.publish("sensors/heartrate", json.dumps(data))



# --- gRPC SERVER ---

class MetricsService(metrics_pb2_grpc.MetricsServiceServicer):
    def EnviarMetrica(self, request, context):
        data = {
            "sensor_id": request.sensor_id,
            "persona_id": request.persona_id,
            "nombre": request.nombre,
            "unidad": request.unidad,
            "valor": request.valor,
            "timestamp": request.timestamp,
        }
        print(f"[gRPC] Métrica recibida:\n{json.dumps(data, indent=2)}", flush=True)
        mqtt_client.publish("sensors/heartrate", json.dumps(data))
        return metrics_pb2.MetricaResponse(status="ok")


def iniciar_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    metrics_pb2_grpc.add_MetricsServiceServicer_to_server(MetricsService(), server)
    server.add_insecure_port('[::]:3000')
    print("🟢 Servidor gRPC escuchando en puerto 3000", flush=True)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    # Iniciar gRPC en un hilo aparte
    grpc_thread = threading.Thread(target=iniciar_grpc, daemon=True)
    grpc_thread.start()

    print("🟢 Servidor HTTP/WS escuchando en http://localhost:5000", flush=True)
    app.run(host="0.0.0.0", port=5000)