# OWRX+ Antenna manager
Antenna manager for OpenWebRX+

## Overview
This software serves as a foundation for developing an antenna manager for OpenWebRX+. Its primary goals are:

- Enabling customization of the plugin and backend component (server) by simply extending a Python class (AntennaSystem).
- Providing seamless two-way communication between the backend and the plugin to keep the antenna usage information synchronized across all open pages.

The software consists of two main components: a server and a client.

- **Server**: Written in Python, it leverages the FastAPI framework to handle HTTP requests. It uses the Server-Sent Events (SSE) protocol to update the client with the current antenna in use in real time.

- **Client**: Developed in HTML and JavaScript, it includes a web interface for controlling the antenna manager, which is particularly useful during development and testing phases, as well as a plugin for OpenWebRX+.

**My sincere thanks go to Stanislav Lechev [0xAF] for his help in making the plugin.**


## Customizing the Application with Your Own `AntennaSystem`

This application is designed to be flexible and allows you to create your own `AntennaSystem` to meet your specific requirements. Below, we describe how to customize the application and use it effectively.

### Creating Your Own `AntennaSystem`

To create a custom `AntennaSystem`, follow these steps:

1. **Extend the `AntennaSystem` Class**  
   Create a new class that inherits from the `AntennaSystem` abstract base class. Implement the required methods to define the behavior of your antenna system.
   Be advise that the `AntennaSystem` class implements a context manager, so you can use it with the `with` statement to ensure proper resource management.
 

2. **Implement Required Methods and constructor**
   
   - Override the constructor in your custom class:
     - `__init__`: Initialize the antenna system and define the antennas list base on your requirements.
     
   - Override the following methods in your custom class:
      - `__enter__`: Initialize and start all the services needed for the antenna system.
      - `__exit__`: Stop all the services and clean up resources.
      - `set_default_antenna`: Define the default antenna to be used.
      - `_switch_antenna`: Implement the logic to switch between antennas.

### Example

Here is an example of a custom `AntennaSystem`:

```python
import logging
from antenna_system import AntennaSystem

class MyCustomAntennaSystem(AntennaSystem):
    def __init__(self):
        super().__init__()
        self.antennas = [
            self.Antenna(name="CustomAntenna1", antenna_id="1"),
            self.Antenna(name="CustomAntenna2", antenna_id="2"),
        ]

    def get_available_antennas(self) -> list[AntennaSystem.Antenna]:
        return self.antennas

    def set_default_antenna(self) -> None:
        self.set_used_antenna(self.antennas[0])
        logging.info("MyCustomAntennaSystem: Default antenna set to: %s", self.antennas[0].name)

    def get_used_antenna(self) -> AntennaSystem.Antenna:
        return self._current_antenna

    def _switch_antenna(self, antenna: AntennaSystem.Antenna):
        logging.info(f"MyCustomAntennaSystem: Switching to antenna: {antenna.name}")
        self._notify_antenna_change(antenna)
```

3. **Replace the Default `AntennaSystem`**  
   In the `antenna_manager_server.py` file, replace the default `DummyAntennaSystem` with your custom class:

   ```python
   from my_custom_antenna_system import MyCustomAntennaSystem

   antenna_system = MyCustomAntennaSystem()
   ```

## Using the Application

### Running the Application directly
1. **Install Dependencies**  
   Create a virtual environment and install the required dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run the Server**  
   Start the server with the following command:

   ```bash
   python antenna_manager_server.py
   ```

3. **Access the Web Interface**  
   Open a web browser and navigate to:

   ```
   http://localhost:8000/am-static/antenna_manager.html
   ```

   Use this page to test and control the antenna manager.

### Running the Application with docker
   Run the docker compose file with
   
   ```
   docker-compose up -d
   ```


## ESPHome Antenna System

The application includes a pre-built `AntennaSystem` for ESPHome-based devices, called `esp_home_one_relay_antenna_system`. This system integrates with ESPHome devices using MQTT to manage antennas. To use it, simply replace the default `DummyAntennaSystem` with `esp_home_one_relay_antenna_system` in `antenna_manager_server.py`:

```python
from esp_home_one_relay_antenna_system import esp_home_one_relay_antenna_system

antenna_system = esp_home_one_relay_antenna_system
```

This allows seamless integration with ESPHome devices for antenna management.
```

 