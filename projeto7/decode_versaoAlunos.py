#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.fftpack import fft, fftshift
import sys
from suaBibSignal import *
import sounddevice as sd
import soundfile   as sf
import peakutils
import time 
#Importe todas as bibliotecas
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


def freq_to_num(freqs):
    frequencia_w = [697, 770, 852, 941]
    frequencia_z = [1209, 1336, 1477, 1633]
    mais_perto1 = 100
    mais_perto2 = 100
    for freq in frequencia_w:
        if abs(freq - freqs[0]) < mais_perto1:
            mais_perto1 = abs(freq-freqs[0])
            frequencia1 = freq
    for freq in frequencia_z:
        if abs(freq - freqs[1]) < mais_perto2:
            mais_perto2 = abs(freq-freqs[1])
            frequencia2 = freq
    frequencias = [frequencia2, frequencia1]
    return frequencias

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    signal = signalMeu()
    fs = 44100
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = fs
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = 4

    # faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    print("A captação de áudio iniciará em 3 segundos")
    #use um time.sleep para a espera
    time.sleep(1)
    print('3')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('1')
   #faca um print informando que a gravacao foi inicializada
   
   #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
   #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
   
    numAmostras = duration*fs
    freqDeAmostragem = fs
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    dados = []
    for dado in audio:
        dados.append(dado[0])

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t = np.linspace(-duration/2,duration/2,duration*fs)

    # plot do gravico  áudio vs tempo!
   
    plt.plot(t, audio)
    plt.grid()
    plt.title('Áudio vs Tempo')

    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(dados, fs)
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')    

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.

    freqs = []
    index = peakutils.indexes(np.abs(yf), thres=0.2, min_dist=200)
    print("index de picos {}" .format(index))
    for freq in xf[index]:
        freqs.append(freq)
        print("freq de pico sao {}" .format(freq))

    #printe os picos encontrados! 
    print(freq_to_num(freqs))

    frequencias = freq_to_num(freqs)

    for key in signalDict:
        if signalDict[key] == frequencias:
            print('A tecla pressionada foi {}'.format(key))

    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
  
    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()