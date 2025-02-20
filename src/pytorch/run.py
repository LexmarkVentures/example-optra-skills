import torch
import torchvision
import torchvision.transforms as T
import cv2

def get_usb_camera_id():
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            camera_id = i
            cap.release()
            return camera_id
    return None

def main():
    camera_id = get_usb_camera_id()
    if camera_id is None:
        print('USB Camera not found')
        return

    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    device = torch.device('cuda')
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights=torchvision.models.detection.FasterRCNN_ResNet50_FPN_Weights.DEFAULT)
    coco_labels = torchvision.models.detection.FasterRCNN_ResNet50_FPN_Weights.DEFAULT.meta["categories"]

    model.to(device)
    model.eval()

    transform = T.Compose([
        T.ToTensor(),
    ])

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_tensor = transform(frame).unsqueeze(0).to(device)

        with torch.no_grad():
            results = model(frame_tensor)

        for idx, box in enumerate(results[0]['boxes']):
            score = results[0]['scores'][idx].item()
            if score > 0.8:
                xmin, ymin, xmax, ymax = map(int, box)
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                label = results[0]['labels'][idx].item()
                label_name = coco_labels[label]
                cv2.putText(frame, f'{label_name}: {score:.2f}', (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('PyTorch Demo', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()