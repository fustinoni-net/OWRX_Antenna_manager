# `esp_home_one_relay_antenna_system`

This package provides an implementation of an antenna system that integrates with ESPHome devices using MQTT. It allows managing antennas by switching between them and notifying changes through MQTT topics.

## Configuration Parameters

The package requires the following environment variables to configure the MQTT connection:

- `MQTT_BROKER_URL`: The URL of the MQTT broker.
- `MQTT_BROKER_PORT`: The port of the MQTT broker (default: `1883`).
- `MQTT_USERNAME`: The username for MQTT authentication (optional).
- `MQTT_PASSWORD`: The password for MQTT authentication (optional).

### Example Configuration

Set the environment variables in your system or `.env` file:

```env
MQTT_BROKER_URL=your-broker-url
MQTT_BROKER_PORT=your-broker-port
MQTT_USERNAME=your-username
MQTT_PASSWORD=your-password
```

## Usage in `antenna_manager_server`

To use the package in the `antenna_manager_server`, follow these steps:

1. Import the `esp_home_one_relay_antenna_system` package.
2. Replace the default `DummyAntennaSystem` with `esp_home_one_relay_antenna_system`.
3. Ensure the environment variables are properly set before running the server.

### Example Code

Below is an example of how to integrate the package into the `antenna_manager_server`:

```python
import logging
import signal
import uvicorn
from fastapi import Request
from pydantic import BaseModel

from antenna_manager import AntennaManager
from esp_home_one_relay_antenna_system import esp_home_one_relay_antenna_system

logging.basicConfig(level=logging.INFO)

class AntennaRequest(BaseModel):
    antenna_id: str

antenna_system = esp_home_one_relay_antenna_system

with antenna_system:
    app = AntennaManager(antenna_system)

    @app.post("/setAntenna")
    async def set_antenna(request: AntennaRequest):
        logging.info(f"AntennaManager: Received switch state change request: {request.antenna_id}")
        return app.set_used_antenna_by_id(request.antenna_id)

    @app.get("/getAntennas")
    async def get_antennas():
        """
        Return a JSON with the antennas.
        """
        antennas = app.return_antennas()
        return antennas

    @app.get("/antennasEvents")
    async def antennas_events(request: Request):
        return await app.antennas_events(request)

    if __name__ == "__main__":
        signal.signal(signal.SIGTERM, lambda sig, frame: app.on_shutdown())
        signal.signal(signal.SIGINT, lambda sig, frame: app.on_shutdown())
        uvicorn.run(app, host="0.0.0.0", port=8000)
```

This setup allows the `antenna_manager_server` to manage antennas using the ESPHome-based relay system.