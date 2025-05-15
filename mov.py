import cv2
import time

def rgb_fg(r, g, b):
    return f"\x1b[38;2;{r};{g};{b}m"

def rgb_bg(r, g, b):
    return f"\x1b[48;2;{r};{g};{b}m"

def frame_to_ascii_block(frame, width=120):
    height, original_width = frame.shape[:2]
    aspect_ratio = original_width / height

    # 文字の縦横比を約0.5（文字は縦長）として縦文字数を計算
    char_height = int(width / aspect_ratio * 0.5)

    # ブロック文字は1文字で上下2ピクセルを表示するので高さは2倍にリサイズ
    resized = cv2.resize(frame, (width, char_height * 2))

    ascii_image = ""
    for y in range(0, resized.shape[0] - 1, 2):
        upper = resized[y]
        lower = resized[y + 1]
        for u_pixel, l_pixel in zip(upper, lower):
            r1, g1, b1 = u_pixel  # 上のピクセル色
            r2, g2, b2 = l_pixel  # 下のピクセル色
            # 色反転を直すため、fg=下ピクセル色、bg=上ピクセル色
            fg = rgb_fg(r2, g2, b2)
            bg = rgb_bg(r1, g1, b1)
            ascii_image += fg + bg + "▄" + "\x1b[0m"
        ascii_image += "\n"

    return ascii_image

def play_ascii_video(video_path, width=120):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    if not cap.isOpened():
        print("動画を開けません。")
        return

    print("\x1b[2J")  # 画面クリア

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            ascii_frame = frame_to_ascii_block(frame, width)
            print("\x1b[H" + ascii_frame, end="")
            time.sleep(1 / fps)
    finally:
        cap.release()

# 動画ファイル名を指定して実行
play_ascii_video("mov.mp4", width=120)
