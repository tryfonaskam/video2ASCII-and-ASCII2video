import pygame
import sys
import time

# Map ASCII characters to colors
CHAR_COLOR = {
    '-': (0, 0, 0),      # black / dark
    '=': (85, 85, 85),   # dark gray
    '+': (170, 170, 170),# light gray
    '_': (255, 255, 255) # white / bright
}

PIXEL_SIZE = 1  # size of each "pixel" on screen

def load_frames(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Split by frames
    raw_frames = content.split('--- FRAME')
    frames = []
    for raw in raw_frames[1:]:  # skip first empty split
        lines = raw.splitlines()[1:]  # remove frame number line
        frames.append(lines)
    return frames

def play_ascii_frames(frames, fps=10):
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

        # Recalculate center offset every frame (handles window resizing)
        win_w, win_h = screen.get_size()
        offset_x = (win_w - frame_pixel_width) // 2
        offset_y = (win_h - frame_pixel_height) // 2

        screen.fill((0, 0, 0))  # Clear screen each frame

        for y, line in enumerate(frame):
            for x, char in enumerate(line):
                color = CHAR_COLOR.get(char, (0, 0, 0))
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
    file_path = "output_BnW.txt" #input("Enter ASCII .txt file: ").strip()
    frames = load_frames(file_path)
    play_ascii_frames(frames, fps=30)  # adjust fps as needed
    time.sleep(203.4)
    print("Playback finished.")