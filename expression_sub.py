import paho.mqtt.client as mqtt
import json

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    #m_in=json.loads(m_decode) 
    #print(type(m_in))

    with open('expression.txt', 'a') as f:
        f.write('\n')
        f.write(str(m_decode))
        f.close()
          
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect

mqttc.connect("mqtt.eclipseprojects.io", 1883, 60)
mqttc.subscribe("AAIB-LT", 0)

mqttc.loop_forever()