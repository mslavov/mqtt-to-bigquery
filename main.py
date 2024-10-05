import json
from datetime import datetime
from configparser import ConfigParser
import paho.mqtt.client as mqtt
from google.cloud import bigquery


def config_read():
    parser = ConfigParser()
    parser.read("./etc/mqtt.conf")
    return parser


def stream_data(table_name, row):
    client = bigquery.Client.from_service_account_json("./service_account.json")

    client.load_table_from_json(
        [row], table_name, job_config=bigquery.LoadJobConfig(autodetect=True)
    )
    print(f'[{row["timestamp"]}] Loaded 1 row into {table_name}')


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    topic = config_read().get("mqtt_broker", "topic")
    client.subscribe(topic)


def on_message(client, userdata, msg):
    value = str(msg.payload.decode("utf-8"))
    # print(f"[{msg.topic}] {value}")
    message = json.loads(value)

    try:
        table_name = config_read().get("gcp", "table_name")
        message["topic"] = msg.topic
        message["timestamp"] = datetime.now().isoformat()
        stream_data(table_name, message)
    except Exception as e:
        print(str(e))


def main():
    broker_ip = config_read().get("mqtt_broker", "ip")
    broker_port = config_read().getint("mqtt_broker", "port")
    broker_timeout = config_read().getint("mqtt_broker", "timeout")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_ip, broker_port, broker_timeout)
    client.loop_forever()


if __name__ == "__main__":
    main()
