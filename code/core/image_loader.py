import pygame

_image_cache = {}

def load_image(path, size=None):
    if path in _image_cache:
        return _image_cache[path]

    try:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        _image_cache[path] = image
        return image
    except Exception as e:
        print(f"[ImageLoader] Erro ao carregar imagem: {path} → {e}")
        fallback = pygame.Surface((64, 64))
        fallback.fill((255, 0, 0))
        return fallback

def load_spritesheet(path, frame_count, scale=1, directional=True):
    sheet = pygame.image.load(path).convert()
    colorkey = sheet.get_at((0, 0))
    sheet.set_colorkey(colorkey)

    sheet_width, sheet_height = sheet.get_size()
    frame_width = sheet_width // frame_count
    frame_height = sheet_height

    frames = []
    for i in range(frame_count):
        x = i * frame_width
        frame = sheet.subsurface(pygame.Rect(x, 0, frame_width, frame_height))
        if scale != 1:
            frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
        frames.append(frame)

    if directional:
        return {
            "down": [frames[0], frames[1]],
            "up": [frames[2], frames[3]],
            "right": [frames[4], frames[5]],
            "left": [
                pygame.transform.flip(frames[4], True, False),
                pygame.transform.flip(frames[5], True, False)
            ]
        }
    else:
        return frames