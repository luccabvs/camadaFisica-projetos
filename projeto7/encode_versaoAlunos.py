import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.fftpack import fft, fftshift
import sys
from suaBibSignal import *
import sounddevice as sd
import soundfile   as sf
import peakutils

#importe as bibliotecas


def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    print("Inicializando encoder")
    
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    signal = signalMeu()
    fs  = 44100
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    
    duration = 1 #tempo em segundos que ira emitir o sinal acustico 
    A   = 1.5   # Amplitude

#relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3


    print("Gerando Tons base")
    
    signalDict = {
        '1':[1209, 697], 
        '2':[1336, 697],
        '3':[1477, 697],
        '4':[1209, 770],
        '5':[1336, 770],
        '6':[1477, 770],
        '7':[1209, 852],
        '8':[1336, 852],
        '9':[1477, 852],
        '0':[1336, 941],
        'X':[1209, 941],
        '#':[1477, 941],
        'A':[1633, 697],
        'B':[1633, 770],
        'C':[1633, 852],
        'D':[1633, 941]
    }

    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y 
    #use para isso sua biblioteca (cedida)
    def generateDTMF(key):
        freqs = signalDict[key]
        x = 0
        y = 0
        for freq in freqs:
            x += signal.generateSin(freq, A, duration, fs)[0]
            y += signal.generateSin(freq, A, duration, fs)[1]
        
        '''plt.figure()
        plt.plot(x, y)
        plt.xlim(0, 0.01)'''
        return (x, y)

    #obtenha o vetor tempo tb.
    t   = np.linspace(-duration/2,duration/2,duration*fs)
    print(t)
    #deixe tudo como array

    #printe a mensagem para o usuario teclar um numero de 0 a 9. 
    #nao aceite outro valor de entrada.
    numFlag = True
    while numFlag:
        NUM = input('Digite uma tecla: ')
        if NUM in signalDict:
            numFlag = False
        else:
            print('---Tecla inválida---')
    print("Gerando Tom referente ao símbolo : {}".format(NUM))
    
    #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides
    tone = generateDTMF(NUM)
    #printe o grafico no tempo do sinal a ser reproduzido
    # reproduz o som
    sd.play(tone, fs)
    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()

if __name__ == "__main__":
    main()