from numpy.lib.shape_base import expand_dims
from enlace import *
import time
serialName = 'COM4'

def main():
    try:
        com1 = enlace('COM4')
        com1.enable()
        com1.rx.clearBuffer()
        listResult = []

        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        while True:
            rxBuffer, nRx = com1.getData(1)
            if rxBuffer == b'\xBB':
                break   
            elif rxBuffer == b'\xAA':
                rxBuffer, nRx = com1.getData(2)
                listResult.append(rxBuffer)
            else:
                listResult.append(rxBuffer)

        print(listResult)
        print(len(listResult))

        com1.sendData(bytes([len(listResult)]))

        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()