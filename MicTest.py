import queue, json, words
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from skills import *

q = queue.Queue()

model = Model('model_small')

device = sd.default.device
samplerate = int(sd.query_devices(device[2], 'input')['default_samplerate'])

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def recognize(data, vectorizer, clf):
    trg = words.TRIGGERS.intersection(data.split())
    if not trg:
        return
    data.replace(list(trg)[0], '')
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    speaker(answer)

def main():
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set
    speaker('Попроси телефончик что-то сделать')
    with sd.RawInputStream(samplerate=samplerate, blocksize = 48000, device=device[0],
            dtype="int16", channels=1, callback=callback):

        rec = KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                print(data)
                recognize(data, vectorizer, clf)
            # else:
            #     print(rec.PartialResult())

if __name__ == '__main__':
    main()