import cv2
import sys

# Character set (dark → bright), 14 chars
CHARS = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=']

WIDTH = 16
HEIGHT = 16

def print_progress(current, total, bar_length=40):
    percent = float(current) / total
    filled_length = int(bar_length * percent)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rProgress: |{bar}| {percent*100:.1f}% ({current}/{total} frames)')
    sys.stdout.flush()
    if current == total:
        print()

def pixel_to_char(brightness):
    index = int(brightness / 256 * len(CHARS))
    return CHARS[min(index, len(CHARS) - 1)]

def frame_to_ascii_rgb(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized_gray = cv2.resize(gray, (WIDTH, HEIGHT))
    resized_bgr = cv2.resize(frame, (WIDTH, HEIGHT))

    rows = []
    for y in range(HEIGHT):
        cells = []
        for x in range(WIDTH):
            brightness = resized_gray[y, x]
            char = pixel_to_char(brightness)

            b, g, r = resized_bgr[y, x]  # OpenCV is BGR
            cells.append(f"{char}{r},{g},{b}")  # e.g. "!255,0,128"

        rows.append("|".join(cells))  # pipe-separated cells per row

    return "\n".join(rows)

def convert_color(input_video, output_file, frame_skip=1):
    cap = cv2.VideoCapture(input_video)

    if not cap.isOpened():
        print("Error opening video file")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    with open(output_file, "w", encoding="utf-8") as f:
        frame_count = 0
        saved_frames = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_skip == 0:
                ascii_frame = frame_to_ascii_rgb(frame)
                f.write(f"\n--- FRAME {saved_frames} ---\n")
                f.write(ascii_frame)
                f.write("\n")
                saved_frames += 1

            print_progress(frame_count + 1, total_frames)
            frame_count += 1

    cap.release()
    print(f"Done! {saved_frames} frames written.")
    print(f"Original FPS: {fps}")

convert_color("colore.mp4", "output_color.txt", frame_skip=2)