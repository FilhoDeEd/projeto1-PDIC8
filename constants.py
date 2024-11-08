
#Tamanho da tela (HD)
width, height = (1280, 720)

#Nome da tela
preview_name = 'Cards Detector'

#Posição que carta deverá estar na tela, também onde o retângulo será posicionado e todos os filtros serão computados
top_left = (width // 2 - 150, height // 2 - 225)
bottom_right = (width // 2 + 150, height // 2 + 225)
text_position = (width // 2 - 150, height // 2 - 250)

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