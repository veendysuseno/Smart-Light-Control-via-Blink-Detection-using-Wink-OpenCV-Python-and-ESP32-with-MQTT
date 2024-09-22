import random
from paho.mqtt import client as mqtt_client
broker = 'broker.emqx.io'
port = 1883
topic = "htmtfunas/97921921312/tes"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
client = mqtt_client.Client(client_id)
client.connect(broker, port)

client.publish(topic, "Hello, I'm Veendy")
