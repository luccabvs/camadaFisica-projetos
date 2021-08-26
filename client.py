import random
from datetime import datetime
import enlace
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

        print('deu bom')
    except Exception as erro:     
       print('F')
       print(erro) 
       


if __name__ == "__main__":
    main()