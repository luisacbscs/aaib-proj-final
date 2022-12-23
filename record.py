import sounddevice as sd


fs = 44100

# Recording duration
max_duration = 2

print('start')
recording = sd.rec(int(max_duration * fs), samplerate=fs, channels=1)

# Record audio for the given number of seconds
sd.wait()
print('done')

file = 'divide.txt'

lst = [i[0] for i in recording]

listToStr = ' '.join([str(elem) for elem in lst])

with open(file, 'a') as f:
    f.write(listToStr)
    f.write("\n")
    f.close()

with open(file, 'r') as f:
    lines = f.readlines()
    print('{} now has {} audios'.format(file, len(lines)))
    f.close()

