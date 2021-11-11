from suaBibSignal import * 
from funcoes_LPF import LPF
from scipy.io import wavfile
import sounddevice as sd
import matplotlib.pyplot as plt   
from scipy import * 

def main():
    signal = signalMeu()

    samplerate, data = wavfile.read('projeto-8/new_audio.wav')

    xf, yf = signal.calcFFT(data, samplerate)

    portadora = 14000

    x, y = signal.generateSin(portadora, 1, 5, samplerate)

    x = x[0:len(data)]
    y = y[0:len(data)]

    audio_demodulado  = y * data

    signal.plotFFT(audio_demodulado, samplerate)
    plt.title("Áudio demodulado x Frequência")
    plt.xlabel("Frequência")
    plt.ylabel("Áudio demodulado")
    plt.grid()

    audio_filtrado = LPF(audio_demodulado, 4000, samplerate)

    max_data = max([abs(i) for i in audio_filtrado])

    normalized_data = []

    for i in audio_filtrado:
        normalized_data.append(i/max_data)

    audio_final = LPF(normalized_data, 4000, samplerate)

    print("Iniciano reprodução de áudio")
    sd.play(audio_final)

    signal.plotFFT(audio_filtrado, samplerate)
    plt.grid()
    plt.title("Áudio demodulado e filtrado x Frequência")
    plt.xlabel("Frequência")
    plt.ylabel("Áudio demodulado e filtrado")

    plt.show()

    sd.wait()

if __name__ == "__main__":
    main()