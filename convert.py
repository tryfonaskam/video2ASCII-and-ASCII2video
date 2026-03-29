import cv2
import sys

# Character set (dark → bright)
CHARS = ['-', '=', '+', '_']

WIDTH = 16
HEIGHT = 16

def print_progress(current, total, bar_length=40):
    percent = float(current) / total
    filled_length = int(bar_length * percent)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rProgress: |{bar}| {percent*100:.1f}% ({current}/{total} frames)')
    sys.stdout.flush()
    if current == total:
        print()  # Newline at the end

def pixel_to_char(pixel):
    index = int(pixel / 256 * len(CHARS))
    return CHARS[min(index, len(CHARS) - 1)]

def frame_to_ascii(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (WIDTH, HEIGHT))

    ascii_frame = []
    for row in resized:
        line = "".join(pixel_to_char(pixel) for pixel in row)
        ascii_frame.append(line)

    return "\n".join(ascii_frame)



def video_to_ascii(input_video, output_file, frame_skip=1):
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

            # Skip frames to reduce size
            if frame_count % frame_skip == 0:
                ascii_frame = frame_to_ascii(frame)

                f.write(f"\n--- FRAME {saved_frames} ---\n")
                f.write(ascii_frame)
                f.write("\n")

                saved_frames += 1
            print_progress(frame_count + 1, total_frames)
            frame_count += 1

    cap.release()
    print(f"Done! {saved_frames} frames written.")
    print(f"Original FPS: {fps}")


# 🔧 Usage
video_to_ascii("BnW.mp4", "output_BnW.txt", frame_skip=2)