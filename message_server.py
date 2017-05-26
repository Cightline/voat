
# this recieves messages from MQTT and publishes messages
# the REST server will publish messages (that way we can call it soon as it happens)

# docs
# https://pypi.python.org/pypi/paho-mqtt

# some MQTT stuff that you probably wont read
# https://thenewstack.io/messaging-reliability-persistence-mqtt/

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print('Connected with result code %s' % (rc))

    client.subscribe('messages')




def on_message(client, userdata, msg):
    print('message_topic: %s message_payload: %s' % (msg.topic, msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


#client.connect('iot.eclipse.org', 1883, 60)
client.connect('localhost', 1883, 60)


client.loop_forever()



