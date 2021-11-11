from suaBibSignal import signalMeu 
from funcoes_LPF import LPF
from scipy.io import wavfile
import sounddevice as sd
import soundfile   as sf
import matplotlib.pyplot as plt
import numpy as np

def main():
    signal = signalMeu()

    samplerate, data = wavfile.read('/home/josermf/Insper/4oSemestre/CamadaFisica/camadaFisica-projetos/projeto-8/audio.wav')

    duration = int(len(data)/samplerate)

    t = np.linspace(0, duration, duration*samplerate)

    max_data = max([abs(i) for i in data])

    normalized_data = []

    for i in data:
        normalized_data.append(i/max_data)
    
    plt.figure()
    plt.plot(t, normalized_data[:len(t)])
    plt.ylabel('Áudio Normalizado')
    plt.xlabel('Tempo')
    plt.grid()
    plt.title('Áudio Normalizado vs Tempo')
    
    filtred_data = LPF(normalized_data, 4000, samplerate)

    plt.figure()
    plt.plot(t, filtred_data[:len(t)])
    plt.ylabel('Áudio Filtrado')
    plt.xlabel('Tempo')
    plt.grid()
    plt.title('Áudio Filtrado vs Tempo')

    signal.plotFFT(filtred_data, samplerate)
    plt.title('Áudio Filtrado vs Frequencia')

    portadora = 14000

    x, y = signal.generateSin(portadora, 1, 5, samplerate)

    x = x[0:len(filtred_data)]
    y = y[0:len(filtred_data)]

    audio_modulado = y*filtred_data
    audio_Demodulado = y*audio_modulado

    plt.figure()
    plt.plot(t, audio_modulado[:len(t)])
    plt.ylabel('Áudio Modulado')
    plt.xlabel('Tempo')
    plt.grid()
    plt.title('Áudio Modulado vs Tempo')

    signal.plotFFT(audio_modulado, samplerate)
    plt.title('Áudio Modulado vs Frequencia')

    sd.play(audio_Demodulado, samplerate)
    sf.write('new_audio.wav', audio_modulado, samplerate)

    sd.wait()

    plt.show()

if __name__ == "__main__":
    main() 