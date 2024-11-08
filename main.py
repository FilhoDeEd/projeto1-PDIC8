import cv2
import constants as c
from functions import *

###########################################################################
#Threshold do filtro vermelho
red_threshold = 6.0

#Máscara de Zeros do tamanho da tela
rectagle_mask = np.zeros((c.height, c.width, 3), dtype=np.uint8)
#Retângulo com o tamanho da área que queremos computar
rectagle_mask = cv2.rectangle(rectagle_mask, c.top_left, c.bottom_right, (255, 255, 255), -1)

lower_bound = np.array([0, 0, 0], dtype=np.uint8)
upper_bound = np.array([180, 180, 180], dtype=np.uint8)
#############################################################################

#Nome da janela
cv2.namedWindow(c.preview_name)

# Configurando Captura
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro ao abrir a webcam")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, c.width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, c.height)

# Começo
while True:
    ret, frame = cap.read()
    if not ret:
        print("Falha na captura de imagem")
        break

    # Detectando a cor da carta
    card_color = red_or_black(frame, red_threshold)

    # Contando o número de símbolos na carta
    card_value, keypoints = number_of_card(frame, rectagle_mask)

    # Desenhando os keypoints encontrados pelo simple blob detector
    frame_with_keypoints = drawKeypoints(frame, keypoints)

    # Desenhando o retângulo onde pede a carta
    draw_rectangle(frame_with_keypoints)
    
    # Mostra a câmera
    cv2.imshow(c.preview_name, frame_with_keypoints)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
