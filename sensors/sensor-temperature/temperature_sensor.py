import socketio
import random
import datetime
import time

WS_URL = "http://gateway:5000"

sio = socketio.Client()

@sio.event
def connect():
    print("[✓] Conectado al servidor Socket.IO")

@sio.event
def disconnect():
    print("[✗] Desconectado del servidor")

class Metrica:
    def __init__(self, sensor_id, persona_id, nombre, unidad, valor):
        self.sensor_id = sensor_id
        self.persona_id = persona_id
        self.nombre = nombre
        self.unidad = unidad
        self.valor = valor
        self.timestamp = datetime.datetime.now().isoformat()

    def to_dict(self):
        return {
            "sensor_id": self.sensor_id,
            "persona_id": self.persona_id,
            "nombre": self.nombre,
            "valor": self.valor,
            "unidad": self.unidad,
            "timestamp": self.timestamp
        }

def get_metrics():
    return Metrica(
        sensor_id=1,
        persona_id=3,
        nombre="Temperature",
        unidad="C",
        valor=round(random.uniform(36, 65), 2)
    )

def main():
    sio.connect(WS_URL, namespaces=["/sensors/metrics"])

    while True:
        metrica = get_metrics().to_dict()
        sio.emit("message", metrica, namespace="/sensors/metrics")
        print(f"[TEMPERATURE] ({datetime.datetime.now().isoformat()}) : {metrica}")
        time.sleep(5)

if __name__ == "__main__":
    main()
