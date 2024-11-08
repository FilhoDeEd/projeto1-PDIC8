import cv2
import numpy as np
import constants as c
from typing import Literal

#Configuração do Simple Blob Detector
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 1000
params.maxArea = 1000000
params.filterByCircularity = True
params.minCircularity = 0.3
params.filterByConvexity = False
params.filterByInertia = False
detector = cv2.SimpleBlobDetector_create(params)


def to_hsv(frame:cv2.typing.MatLike) -> cv2.typing.MatLike:
    '''
        Convert frame in HSV colors
    '''
    return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

def filter_red(frame:cv2.typing.MatLike) -> cv2.typing.MatLike:
    '''
        Clips all colors but red defined in HSV min and max values set in constants.py
    '''
    return cv2.inRange(frame, np.array(list(c.min.values())), np.array(list(c.max.values())))   

def crop_frame(frame:cv2.typing.MatLike) -> cv2.typing.MatLike:
    '''
        Crop the frame on the dimensions set in constants.py
    '''
    return frame[c.top_left[1]:c.bottom_right[1], c.top_left[0]:c.bottom_right[0]]
     
def apply_mask(frame:cv2.typing.MatLike, mask:cv2.typing.MatLike) -> cv2.typing.MatLike:
    '''
        Apply the mask in the frame
    '''
    return cv2.bitwise_and(frame, frame, mask=mask)
     
def drawKeypoints(frame: cv2.typing.MatLike, keypoints: list[cv2.KeyPoint]) -> cv2.typing.MatLike:
    '''
    Draw the circles in the frame where keypoints were found
    '''
    return cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 255, 255),
                                             cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
def red_or_black(frame:cv2.typing.MatLike, red_threshold:float) -> Literal['red', 'black']:
    '''
    Returns if color is red or black
    '''
    hsv = to_hsv(frame)     #convertendo para hsv
    red_mask = filter_red(hsv)     #criando mascara para apenas mostrar os vermelhos definidos
    frame_color_filtered = apply_mask(frame,red_mask)     #aplicando mascara no frame
    croped_frame_filtered = crop_frame(frame_color_filtered)    #recortando o frame para apenas computar a parte que interessa no cálculo da média (onde o retângulo sinaliza)
    if np.mean(croped_frame_filtered) > red_threshold: #    caso a média for maior do que foi definido empiricamente: VERMELHO, se não, é PRETA   
        return 'red'
    else:
        return 'black'

def number_of_card(frame: cv2.typing.MatLike, mask: cv2.typing.MatLike) -> tuple[int, list[cv2.KeyPoint]]:
    '''
    Returns number of the card and where the symbols where found in the image
    '''
    frame_masked = np.where(mask==255, frame, mask) # Achar um nome melhor
    keypoints = detector.detect(frame_masked)

    i = 0
    sum = 0
    for keypoint in keypoints:
        i += 1
        # Calcula a circularidade para cada keypoint
        diameter = keypoint.size
        radius = diameter / 2
        area = np.pi * (radius ** 2)
        perimeter = np.pi * diameter

        # Circularidade
        sum += diameter

    if i != 0:
        print(sum/i)
    #Somatória de blobs na tela
    blobs_sum = 0
    #Contador
    count = 0
    count += 1
    blobs_count = len(keypoints) - 2
    blobs_sum += blobs_count
    card_number = round(blobs_sum/count)
    if count >= 50:
        count = 0
        blobs_sum = 0
    return card_number, keypoints

def draw_rectangle(frame:cv2.typing.MatLike) -> None:
    '''
    Draws retangle with text "Posicione a carta aqui" above
    '''
    cv2.rectangle(frame, c.top_left, c.bottom_right, (0, 255, 0), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Posicione a carta aqui", c.text_position, font, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
