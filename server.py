from numpy.lib.shape_base import expand_dims
from enlace import *

serialName = 'COM5'

def main():
    try:
        com1 = enlace('COM5')
        com1.enable()

        listResult = []
        

        while True:
            txLen = com1.rx.getBufferLen()
            rxBuffer, nRx = com1.getData(txLen)
            if len(rxBuffer) > 0:
                print(rxBuffer)
                listResult.append(rxBuffer)
                break
            
        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()