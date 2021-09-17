import random
from datetime import datetime
from sys import byteorder
from math import *
from numpy.core.fromnumeric import size
from enlace import *
import numpy as np

with open('tupa_fc.png', 'rb') as file:
    img = file.read()
'''def generate_commandList():
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
    return listBytes_to_Array, listBytesWithoutFlags'''

def create_datagram(type, payload=b"\xAA" b"\xAA" b"\xAA", id=int(1).to_bytes(4, byteorder= 'big'), size=b"\x03", total=int(1).to_bytes(4, byteorder= 'big')):
    datagram = b''
    #head
    if type == 'data':
        datagram += b"\x00"
    elif type == 'handshake':
        datagram += b"\x01"

    datagram += id
    datagram += total
    datagram += size

    #payload
    datagram += payload

    datagram += b"\xBB" b"\xBB" b"\xBB" b"\xBB"
    return datagram

#print(np.asarray(create_datagram("handshake")))

'''def main():
    try:
        com1 = enlace("/dev/ttyACM0")

        com1.enable()

        id = 1

        while 

        #txBuffer, listBytesWithoutFlags = generate_commandList()

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
        com1.disable()'''

def main():
    try:
        com1 = enlace("COM4")

        com1.enable()


        while True:
            txBuffer = create_datagram('handshake')
            #print(len(np.asarray(txBuffer)))
            com1.sendData(np.asarray(txBuffer))

            lenght = com1.getDataClient(3)

            if lenght[1] > 0:
                stop = False
                break

            elif lenght[0] == True:
                continue

            else:
                stop = True
                break
        
        if stop == True:
            pass
        else:
            for bytes in range(ceil(len(img)/114)):
                payload = img[bytes*114: (bytes+1)*114]
                payload_size = len(payload)
                #erro_id = 3
                txBuffer = create_datagram('data', payload=payload, id=bytes.to_bytes(4, byteorder= 'big'), size=payload_size.to_bytes(1, byteorder= 'big'), total= ceil(len(img)/114).to_bytes(4, byteorder= 'big'))
                com1.sendData(np.asarray(txBuffer))
                print('---------------')
                print('Pacote {} enviado'.format(bytes))
                print('---------------')
                lenght = com1.getDataClient(3)
                if lenght[1] > 0:
                    if lenght[0] == b"\xAA"b"\xAA"b"\xAA":
                        print('Pacote {} recebido'.format(bytes))
                    elif lenght[0] == b"\xFF"b"\xFF"b"\xFF":
                        print('Houve um erro ao receber o pacote'.format(bytes.to_bytes(4, byteorder= 'big')))
                        print('---------')
                        print('Enviando novamente o pacote que teve erro')
                        while True:
                            com1.sendData(np.asarray(txBuffer))
                            txBuffer = create_datagram('data', payload=payload, id=bytes.to_bytes(4, byteorder= 'big'), size=payload_size.to_bytes(1, byteorder= 'big'), total= ceil(len(img)/114).to_bytes(4, byteorder= 'big'))
                            com1.sendData(np.asarray(txBuffer))
                            print('---------------')
                            print('Pacote {} enviado'.format(bytes))
                            print('---------------')
                            lenght = com1.getDataClient(3)
                            if lenght[1] > 0:
                                if lenght[0] == b"\xAA"b"\xAA"b"\xAA":
                                    print('Pacote que teve erro agora foi recebido com sucesso'.format(bytes))
                                    break
                                else:
                                    print('Houve um erro ao receber o pacote')

                elif lenght[0] == True:
                    continue

                else:
                    break

        com1.disable()               
    except Exception as erro:     
        print("F")
        print(erro) 
        com1.disable()

if __name__ == "__main__":
    main()   