# Ollama LLM Skill

This skill runs the native [Ollama](https://ollama.com/) API on an Optra Edge device. At startup, it reads the `models` skill input from the Azure IoT Hub module twin and downloads the requested models before serving requests on port `11434`.

## Supported Devices

The image uses NVIDIA JetPack 6 and the Ollama JetPack 6 runtime. Deploy it to a compatible NVIDIA-based Optra device with enough memory and disk space for each selected model. The device should be running 3.x or later firmware.

## How to Build

Run this command from this directory:

```sh
docker buildx build --platform linux/arm64 -t <registry>/ollama --push .
```

## Optra Portal Configuration

Create a Docker Image skill with the pushed image and configure:

| Setting | Value |
| --- | --- |
| Input key | `models` |
| Input label | `Ollama models` |
| Input value | Comma-separated Ollama model references, such as `llama3.2:3b,gemma3:4b` |
| Exposed port | Container port `11434`, mapped to the desired device port |
| Volume | A persistent volume mounted at `/app/storage` |

The skill reads the configured models only during startup. Sync or restart the skill after changing the `models` input. The persistent volume retains downloaded models across restarts.

## Using the API

Ollama is available on the port configured above. For example:

```sh
curl http://<device-host>:11434/api/generate \
  -d '{"model":"llama3.2:3b","prompt":"Why run models at the edge?","stream":false}'
```

## Required Privileges

* Port Binding:
  * Container port: 11434
  * Protocol: tcp
  * Host port: 11434
* Persistent volume mounted at `/app/storage`
