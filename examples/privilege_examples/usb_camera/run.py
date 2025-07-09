import cv2
import argparse

def frame_to_ascii(frame, width=150, height=45):
    ascii_chars = "@%#*+=-:. "

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (width, height))

    resized = cv2.normalize(resized, None, 0, 255, cv2.NORM_MINMAX)

    ascii_frame = []
    for row in resized:
        ascii_row = ""
        for pixel in row:
            char_index = int(int(pixel) * (len(ascii_chars) - 1) / 255)
            ascii_row += ascii_chars[char_index]
        ascii_frame.append(ascii_row)

    return ascii_frame

def get_usb_camera_id():
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            camera_id = i
            cap.release()
            return camera_id
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--usb_camera_id', type=int, default=None)
    args = parser.parse_args()

    if args.usb_camera_id is None:
        camera_id = get_usb_camera_id()
        if camera_id is None:
            print('USB Camera not found')
            return
    else:
        camera_id = args.usb_camera_id

    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    while True:
        ret, frame = cap.read()

        if ret:
            print(f"Frame Shape: {frame.shape}")

            ascii_art = frame_to_ascii(frame)
            for row in ascii_art:
                print(row)

            print("\n" + "=" * 160 + "\n")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()