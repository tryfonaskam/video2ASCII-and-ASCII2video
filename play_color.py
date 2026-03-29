import pygame
import sys
import time

PIXEL_SIZE = 1

def load_frames(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    raw_frames = content.split('--- FRAME')
    frames = []
    for raw in raw_frames[1:]:
        lines = raw.splitlines()[1:]  # skip the frame number line
        parsed_rows = []
        for line in lines:
            if not line.strip():
                continue
            cells = line.split('|')
            parsed_row = []
            for cell in cells:
                if not cell:
                    continue
                char = cell[0]                      # first character is the symbol
                r, g, b = map(int, cell[1:].split(','))  # rest is R,G,B
                parsed_row.append((char, (r, g, b)))
            if parsed_row:
                parsed_rows.append(parsed_row)
        frames.append(parsed_rows)
    return frames

def play_ascii_frames(frames, fps=30):
    height = len(frames[0])
    width = len(frames[0][0])
    frame_pixel_width = width * PIXEL_SIZE
    frame_pixel_height = height * PIXEL_SIZE

    pygame.init()
    screen = pygame.display.set_mode((512, 512), pygame.RESIZABLE)
    pygame.display.set_caption("ASCII Video Player")
    clock = pygame.time.Clock()

    for frame in frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        win_w, win_h = screen.get_size()
        offset_x = (win_w - frame_pixel_width) // 2
        offset_y = (win_h - frame_pixel_height) // 2

        screen.fill((0, 0, 0))

        for y, row in enumerate(frame):
            for x, (char, color) in enumerate(row):
                rect = pygame.Rect(
                    offset_x + x * PIXEL_SIZE,
                    offset_y + y * PIXEL_SIZE,
                    PIXEL_SIZE,
                    PIXEL_SIZE
                )
                pygame.draw.rect(screen, color, rect)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    file_path = "output_color.txt"
    frames = load_frames(file_path)
    play_ascii_frames(frames, fps=30)
    time.sleep(203.4)
    print("Playback finished.")