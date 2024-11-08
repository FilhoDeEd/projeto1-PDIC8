from pprint import pprint
import cv2
import numpy as np

preview_name = 'Cards Detector'
width, height = (1280, 720)

top_left = (width // 2 - 150, height // 2 - 225)
bottom_right = (width // 2 + 150, height // 2 + 225)
text_position = (width // 2 - 150, height // 2 - 250)
font = cv2.FONT_HERSHEY_SIMPLEX

cv2.namedWindow(preview_name)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro ao abrir a webcam")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

rectagle_mask = np.zeros((height, width, 3), dtype=np.uint8)
rectagle_mask = cv2.rectangle(rectagle_mask, top_left, bottom_right, (255, 255, 255), -1)

# Filtro HSV ajustado para vermelho
min = {
    'hue': 100,
    'saturation': 21,
    'value': 62
}

max = {
    'hue': 179,
    'saturation': 211,
    'value': 255
}

red_threshold = 6.0

blobs_sum = 0
count = 0

params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 1000
params.maxArea = 1000000
params.filterByCircularity = True
params.minCircularity = 0.3
params.filterByConvexity = False
params.filterByInertia = False
detector = cv2.SimpleBlobDetector_create(params)

lower_bound = np.array([0, 0, 0], dtype=np.uint8)
upper_bound = np.array([180, 180, 180], dtype=np.uint8)


while True:
    ret, frame = cap.read()
    if not ret:
        print("Falha na captura de imagem")
        break

    # Detectando a cor da carta
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv, np.array(list(min.values())), np.array(list(max.values())))
    frame_color_filtered = cv2.bitwise_and(frame, frame, mask=red_mask)

    croped_frame_filtered = frame_color_filtered[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    if np.mean(croped_frame_filtered) > red_threshold:
        color = 'red'
    else:
        color = 'black'

    # Contando o número de símbolos na carta
    frame_masked = np.where(rectagle_mask==255, frame, rectagle_mask) # Achar um nome melhor
    keypoints = detector.detect(frame_masked)

    # if len(keypoints) != 0:
    #     pprint(type(keypoints[0]))

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

    count += 1
    blobs_count = len(keypoints) - 2
    blobs_sum += blobs_count
    #print(round(blobs_sum/count))

    if count >= 50:
        count = 0
        blobs_sum = 0

    frame_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 255, 255),
                                            cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.rectangle(frame_with_keypoints, top_left, bottom_right, (0, 255, 0), 2)
    cv2.putText(frame_with_keypoints, "Posicione a carta aqui", text_position, font, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow(preview_name, frame_with_keypoints)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
