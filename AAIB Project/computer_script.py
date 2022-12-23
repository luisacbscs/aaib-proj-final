import sounddevice as sd
import paho.mqtt.client as mqtt
import tsfel
import joblib
from time import sleep
loaded_model = joblib.load('model4.joblib')


def get_features(x):
    features = ['0_Absolute energy',
                '0_LPCC_11',
                '0_LPCC_6',
                '0_MFCC_0',
                '0_Mean absolute diff',
                '0_Mean diff',
                '0_Median frequency',
                '0_Neighbourhood peaks',
                '0_Skewness',
                '0_Spectral centroid',
                '0_Wavelet energy_4',
                '0_Wavelet entropy']

    cfg_file = tsfel.get_features_by_domain()
    rec = tsfel.time_series_features_extractor(cfg_file, x, fs=44100)
    rec = rec[features]

    return rec
def on_publish(mqttc, obj, msg):
    print('sent')

def on_message(mqttc, obj, msg):

    if msg.payload.decode('UTF-8') == 'start':

        fs = 44100
        max_duration = 2

        print('start recording')
        recording = sd.rec(int(max_duration * fs), samplerate=fs, channels=1)
        sd.wait()
        print('done')

        recording = [i[0] for i in recording]

        x = get_features(recording)
        y = loaded_model.predict(x)
        print(y)
        sleep(60)
        mqttc.publish('AAIB-LT', payload= y[0])


try:
    mqttc = mqtt.Client()
    mqttc.on_publish = on_publish
    mqttc.on_message = on_message
    mqttc.connect("192.168.1.98")
    mqttc.subscribe("AAIB-TL", 0)

    mqttc.loop_forever()

except KeyboardInterrupt:
    print('Communication terminated.')
