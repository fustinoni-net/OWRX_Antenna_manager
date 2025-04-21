import json
import logging
import asyncio
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from antenna_system import AntennaSystem


class AntennaManager(FastAPI):

    def __init__(self, antenna_system: AntennaSystem=None):
        super().__init__()
        self.add_middleware( # CORS
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.active_connections_queues = []
        self.latest_message = None
        self.antenna_system = antenna_system

        # Mount the static files directory
        self.mount("/am-static", StaticFiles(directory="am-static"), name="am-static")
        # Set the antenna change listener
        self.antenna_system.set_antenna_change_listener(self.antennas_change_listener)
        # Set the default antenna
        self.antenna_system.set_default_antenna()

    def on_shutdown(self):
        logging.info("AntennaManager: Application is shutting down")
        self.antenna_system.set_default_antenna()

    def return_antennas(self) -> list[AntennaSystem.Antenna]:
        """
        Return a json with the antennas.
        """
        return self.antenna_system.get_available_antennas()

    def set_used_antenna(self, antenna: AntennaSystem.Antenna) -> None:
        """
        Set the used antenna.
        """
        self.antenna_system.set_used_antenna(antenna)
        logging.info(f"AntennaManager: Set used antenna: {antenna.name}")

    def set_used_antenna_by_id(self, antenna_id: str) :
        """
        Set the used antenna by ID.
        """
        try:
            antenna = list(filter( lambda a: a.id == antenna_id ,self.return_antennas()))[0]
            self.set_used_antenna(antenna)
            logging.info(f"AntennaManager: Switched to antenna: {antenna.name}")
            return "OK"
        except (IndexError, ValueError) as e:
            logging.error(f"AntennaManager: Invalid antenna ID: {antenna_id}. Error: {e}")
            return {"error": "Invalid antenna ID"}

    def antennas_change_listener(self, antenna: AntennaSystem.Antenna) -> None:
        self.latest_message = antenna
        logging.info(f"Received message: {self.latest_message}")
        # Broadcast the message to all connected clients
        for connection_queue in self.active_connections_queues:
            connection_queue.put_nowait(self.latest_message)

    async def _event_stream(self, request: Request, queue: asyncio.queues.Queue):
        try:
            # Send the latest message to the newly connected client
            if self.latest_message:
                yield f"data: {json.dumps(self.latest_message.to_dict())}\n\n"

            while True:
                if await request.is_disconnected():
                    logging.info("AntennaManager: Client disconnected")
                    break
                try:
                    message = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield f"data: {json.dumps(message.to_dict())}\n\n"
                except asyncio.TimeoutError:
                    # Send last message like a ping message if no other message was sent in the last 30 seconds
                    yield f"data: {json.dumps(self.latest_message.to_dict())}\n\n"
                    # yield f"data: ping\n\n"
                    logging.info("AntennaManager: Sent last message like ping to keep connection alive")
        except asyncio.CancelledError:
            logging.info("AntennaManager: Event stream cancelled")
            raise
        finally:
            if queue in self.active_connections_queues:
                self.active_connections_queues.remove(queue)
            logging.info(f"AntennaManager: Client disconnected, active connections: {len(self.active_connections_queues)}")
            if len(self.active_connections_queues) == 0:
                self.no_more_client_connected()
                self.antenna_system.set_default_antenna()


    async def antennas_events(self, request: Request):
        queue: asyncio.queues.Queue = asyncio.Queue()
        self.active_connections_queues.append(queue)
        logging.info(f"AntennaManager: Client connected, active connections: {len(self.active_connections_queues)}")


        response = StreamingResponse(self._event_stream(request, queue), media_type="text/event-stream")
        response.headers["Cache-Control"] = "no-cache"
        response.headers["X-Accel-Buffering"] = "no"
        return response

    def no_more_client_connected(self):
        logging.info("AntennaManager: No more clients connected")






