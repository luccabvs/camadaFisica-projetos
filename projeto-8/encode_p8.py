from suaBibSignal import signalMeu 
from funcoes_LPF import LPF
from scipy.io import wavfile
import sounddevice as sd

def main():
    signal = signalMeu()
    
    samplerate, data = wavfile.read('/home/josermf/Insper/4oSemestre/CamadaFisica/camadaFisica-projetos/projeto-8/audio.wav')

    max_data = max([abs(i) for i in data])

    normalized_data = []

    for i in data:
        normalized_data.append(i/max_data)

    filtred_data = LPF(normalized_data, 4000, samplerate)

    portadora = 14000

    x, y = signal.generateSin(portadora, 1, 5, samplerate)

    x = x[0:len(filtred_data)]
    y = y[0:len(filtred_data)]

    audioModulado = y*filtred_data
    audioDemodulado = y*audioModulado

    sd.play(audioModulado, samplerate)

    sd.wait()

if __name__ == "__main__":
    main()