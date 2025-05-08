import time
import requests
import random
import datetime

URL_GATEWAY = "http://gateway:5000/sensors/metrics"


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
        nombre="Heartrate",
        unidad="BPM",
        valor= round(random.uniform(36, 65), 2)
    )


def main():
    while True:
        metric = get_metrics().to_dict()
        try:
            resp = requests.post(URL_GATEWAY, json=metric)
            print(f"[HEARTRATE] ({datetime.datetime.now().isoformat()}) : {metric}")
        except:
            print(f"[hear] ({datetime.datetime.now().isoformat()}) : ERROR...!")

        time.sleep(5)


if __name__ == "__main__":
    main()