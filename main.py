import json
import logging

from datetime import datetime
import paho.mqtt.client as mqtt
from google.cloud import bigquery

MQTT_HOST = "192.168.1.160"
MQTT_PORT = 1883
TOPIC = "energy-monitor/status/em:0"
BQ_TABLE_NAME = "home-iot-437703.metrics.energy-monitor"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def stream_data(table_name, row):
    client = bigquery.Client.from_service_account_json("./service_account.json")

    client.load_table_from_json(
        [row], table_name, job_config=bigquery.LoadJobConfig(autodetect=True)
    )
    logger.info(f'[{row["timestamp"]}] Loaded 1 row into {table_name}')


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code " + str(rc))
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    value = str(msg.payload.decode("utf-8"))
    message = json.loads(value)

    try:
        table_name = BQ_TABLE_NAME
        message["topic"] = msg.topic
        message["timestamp"] = datetime.now().isoformat()
        stream_data(table_name, message)
    except Exception as e:
        logger.info(str(e))


def main():
    broker_ip = MQTT_HOST
    broker_port = MQTT_PORT
    logger.info(f"Connecting to {broker_ip}:{broker_port}")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_ip, broker_port)
    client.loop_forever()


if __name__ == "__main__":
    main()
