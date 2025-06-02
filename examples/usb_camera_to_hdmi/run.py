import cv2
import argparse

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
        cv2.imshow('USB Camera', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()