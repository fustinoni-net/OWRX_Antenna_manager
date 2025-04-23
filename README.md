# OWRX-_Antenna_manager
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
