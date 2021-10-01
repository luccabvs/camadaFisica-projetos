from numpy.lib.shape_base import expand_dims
from enlace import *
import numpy as np
import time
import sys
import PIL.Image as Image
import io
from PIL import ImageFile
import traceback
ImageFile.LOAD_TRUNCATED_IMAGES = True
from datetime import datetime

serialName = '/dev/ttyACM0'

def send_fail(com1):
    com1.sendData(np.asarray([b'\xFF\xFF\xFF']))

def receive_type1(com1):
    head = com1.getData(9)[0]
    payload = com1.getData(4)[0]
    eop = com1.getData(4)[0]
    if eop == b'\xff\xaa\xff\xaa' and head[1].to_bytes(1, byteorder='big') == b'\xcc':
        return "OK", head[2], len(head)+len(payload)+len(eop)
    else:
        return "ERROR", head[2], len(head)+len(payload)+len(eop)

def receive_type3(com1):
    head = com1.getData(9)[0]
    payload = com1.getData(head[4])[0]
    eop = com1.getData(4)[0]

    if eop == b'\xFF\xAA\xFF\xAA' and head[1].to_bytes(1, byteorder='big') == b'\xCC':
        return "OK", head[3], payload, len(head)+len(payload)+len(eop)
    else:
        return "ERROR", head[3], payload, len(head)+len(payload)+len(eop)
 

def send_type2(com1):
    com1.sendData(np.asarray([b'\x02\x00\xCC\x00\x00\x00\x00\x00\x00\x00\xBB\xBB\xBB\xBB\xFF\xAA\xFF\xAA']))

def send_type4(com1, last_id):
    msg = b'\x04\x00\xCC\x00\x00\x00' + last_id.to_bytes(1, byteorder= 'big') + b'\x00\x00\x00\xBB\xBB\xBB\xBB\xFF\xAA\xFF\xAA'
    com1.sendData(np.asarray([msg]))

def send_type5(com1):
    com1.sendData(np.asarray([b'\x05\x00\xCC\x00\x00\x00\x00\x00\x00\x00\xBB\xBB\xBB\xBB\xFF\xAA\xFF\xAA']))

def send_type6(com1, last_id):
    msg = b'\x06\x00\xCC\x00\x00\x00' + last_id.to_bytes(1, byteorder= 'big') + b'\x00\x00\x00\xBB\xBB\xBB\xBB\xFF\xAA\xFF\xAA'
    com1.sendData(np.asarray([msg]))

def main():
    try:     
        com1 = enlace(serialName)
        com1.enable()
        com1.rx.fisica.flush()
        com1.rx.clearBuffer()
        
        numPckg = 0
        ocioso = True
        
        timer1 = time.time()
        while ocioso: 
            if time.time()-timer1 < 20:
                #print('Servidor ocioso...')
          
                transfer_type = com1.getDataClient(1)
                if transfer_type[0][0] == b'\x01':
                    inicio, numPckg, tamPckg  = receive_type1(com1)
                    with open("Server5.txt", "a") as file:
                        msg = str(datetime.now()) + ' / ' + 'receb / ' + str(int.from_bytes(transfer_type[0][0], byteorder='big')) + ' / ' + str(tamPckg+1)
                        file.write(msg)   
                        file.write("\n")

                    if inicio == "OK":
                        ocioso = False
                    time.sleep(1)
            else:
                ocioso = False
        
        if ocioso == False:
            data = b''
            send_type2(com1)
            with open("Server5.txt", "a") as file:
                msg = str(datetime.now()) + ' / ' + 'envio / ' + str(2) + ' / ' + str(18)
                file.write(msg)   
                file.write("\n")
            cont = 1
            recebimento = True
            while recebimento:
                if cont <= numPckg:
                    timer1 = time.time()
                    timer2 = time.time()
                    transfer_type = com1.getData(1)
                    tentativa_recebimento = True
                    while tentativa_recebimento:
                        if transfer_type[0] == b'\x03':
                            inicio, idPack, payload, tamPckg  = receive_type3(com1)
                            with open("Server5.txt", "a") as file:
                                msg = str(datetime.now()) + ' / ' + 'receb / ' + str(int.from_bytes(transfer_type[0], byteorder='big')) + ' / ' + str(tamPckg+1) + ' / ' + str(idPack) + ' / ' + str(numPckg)
                                file.write(msg)  
                                file.write("\n") 
                            if inicio == 'OK':
                                if idPack == cont:
                                    send_type4(com1, cont)
                                    with open("Server5.txt", "a") as file:
                                        msg = str(datetime.now()) + ' / ' + 'envio / ' + str(4) + ' / ' + str(18)
                                        file.write(msg)   
                                        file.write("\n")
                                    cont += 1
                                    data += payload
                                    #print('PACOTE {} RECEBIDO'.format(idPack))
                                else:
                                    send_type6(com1, idPack)
                                    #print('MANDOU TIPO 6')
                                    with open("Server5.txt", "a") as file:
                                        msg = str(datetime.now()) + ' / ' + 'envio / ' + str(6) + ' / ' + str(18)
                                        file.write(msg)   
                                        file.write("\n")
                            else:
                                send_type6(com1, idPack)
                                #print('MANDOU TIPO 6')
                                with open("Server5.txt", "a") as file:
                                    msg = str(datetime.now()) + ' / ' + 'envio / ' + str(6) + ' / ' + str(18)
                                    file.write(msg)   
                                    file.write("\n")

                            tentativa_recebimento = False
                            continue
                        else:
                            com1.rx.clearBuffer()
                            time.sleep(1)
                            if time.time()-timer2 > 20:
                                ocioso = True
                                send_type5(com1)
                                with open("Server5.txt", "a") as file:
                                    msg = str(datetime.now()) + ' / ' + 'envio / ' + str(5) + ' / ' + str(18)
                                    file.write(msg) 
                                    file.write("\n")

                                recebimento = False
                                tentativa_recebimento = False
                                continue
                            else:
                                if time.time()-timer1 > 2:
                                    send_type6(com1, cont)
                                    with open("Server5.txt", "a") as file:
                                        msg = str(datetime.now()) + ' / ' + 'envio / ' + str(6) + ' / ' + str(18)
                                        file.write(msg)
                                        file.write("\n")

                                    timer1 = time.time()
                                    transfer_type = com1.getData(1)

                else:
                    recebimento = False
        try:   
            image = Image.open(io.BytesIO(np.asarray(data)))
            image.save('imagemRecebida.jpg')    
        except:
            pass
        com1.disable()

    except Exception as e:
        print("ops! :-\\")
        print(e)
        print(traceback.format_exc())
        com1.disable()

if __name__ == "__main__":
    main()
