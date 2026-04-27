import os
import socket
import subprocess
import time

import cv2
import msgpack
import numpy as np

SOCKET_PATH          = "/tmp/inference_server.sock"
INFERENCE_SERVER_BIN = "/app/inference-server"
MODEL_PATH           = "/app/yolox_s.rknn"

CONF_THRESHOLD = 0.30
NMS_THRESHOLD  = 0.45

MODEL_WIDTH  = 640
MODEL_HEIGHT = 640

# COCO class labels (80 classes, YOLOX-S is trained on COCO)
COCO_LABELS = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
    "truck", "boat", "traffic light", "fire hydrant", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
    "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag",
    "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
    "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon",
    "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot",
    "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant",
    "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote",
    "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear",
    "hair drier", "toothbrush",
]

def start_inference_server() -> tuple[subprocess.Popen, socket.socket]:
    """Spawn the C++ inference server and connect to its Unix socket."""
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    process = subprocess.Popen([
        INFERENCE_SERVER_BIN,
        MODEL_PATH,
        str(CONF_THRESHOLD),
        str(NMS_THRESHOLD),
    ])

    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    for attempt in range(10):
        try:
            client.connect(SOCKET_PATH)
            print("Connected to inference server")
            return process, client
        except (ConnectionRefusedError, FileNotFoundError):
            print(f"Waiting for inference server... ({attempt + 1}/10)")
            time.sleep(1)

    process.terminate()
    raise RuntimeError("Could not connect to inference server after 10 attempts")


def send_frame(client: socket.socket, frame_bytes: bytes) -> list[dict]:
    """Send a raw frame to the C++ server and return parsed detections."""
    total_sent = 0
    while total_sent < len(frame_bytes):
        sent = client.send(frame_bytes[total_sent:])
        if sent == 0:
            raise RuntimeError("Socket connection broken")
        total_sent += sent

    # Read until we have a complete msgpack message
    response = b""
    while True:
        chunk = client.recv(1024)
        response += chunk
        try:
            response_dict = msgpack.unpackb(response)
            break
        except Exception:
            continue
    results = []
    for result in response_dict["results"]:
        results.append({
            b"x1": result["x1"],
            b"y1": result["y1"],
            b"x2": result["x2"],
            b"y2": result["y2"],
            b"conf": result["conf"],
            b"cls": result["cls"],
        })
    return results


def open_camera() -> cv2.VideoCapture:
    for i in range(12):
        cap = cv2.VideoCapture(i)
        try:
            if cap.isOpened() and cap.read()[0]:
                return cap
        except Exception:
            pass
        cap.release()
    raise RuntimeError("No camera found")


def draw_detections(
    frame: np.ndarray,
    detections: list[dict],
    scale_x: float,
    scale_y: float,
) -> None:
    for det in detections:
        x1   = int(det[b"x1"] * scale_x)
        y1   = int(det[b"y1"] * scale_y)
        x2   = int(det[b"x2"] * scale_x)
        y2   = int(det[b"y2"] * scale_y)
        conf = float(det[b"conf"])
        cls  = int(det[b"cls"])

        label = COCO_LABELS[cls] if cls < len(COCO_LABELS) else str(cls)
        print(f"  {label} ({conf:.2f})  [{x1},{y1}] → [{x2},{y2}]", flush=True)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"{label}: {conf:.2f}",
            (x1, max(y1 - 8, 0)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main() -> None:
    process, client = start_inference_server()
    cap = open_camera()

    cam_width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cam_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    scale_x    = cam_width  / MODEL_WIDTH
    scale_y    = cam_height / MODEL_HEIGHT

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame from camera", flush=True)
                break

            # Pre-process: resize to model input, flatten to bytes
            infer_frame  = cv2.resize(frame, (MODEL_WIDTH, MODEL_HEIGHT))
            frame_bytes  = np.expand_dims(infer_frame, axis=0).tobytes()

            # Infer
            detections = send_frame(client, frame_bytes)

            # Print detections
            if detections:
                print(f"Detections ({len(detections)}):", flush=True)
            draw_detections(frame, detections, scale_x, scale_y)

            cv2.imshow("RKNN Inference", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        client.close()
        process.terminate()
        process.wait()


if __name__ == "__main__":
    main()
