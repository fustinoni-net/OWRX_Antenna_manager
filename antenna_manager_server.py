import logging
import signal
import uvicorn
from fastapi import Request

from antenna_manager import AntennaManager
from antenna_system import DummyAntennaSystem

logging.basicConfig(level=logging.INFO)

app = AntennaManager(DummyAntennaSystem())

@app.post("/setAntenna/{antenna_id}")
async def set_antenna(antenna_id: str):
    logging.info(f"AntennaManager: Received switch state change request: {antenna_id}")
    return app.set_used_antenna_by_id(antenna_id)

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