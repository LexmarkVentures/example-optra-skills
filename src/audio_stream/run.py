import subprocess
import wave
import numpy as np

def main():
    format = "S16_LE"
    rate = 48000
    channels = 1
    device = "mic:CARD=APE,DEV=0"
    chunk = 1024
    record_time = 10
    arecord_cmd = [
        "arecord",
        "-t", "raw",
        "-f", format,
        "-r", str(rate),
        "-c", str(channels),
        "-D", device,
    ]

    try:
        recording_num = 0
        process = subprocess.Popen(arecord_cmd, stdout=subprocess.PIPE)
        while True:
            print(f"Recording {recording_num}...")
            data = b""
            for i in range(0, int(rate * record_time / chunk * 2)):
                data += process.stdout.read(chunk)
            audio = np.frombuffer(data, dtype=np.int16)

            file_path = f"/app/outputs/output{recording_num}.wav"
            with wave.open(file_path, "wb") as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(2)
                wf.setframerate(rate)
                wf.writeframes(b''.join(audio))

            recording_num += 1
            print(f"Audio saved to file: {file_path}")

    except KeyboardInterrupt:
        process.kill()

if __name__ == '__main__':
    main()