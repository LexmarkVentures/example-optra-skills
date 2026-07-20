import logging
import subprocess
from collections.abc import Mapping

from azure.iot.device import IoTHubModuleClient


def parse_models(value: object) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, str):
        raise ValueError("The 'models' skill input must be a comma-separated string.")
    return [model.strip() for model in value.split(",") if model.strip()]


def get_models_from_twin(twin: Mapping[str, object]) -> list[str]:
    desired = twin.get("desired", {})
    if not isinstance(desired, Mapping):
        raise ValueError("The IoT twin desired properties must be an object.")

    inputs = desired.get("inputs", {})
    if not isinstance(inputs, Mapping):
        raise ValueError("The IoT twin desired inputs must be an object.")

    return parse_models(inputs.get("models"))


def pull_models(models: list[str]) -> None:
    if not models:
        logging.warning("No models configured in the 'models' skill input.")
        return

    for model in models:
        logging.info("Pulling Ollama model: %s", model)
        subprocess.run(["ollama", "pull", model], check=True)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    client = IoTHubModuleClient.create_from_edge_environment(websockets=True)
    pull_models(get_models_from_twin(client.get_twin()))


if __name__ == "__main__":
    main()
