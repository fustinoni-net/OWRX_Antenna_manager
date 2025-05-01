import logging
import signal
import uvicorn
from fastapi import Request
from pydantic import BaseModel

from antenna_manager import AntennaManager
from antenna_system import DummyAntennaSystem
# from esp_home_one_relay_antenna_system import esp_home_one_relay_antenna_system

logging.basicConfig(level=logging.INFO)

class AntennaRequest(BaseModel):
    antenna_id: str

antenna_system = DummyAntennaSystem()
# antenna_system = esp_home_one_relay_antenna_system

with antenna_system:
    app = AntennaManager(antenna_system)

    @app.post("/setAntenna")
    async def set_antenna(request: AntennaRequest):
        logging.info(f"AntennaManager: Received switch state change request: {request.antenna_id}")
        return app.set_used_antenna_by_id(request.antenna_id)


    @app.get("/getAntennas")
    async def get_antennas():
        """
        Return a json with the antennas.
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