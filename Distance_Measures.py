import time
import numpy as np
import cv2
import cv2.aruco as aruco
import numpy as np

#Cambiar las rutas por las nuestras
GENERAL_PATH = '/home/pol/Escritorio/TFG_2019-2020/Bibliotecas/'
ROBOBO_PATH = GENERAL_PATH+'robobo.py-master'
STREAMING_PATH = GENERAL_PATH+'robobo-python-video-stream-master/robobo_video'
import sys
sys.path.append(ROBOBO_PATH)
from Robobo import Robobo
from utils.Tag import Tag
sys.path.append(STREAMING_PATH)
from robobo_video import RoboboVideo

#Cambiar la IP por la nuestra
IP = '192.168.0.17'
rob = Robobo(IP)
rob.connect()
rob.moveTiltTo(80,70)
video = RoboboVideo(IP)
video.connect()

def Draw_Arucos(test, cord1,cord2,cord3,cord4,ids):
    '''
    Pinta el ArUco detectado junto su ID
    Recibe la imagen, las 4 coordenadas del marcador y su ID
    '''
    try:
        # Crear una polinea cerrada usando un array formado por las 4 coordenadas (x,y) de las esquinas del ArUco
        pts = np.array(((cord1['x'],cord1['y']),(cord2['x'],cord2['y']),(cord3['x'],cord3['y']),(cord4['x'],cord4['y'])))
        cv2.polylines(test,[pts],True,(0,255,0), thickness= 2)
        #Pinta el Id cerca de las coordenadas de la esquina 1 del tag
        x,y = int(cord1['x']), int(cord1['y'])
        cv2.putText(test,str(ids),(x,y+20), 1,1, color= (0,0,255),thickness= 1)
                
    except  IndexError:
        pass

    return test


def Distance_Measures(factor=1.3):
    '''
    Pinta y muestra por pantalla la distancia del ArUco a la cámara
    a partir del método de detección de tags de Robobo
    '''
    #Obtengo la imagen del streaming
    image = video.getImage()
    #Saco la altura y la anchura de la imagen
    height, width, _ = image.shape
    
    while True:
        #Obtenemos la imagen del streaming
        image = video.getImage() 
        #Llamamos al método lector de ArUcos
        tag = rob.readTag()     
        #De forma opcional podemos pintar el ArUco detectado junto a su ID
        Draw_Arucos(image,tag.cor1, tag.cor2, tag.cor3, tag.cor4, tag.id )
        #La distancia de la cámara al ArUco es el componente 'z' del vector de traslación pasado a centímetros
        # y multiplicado por un factor obtenido de forma experimental
        value = (tag.tvecs['z']/10)*factor
        #Se muestra dicho valor por pantalla y se pinta en la imagen
        print(f'Distance:{value}\n')
        cv2.putText(image,f'Distance:{round(value,2)} cm', (int(width/2)-100,50),cv2.FONT_HERSHEY_SIMPLEX,0.7, (0,0,255))     
        #Se muestra por pantalla la imagen pintada
        cv2.imshow("Frame", image)
        #Si se pulsa la tecla 'q' finaliza el script
        if cv2.waitKey(1) & 0xFF == ord("q"):
            video.disconnect()
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    Distance_Measures()
