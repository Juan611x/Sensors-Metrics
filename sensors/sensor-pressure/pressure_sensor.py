import grpc
import metrics_pb2
import metrics_pb2_grpc
import time
import random
import datetime


class Metrica:
    def __init__(self, sensor_id, persona_id, nombre, unidad, valor):
        self.sensor_id = sensor_id
        self.persona_id = persona_id
        self.nombre = nombre
        self.unidad = unidad
        self.valor = valor
        self.timestamp = datetime.datetime.now().isoformat()

    def to_grpc_request(self):
        return metrics_pb2.MetricaRequest(
            sensor_id=self.sensor_id,
            persona_id=self.persona_id,
            nombre=self.nombre,
            unidad=self.unidad,
            valor=self.valor,
            timestamp=self.timestamp
        )
    
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
        nombre="Pressure",
        unidad="BPM",
        valor=round(random.uniform(36, 65), 2)
    )


def main():
    with grpc.insecure_channel('gateway:3000') as channel:
        stub = metrics_pb2_grpc.MetricsServiceStub(channel)
        while True:
            metrica = get_metrics()
            response = stub.EnviarMetrica(metrica.to_grpc_request())
            print(f"[PRESSURE] ({datetime.datetime.now().isoformat()}) : {metrica.to_dict()}")
            time.sleep(5)


if __name__ == '__main__':
    main()
