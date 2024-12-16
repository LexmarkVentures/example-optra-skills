import cv2
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--usb_camera_id', type=int, default=0)
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.usb_camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    while True:
        ret, frame = cap.read()
        cv2.imshow('USB Camera', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()