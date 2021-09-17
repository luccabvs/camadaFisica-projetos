from numpy.lib.shape_base import expand_dims
from enlace import *
import numpy as np
import time
import sys
import PIL.Image as Image
import io
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

serialName = '/dev/ttyACM0'

'''def main():
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
        com1.disable()'''

def send_ok(com1):
    com1.sendData(np.asarray([b'\xAA\xAA\xAA']))

def send_fail(com1):
    com1.sendData(np.asarray([b'\xFF\xFF\xFF']))

def handle_package(com1):
    received_id = com1.getData(4)
    total = com1.getData(4)
    size = com1.getData(1)

    payload = com1.getData(int.from_bytes(size[0], byteorder='big'))
    eop = com1.getData(4)

    if eop[0] == b'\xBB\xBB\xBB\xBB':
        pass    
    else:
        send_fail(com1)
        return 
    
    if int.from_bytes(received_id[0], byteorder='big') == int.from_bytes(total[0], byteorder='big')-1:
        return [payload[0], received_id, "over"]
    return [payload[0], received_id]


def main():
    try:
        com1 = enlace(serialName)
        com1.enable()
        com1.rx.fisica.flush()
        com1.rx.clearBuffer()

        #handshake
        transfer_type = com1.getData(1)
        if transfer_type[0] == b'\x01':
            handle_package(com1)
            send_ok(com1)

        package = []
        print('------------------')
        print('Hanshake completo!')
        print('------------------')
        
        check_id = 0

        print('Iniciando transmissão!')
        print('----------------------')

        while True:
            com1.rx.clearBuffer()
            transfer_type = com1.getData(1)
            
            payload = ''
            id_received = ''
            over = ''

            if transfer_type[0] == b'\x00':
                handle_package_content = handle_package(com1)
                payload = handle_package_content[0]
                id_received = int.from_bytes(handle_package_content[1][0], byteorder='big')
                try:
                    over = handle_package_content[2]
                except:
                    pass
                if id_received == check_id:
                    package.append(payload)
                    send_ok(com1)
                    print('Pacote número {} recebido!'.format(id_received+1))
                    print('--------------------------')
                    check_id += 1

                else:
                    send_fail(com1)
                    print('Houve um erro. Pacote número {} recebido! O pacote correto era o número {}'.format(id_received+1, check_id))
                    print('---------------------------------------------------------------------------')                


            if over == 'over':
                break
        
        print('Transmissão Finalizada!')
        print('------------------------')
        time.sleep(2)
        print('Número total de pacotes recebidos: {}'.format(len(package)))
        print('-------------------------------------')

        image = Image.open(io.BytesIO(np.asarray(package)))
        image.save('imagemRecebida.jpg')    
        
        com1.disable()

    except Exception as e:
        print("ops! :-\\")
        print(e)
        com1.disable()



if __name__ == "__main__":
    main()