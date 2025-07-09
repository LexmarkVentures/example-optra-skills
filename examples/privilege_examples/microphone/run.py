import subprocess
import numpy as np
import select

def get_volume_level(audio):
    if len(audio) == 0:
        return -100
    sq_amplitude = audio.astype(np.float32)**2
    mean_squared_amplitude = np.mean(sq_amplitude)
    if mean_squared_amplitude <= 0:
        return -100
    decibels = 10 * np.log10(mean_squared_amplitude / (32768.0**2))
    return decibels

def VZ61k_mic_setup():
    subprocess.run(
        ["amixer", "-c2", "cset", "name='DAI-TLV Mic PGA Capture Volume'", "5"]
    )
    subprocess.run(
        ["amixer", "-c2", "cset", "name='DAI-TLV ADC Capture Volume'", "64"]
    )
    subprocess.run(
        ["amixer", "-c2", "cset", "name='DAI-TLV MIC1RP P-Terminal'", "0"]
    )
    subprocess.run(
        ["amixer", "-c2", "cset", "name='DAI-TLV MIC1LP P-Terminal'", "1"]
    )
    subprocess.run(
        ["amixer", "-c2", "cset", "name='DAI-TLV MIC1LM P-Terminal'", "0"]
    )
    subprocess.run(
        ["amixer", "-c2", "cset", "name='DAI-TLV MIC1LM M-Terminal'", "0"]
    )

def main():
    format = "S16_LE"
    rate = 48000
    channels = 1
    device = "mic:CARD=APE,DEV=0"

    chunk_size = 4096
    buffer_duration = 0.1
    samples_per_buffer = int(rate * buffer_duration)
    bytes_per_buffer = samples_per_buffer * 2

    arecord_cmd = [
        "arecord",
        "-t", "raw",
        "-f", format,
        "-r", str(rate),
        "-c", str(channels),
        "-D", device,
        "--buffer-size", str(samples_per_buffer * 4),
        "--period-size", str(samples_per_buffer // 4),
    ]

    # uncomment the following line to set up the VZ61k microphone
    #VZ61k_mic_setup()

    try:
        print("Starting audio stream...")
        process = subprocess.Popen(arecord_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        audio_buffer = b""

        while True:
            ready, _, _ = select.select([process.stdout], [], [], 0.001)

            if ready:
                try:
                    data = process.stdout.read(chunk_size)
                    if not data:
                        break

                    audio_buffer += data

                    if len(audio_buffer) >= bytes_per_buffer:
                        process_data = audio_buffer[:bytes_per_buffer]
                        audio_buffer = audio_buffer[bytes_per_buffer:]

                        audio = np.frombuffer(process_data, dtype=np.int16)

                        volume_level = get_volume_level(audio)
                        bar_length = max(0, min(30, int((volume_level + 60) / 2)))
                        bar = "#" * bar_length + "-" * (30 - bar_length)
                        print(f"Volume Level: {volume_level:.2f} dB | [{bar}]")

                except Exception as e:
                    print(f"Error reading audio: {e}")
                    break

            if process.poll() is not None:
                stderr_output = process.stderr.read().decode()
                if stderr_output:
                    print(f"arecord error: {stderr_output}")
                break

    except KeyboardInterrupt:
        print("\nStopping audio stream...")
    finally:
        if process:
            process.terminate()
            process.wait()

if __name__ == '__main__':
    main()