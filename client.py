import random
from datetime import datetime
from sys import byteorder
from math import *
from numpy.core.fromnumeric import size
from enlace import *
import numpy as np

with open('tupa_fc.png', 'rb') as file:
    img = file.read()

print(ceil(len(img)/114).to_bytes(4, byteorder= 'big'))
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

def main():
    try:
        com1 = enlace("COM4")

        com1.enable()

        conectando = True
        while conectando:
            txBuffer = tipo1(ceil(len(img)/114).to_bytes(1, byteorder= 'big'), b"\xAA"b"\xAA"b"\xAA"b"\xAA")
            #print(len(np.asarray(txBuffer)))
            com1.sendData(np.asarray(txBuffer))

            data = com1.getDataClient(1)

            if data[1] > 0:
                while True:
                    if data[0] == b"\x02":
                        print("A mensagem enviado pelo servidor foi recebida, hora de começar o envio do arquivo")
                        stop = False
                    else:
                        print("A mensagem enviada pelo servidor não é a correta, portanto, finalizando conexão")
                        stop = True
                    
                    conectando = False

            else:
                print("Não tivemos resposta do servidor, hora de finalizar a conexão")
                txBuffer = tipo5(ceil(len(img)/114).to_bytes(1, byteorder= 'big'), b"\xAA"b"\xAA"b"\xAA"b"\xAA")
                com1.sendData(np.asarray(txBuffer))
                print("O servidor já foi avisado que a conexão será finalizada")
                print("Finalizando...")
                stop = True
                conectando = False

        if stop == True:
            pass

        else:
            for bytes in range(ceil(len(img)/114)):
                payload = img[bytes*114: (bytes+1)*114]
                payload_size = len(payload)
                #erro_id = 3
                txBuffer = tipo3(ceil(len(img)/114).to_bytes(1, byteorder= 'big'), bytes.to_bytes(4, byteorder= 'big') , payload)
                com1.sendData(np.asarray(txBuffer))
                print('---------------')
                print('Pacote {} enviado'.format(bytes))
                print('---------------')
                lenght = com1.getDataClient(1)
                if lenght[1] > 0:
                    if lenght[0] == b"\x04":
                        print('Pacote {} recebido'.format(bytes))
                    elif lenght[0] == b"\x06":
                        com1.getDataClient(5)
                        pacote_errado = com1.getDataClient(5)
                        print('Houve um erro ao receber o pacote {}'.format(int.from_bytes(pacote_errado, byteorder='big')))
                        print('---------')
                        print('Enviando novamente o pacote que teve erro')
                        while True:
                            com1.sendData(np.asarray(txBuffer))
                            txBuffer = tipo3(ceil(len(img)/114).to_bytes(1, byteorder= 'big'), bytes.to_bytes(4, byteorder= 'big') , payload)
                            com1.sendData(np.asarray(txBuffer))
                            print('---------------')
                            print('Pacote {} enviado'.format(bytes))
                            print('---------------')
                            lenght = com1.getDataClient(3)
                            if lenght[1] > 0:
                                if lenght[0] == b"\x04":
                                    print('Pacote que teve erro agora foi recebido com sucesso'.format(bytes))
                                    break
                                else:
                                    print('Houve um erro ao receber o pacote {} novamente'.format(int.from_bytes(pacote_errado, byteorder='big')))
                else:
                    txBuffer = tipo5(ceil(len(img)/114).to_bytes(1, byteorder= 'big'), b"\xAA"b"\xAA"b"\xAA"b"\xAA")
                    com1.sendData(np.asarray(txBuffer))
                    print('SEM TEMPO IRMÃO, CORTANDO RELAÇÕES')
                    break

        print("Comunicação encerrada")
        com1.disable()               
    except Exception as erro:     
        print("F")
        print(erro) 
        com1.disable()

if __name__ == "__main__":
    main()   