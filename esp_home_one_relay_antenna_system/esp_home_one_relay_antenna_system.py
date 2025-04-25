import logging
import os
import paho.mqtt.client as mqtt

from antenna_system import AntennaSystem

# MQTT settings from environment variables
MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL')
MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT', 1883))
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')

# MQTT topics
MQTT_TOPIC_SWITCH_STATE = "antenna-switch/switch/antenna_switch_1_2/state"
MQTT_TOPIC_SWITCH_COMMAND = "antenna-switch/switch/antenna_switch_1_2/command"
# MQTT payloads
MQTT_PAYLOAD_SWITCH_ON = "ON"
MQTT_PAYLOAD_SWITCH_OFF = "OFF"

# Other possible topics and values
# antenna-switch/status offline
# box/status online
# antenna-switch/switch/controllato_da_owrx/state ON


class EspHomeOneRelayAntennaSystem(AntennaSystem):
    def __init__(self, broker_url, broker_port, username, password):
        super().__init__()

        self.broker_url = broker_url
        self.broker_port = broker_port
        self.username = username
        self.password = password
        self.mqtt_client = mqtt.Client(client_id="EspHomeOneRelayAntennaSystem", protocol=mqtt.MQTTv311)
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_message = self._on_message

        self.antennas = [
            self.Antenna(name="windom 40/80", antenna_id='1'),
            self.Antenna(name="vert 11m 1/4λ", antenna_id='2'),
        ]


    def __enter__(self):
        self.mqtt_client.username_pw_set(self.username, self.password)

        self.mqtt_client.connect(self.broker_url, self.broker_port, 60)
        self.mqtt_client.loop_start()
        self._current_antenna = self.antennas[0]  # Default to the first antenna
        logging.info(f"EspHomeOneRelayAntennaSystem: Connected to MQTT broker at {self.broker_url}:{self.broker_port}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
        logging.info(f"EspHomeOneRelayAntennaSystem: Disconnected from MQTT broker")


    @staticmethod
    def _on_connect( client, userdata, flags, rc):
        logging.info(f"EspHomeOneRelayAntennaSystem: Connected to MQTT broker with result code {rc}")
        client.subscribe(MQTT_TOPIC_SWITCH_STATE)

    def _on_message(self, client, userdata, msg):
        latest_message = msg.payload.decode()
        logging.info(f"EspHomeOneRelayAntennaSystem: Received message: {latest_message}")
        # Broadcast the message to all connected clients
        self._current_antenna = self.antennas[1] if latest_message == "ON" else self.antennas[0]
        self._notify_antenna_change(self._current_antenna)


    def get_available_antennas(self) -> list[AntennaSystem.Antenna]:
        return self.antennas


    def set_default_antenna(self) -> None:
        self.set_used_antenna(self.antennas[0]) # Default to the first antenna
        logging.info("EspHomeOneRelayAntennaSystem: Default antenna set to: %s", self.antennas[0].name)

    def get_used_antenna(self) -> AntennaSystem.Antenna:
        return self._current_antenna

    def set_antenna_change_listener(self, antenna_has_changed: callable) -> None:
        self.antenna_listener.append(antenna_has_changed)

    def _switch_antenna(self, antenna: AntennaSystem.Antenna):
        logging.log(logging.INFO, f"EspHomeOneRelayAntennaSystem: Switching to antenna: {antenna.name}")
        if antenna == self.antennas[0]:
            i: mqtt.MQTTMessageInfo = self.mqtt_client.publish(MQTT_TOPIC_SWITCH_COMMAND, MQTT_PAYLOAD_SWITCH_OFF)
            logging.info(i)
        elif antenna == self.antennas[1]:
            i: mqtt.MQTTMessageInfo = self.mqtt_client.publish(MQTT_TOPIC_SWITCH_COMMAND, MQTT_PAYLOAD_SWITCH_ON)
            logging.info(i)
        else:
            raise ValueError("Antenna not available in the system.")


esp_home_one_relay_antenna_system = EspHomeOneRelayAntennaSystem(MQTT_BROKER_URL, MQTT_BROKER_PORT, MQTT_USERNAME, MQTT_PASSWORD)