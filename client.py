import random
from datetime import datetime
from enlace import *
import numpy as np

def main():
    try:
        com1 = enlace('/dev/ttyACM0')

        com1.enable()

        commandList = [b'00FF', b'00', b'0F', b'F0', b'FF00', b'FF']

        listLenght = random.randint(10,30)

        listBytes = []

        initTime = datetime.now()

        for lenght in range(listLenght):
            listBytes.append(random.choice(commandList))

        com1.sendData(np.array(listBytes))
        print(np.array(listBytes))
        print('deu bom')
        com1.disable()

    except Exception as erro:     
        print('F')
        print(erro) 
        com1.disable()
   


if __name__ == "__main__":
    main()