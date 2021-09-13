import random
from datetime import datetime
from sys import byteorder
from enlace import *
import numpy as np

def generate_commandList():
    commandList = [b"\xFF", b"\x00", b"\x0F", b"\xF0", b"\xFF"b"\x00", b"\x00"b"\xFF"]
    listLenght = random.randint(10,30)
    listBytes = []
    listBytesWithoutFlags = []
    for lenght in range(listLenght):
        command = random.choice(commandList)
        if len(command) == 2:
            listBytes.append(b"\xAA")
        listBytes.append(command)
        listBytesWithoutFlags.append(command)
    listBytes.append(b"\xBB")
    listBytes_to_Array = b"".join(listBytes)
    return listBytes_to_Array, listBytesWithoutFlags

def main():
    try:
        com1 = enlace("/dev/ttyACM0")

        com1.enable()
        
        com1.sendData(b"\xdd")

        txBuffer, listBytesWithoutFlags = generate_commandList()

        time.sleep(1)

        com1.sendData(np.asarray(txBuffer))
        print(f'Tamanho da lista enviada: {len(listBytesWithoutFlags)}')

        while True:
            lenght = com1.getData(1)
            if len(lenght) > 0:
                received = int.from_bytes(lenght[0], byteorder='big')
                print('Tamanho da lista recebida: {}'.format(received))
                break

        com1.disable()


    except Exception as erro:     
        print("F")
        print(erro) 
        com1.disable()


if __name__ == "__main__":
    main()   