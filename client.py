import random
from datetime import datetime
from sys import byteorder
from math import *
from numpy.core.fromnumeric import size
from enlace import *
import numpy as np
import traceback

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
    id_server = b"\xCC"
    datagram += id_server

    #h3
    datagram += n_total

    #h4
    datagram += n_pacote

    #h5
    if type != b"\x03":
        id_arquivo = b"\x00"
        datagram += id_arquivo
    else:
        datagram += len(payload).to_bytes(1, byteorder='big')

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
    return create_datagram(b"\x01", b"\xCC", n_total, b"\x00", b"\x00", b"\x00", payload)

def tipo3(n_total, n_pacote, payload):
    return create_datagram(b"\x03", b"\xCC", n_total, n_pacote, b"\x00", b"\x00", payload)

def tipo3_erro(n_total, n_pacote, payload):
    return create_datagram(b"\x03", b"\xCC", n_total, b"\x0A", b"\x00", b"\x00", payload)

def tipo5(n_total, payload):
    return create_datagram(b"\x05", b"\xCC", n_total, b"\x00", b"\x00", b"\x00", payload)

def main():
    try:
        com1 = enlace("COM4")

        com1.enable()

        conectando = False
        while not conectando:
            txBuffer = tipo1(ceil(len(img)/114).to_bytes(1, byteorder= 'big'), b"\xBB"b"\xBB"b"\xBB"b"\xBB")
            #print(len(np.asarray(txBuffer)))
            com1.sendData(np.asarray(txBuffer))
            with open ("Client5.txt", "a") as file:
                msg = str(datetime.now()) + ' / ' + 'envio' + ' / ' + '1' + ' / '  + '18'
                file.write(msg)
                file.write('\n')
            print("Mensagem incial enviada")
            print('---------------')
            data = com1.getDataClient(1)
            try:
                with open ("Client5.txt", "a") as file:
                    msg = str(datetime.now()) + ' / ' + 'receb' + ' / ' + str(int.from_bytes(data[0][0], byteorder='big')) + ' / '  + '18'
                    file.write(msg)
                    file.write('\n')
            except:
                pass
            timer2_handshake = data[0][1]
            while True:
                if data[1] > 0:
                    if data[0][0] == b'\x02':
                        print("A mensagem enviado pelo servidor foi recebida, hora de começar o envio do arquivo")
                        stop = False

                    else:
                        print("A mensagem enviada pelo servidor não é a correta, portanto, finalizando conexão")
                        stop = True
                    
                    conectando = True
                    break 
                        
                elif time.time() - timer2_handshake > 20:
                    print("Não tivemos resposta do servidor, hora de finalizar a conexão")
                    txBuffer = tipo5(ceil(len(img)/114).to_bytes(1, byteorder= 'big'), b"\xBB"b"\xBB"b"\xBB"b"\xBB")
                    com1.sendData(np.asarray(txBuffer))
                    with open ("Client5.txt", "a") as file:
                        msg = str(datetime.now()) + ' / ' + 'envio' + ' / ' + '5' + ' / '  + '18'
                        file.write(msg)
                        file.write('\n')
                    print("O servidor já foi avisado que a conexão será finalizada")
                    print("Finalizando...")
                    stop = True
                    conectando = True
                    break
            
        if stop == True:
            pass

        else:
            cont = 1
            for bytes in range(ceil(len(img)/114)):
                time.sleep(1)
                payload = img[bytes*114: (bytes+1)*114]
                txBuffer = tipo3(ceil(len(img)/114).to_bytes(1, byteorder= 'big'), cont.to_bytes(1, byteorder= 'big') , payload)
                com1.sendData(np.asarray(txBuffer))
                with open ("Client5.txt", "a") as file:
                    msg = str(datetime.now()) + ' / ' + 'envio' + ' / ' + '3' + ' / '  + str(len(payload) + 14) + ' / ' + str(cont) + ' / ' + str(ceil(len(img)/114))
                    file.write(msg)
                    file.write('\n')
                print('---------------')
                print('Pacote {} enviado'.format(cont))
                print('---------------')
                com1.rx.clearBuffer()
                data = com1.getDataClient(1)
                try:
                    with open ("Client5.txt", "a") as file:
                        msg = str(datetime.now()) + ' / ' + 'receb' + ' / ' + str(int.from_bytes(data[0][0], byteorder='big')) + ' / '  + '18'
                        file.write(msg)
                        file.write('\n')
                except:
                    pass
                timer2 = data[0][1]
                if data[1] > 0:
                    if data[0][0] == b"\x04":
                        print('Pacote {} recebido'.format(cont))
                        cont += 1
                    elif data[0][0] == b"\x06":
                        com1.getDataClient(5)
                        pacote_errado = com1.getDataClient(1)
                        print('Houve um erro ao receber o pacote {}'.format(int.from_bytes(pacote_errado[0][0], byteorder='big')))
                        print('---------')
                        print('Enviando novamente o pacote que teve erro')
                        while True:
                            time.sleep(1)
                            txBuffer = tipo3(ceil(len(img)/114).to_bytes(1, byteorder= 'big'), cont.to_bytes(1, byteorder= 'big') , payload)
                            com1.sendData(np.asarray(txBuffer))
                            with open ("Client5.txt", "a") as file:
                                msg = str(datetime.now()) + ' / ' + 'envio' + ' / ' + '3' + ' / '  + str(len(payload) + 14) + ' / ' + str(cont) + ' / ' + str(ceil(len(img)/114))
                                file.write(msg)
                                file.write('\n')
                            print('---------------')
                            print('Pacote {} enviado novamente'.format(cont))
                            print('---------------')
                            com1.rx.clearBuffer()
                            data = com1.getDataClient(1)
                            with open ("Client5.txt", "a") as file:
                                msg = str(datetime.now()) + ' / ' + 'receb' + ' / ' + str(int.from_bytes(data[0][0], byteorder='big')) + ' / '  + '18'
                                file.write(msg)
                                file.write('\n')
                            if data[1] > 0:
                                if data[0][0] == b"\x04":
                                    print('Pacote que teve erro agora foi recebido com sucesso')
                                    cont += 1
                                    break
                                else:
                                    print('Houve um erro ao receber o pacote {} novamente'.format(int.from_bytes(pacote_errado[0][0], byteorder='big')))
                            else:
                                print('Enviando novamente o pacote que deu erro')
                    else:
                        print("NAO RECEBI A CONFIRMACAO DO ZECA")
                else:
                    finaliza = True
                    while (time.time()-timer2) < 20:
                        txBuffer = tipo3(ceil(len(img)/114).to_bytes(1, byteorder= 'big'), cont.to_bytes(1, byteorder= 'big') , payload)
                        com1.sendData(np.asarray(txBuffer))
                        with open ("Client5.txt", "a") as file:
                            msg = str(datetime.now()) + ' / ' + 'envio' + ' / ' + '3' + ' / '  + str(len(payload) + 14) + ' / ' + str(cont) + ' / ' + str(ceil(len(img)/114))
                            file.write(msg)
                            file.write('\n')
                        print('Pacote {} enviado novamente'.format(cont))
                        print('---------------')
                        com1.rx.clearBuffer()
                        data = com1.getDataClient(1)
                        try:
                            with open ("Client5.txt", "a") as file:
                                msg = str(datetime.now()) + ' / ' + 'receb' + ' / ' + str(int.from_bytes(data[0][0], byteorder='big')) + ' / '  + '18'
                                file.write(msg)
                                file.write('\n')
                        except:
                            pass
                        if data[1] > 0:
                            if data[0][0] == b"\x04":
                                print('Pacote {} recebido'.format(cont))
                                cont += 1
                                finaliza = False
                                break
                            elif data[0][0] == b"\x06":
                                com1.getDataClient(5)
                                pacote_errado = com1.getDataClient(1)
                                with open ("Client5.txt", "a") as file:
                                    msg = str(datetime.now()) + ' / ' + 'receb' + ' / ' + str(int.from_bytes(data[0][0], byteorder='big')) + ' / '  + '18'
                                    file.write(msg)
                                    file.write('\n')
                    if (time.time()-timer2) > 20 and finaliza:
                        txBuffer = tipo5(ceil(len(img)/114).to_bytes(1, byteorder= 'big'), b"\xBB"b"\xBB"b"\xBB"b"\xBB")
                        com1.sendData(np.asarray(txBuffer))
                        with open ("Client5.txt", "a") as file:
                            msg = str(datetime.now()) + ' / ' + 'envio' + ' / ' + '5' + ' / '  + '18'
                            file.write(msg)
                            file.write('\n')
                        print('SEM TEMPO IRMÃO, CORTANDO RELAÇÕES')
                        break
        print("Comunicação encerrada")
        com1.disable()               
    except Exception as erro:     
        print("F")
        print(traceback.format_exc()) 
        com1.disable()

if __name__ == "__main__":
    main()   