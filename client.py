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

def create_datagram(type, id_server, n_total, n_pacote, n_reenvio, ultimo_pacote_recebido, payload):
    datagram = b''

    #head
    #h0
    datagram += type

    #h1
    id_sensor = b"\x00"
    datagram += id_sensor

    #h2
    datagram += id_server

    #h3
    datagram += n_total

    #h4
    datagram += n_pacote

    #h5
    if type != 3:
        id_arquivo = b"\x00"
        datagram += id_arquivo
    else:
        datagram += len(payload)

    #h6
    datagram += n_reenvio

    #h7
    datagram += ultimo_pacote_recebido

    #h8
    datagram += b"\x00"

    #h9
    datagram += b"\x00"

    #payload
    datagram += payload

    datagram += b"\xFF" b"\xAA" b"\xFF" b"\xAA"
    return datagram

def tipo1(n_total, payload):
    return create_datagram(b"\x01", b"\CC", n_total, b"x\00", b"\x00", b"\x00", payload)

def tipo3(n_total, n_pacote, payload):
    return create_datagram(b"\x03", b"\CC", n_total, n_pacote, b"\x00", b"\x00", payload)

def tipo5(n_total, payload):
    return create_datagram(b"\x05", b"\CC", n_total, b"x\00", b"\x00", b"\x00", payload)

#print(np.asarray(create_datagram("handshake")))

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
                else:
                    print('SEM TEMPO IRMÃO, CORTANDO RELAÇÕES')
                    break

        com1.disable()               
    except Exception as erro:     
        print("F")
        print(erro) 
        com1.disable()

if __name__ == "__main__":
    main()   