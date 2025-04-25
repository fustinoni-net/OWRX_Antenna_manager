# OWRX+_Antenna_manager
Antenna manager for OpenWebRX+

How to test it:

run the script antenna_manager_server.py

Open a web browser and go to the address: http://localhost:8000/am-static/antenna_manager.html


-------DRAFT------

This software is a starting point for developing an antenna manager for OpenWebRX+.

It is composed of a server and a client part.


The server part is written in Python and uses the FastAPI framework to handle the HTTP requests.
Using the SSE (Server-Sent Events) protocol, the server updates the client with the current antenna in use.

The client part is written in HTML and JavaScript and provide a html page to control the antenna manager that its usefull during the developing and testing fases and a plugin for OpenWebRX+.

What you should do to adapt this software to your needs:
1) Extend the class AntennaSystem as was done for DummyAntennaSystem to create your own antenna system.
2) In the file antenna_manager_server.py, replace the DummyAntennaSystem with your own class in the line 

```
app = AntennaManager(DummyAntennaSystem()).
```
During the test fase can be useful the page:  http://localhost:8000/am-static/antenna_manager.html


That's all ;-)

How you can use it:
1) Install the plugin in OpenWebRX+ by editing the file init.js under the directory "plugins/receiver" the location of which may vary depending on your installation. Add the lines:
``` 
    Plugins.owrx_antenna_manager_API_URL = 'the_url_of_the_server'; // Not olways necessary.
    Plugins.load('the_url_of_the_server/am-static/owrx_antenna_manager.js');
```

2) Run the server with the command after installing the dependencies in a virtual environment:
``` 
    python -m venv venv
    source venv/bin/activate
``` 
    pip install -r requirements.txt
```
    python antenna_manager_server.py
```


-------DRAFT 2------


# Customizing the Application with Your Own `AntennaSystem`

This application is designed to be flexible and allows you to create your own `AntennaSystem` to meet your specific requirements. Below, we describe how to customize the application and use it effectively.

## Creating Your Own `AntennaSystem`

To create a custom `AntennaSystem`, follow these steps:

1. **Extend the `AntennaSystem` Class**  
   Create a new class that inherits from the `AntennaSystem` abstract base class. Implement the required methods to define the behavior of your antenna system.

2. **Implement Required Methods**  
   Override the following methods in your custom class:
   - `get_available_antennas`: Return the list of available antennas.
   - `set_default_antenna`: Define the default antenna to be used.
   - `get_used_antenna`: Return the currently used antenna.
   - `_switch_antenna`: Implement the logic to switch between antennas.

### Example

Here is an example of a custom `AntennaSystem`:

```python
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

## ESPHome Antenna System

The application includes a pre-built `AntennaSystem` for ESPHome-based devices, called `esp_home_one_relay_antenna_system`. This system integrates with ESPHome devices using MQTT to manage antennas. To use it, simply replace the default `DummyAntennaSystem` with `esp_home_one_relay_antenna_system` in `antenna_manager_server.py`:

```python
from esp_home_one_relay_antenna_system import esp_home_one_relay_antenna_system

antenna_system = esp_home_one_relay_antenna_system
```

This allows seamless integration with ESPHome devices for antenna management.
```