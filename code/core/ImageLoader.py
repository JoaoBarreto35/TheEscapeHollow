import pygame


def load_player_spritesheet(path, scale=1):
    sheet = pygame.image.load(path).convert()

    # Pega a cor do pixel no canto superior esquerdo
    colorkey = sheet.get_at((0, 0))
    sheet.set_colorkey(colorkey)

    sheet_width, sheet_height = sheet.get_size()
    frame_count = 6
    frame_width = sheet_width // frame_count
    frame_height = sheet_height

    frames = []
    for i in range(frame_count):
        x = i * frame_width
        frame = sheet.subsurface(pygame.Rect(x, 0, frame_width, frame_height))

        # Aplica escala se necessário
        if scale != 1:
            frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))

        frames.append(frame)

    animations = {
        "down": [frames[0], frames[1]],
        "up": [frames[2], frames[3]],
        "right": [frames[4], frames[5]],
        "left": [
            pygame.transform.flip(frames[4], True, False),
            pygame.transform.flip(frames[5], True, False)
        ]
    }

    return animations