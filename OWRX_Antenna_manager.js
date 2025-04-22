// Antenna manager UI plugin for OpenWebRX+
// License: MIT

// to use this, you need reverse proxy (like nginx) which will redirect the /switch path to the backend port
Plugins.OWRX_Antenna_manager.API_URL ??= `${window.location.origin}/switch`;

// used in development
//Plugins.OWRX_Antenna_manager.API_URL = `http://localhost:8000`;

Plugins.OWRX_Antenna_manager.no_css = true;

// Init function of the plugin
Plugins.OWRX_Antenna_manager.init = function () {
    Plugins.OWRX_Antenna_manager.API_URL = Plugins.OWRX_Antenna_manager.API_URL.replace(/\/$/, '');

    function createAntennaSelector() {
        const antSection = document.createElement('div');
        antSection.classList.add('openwebrx-section');

        const antPanelLine = document.createElement('div');
        antPanelLine.classList.add('openwebrx-ant', 'openwebrx-panel-line');
        antSection.appendChild(antPanelLine);

        const antGrid = document.createElement('div');
        antGrid.classList.add('openwebrx-ant-grid');
        antPanelLine.appendChild(antGrid);

        const label = document.createElement('label');
        label.setAttribute('for', 'antenna-switch');
        label.textContent = 'Select Antenna:';
        antGrid.appendChild(label);

        const select = document.createElement('select');
        select.id = 'antenna-switch';
        // const optionOff = document.createElement('option');
        // optionOff.value = 'turn_off';
        // optionOff.textContent = 'Dipole&nbsp;&nbsp;&nbsp;';
        // select.appendChild(optionOff);
        //
        // const optionOn = document.createElement('option');
        // optionOn.value = 'turn_on';
        // optionOn.textContent = 'Vertical&nbsp;&nbsp;&nbsp;';
        // select.appendChild(optionOn);

        antGrid.appendChild(select);

        // Section Divider to hide ANT panel
        const antSectionDivider = document.createElement('div');
        antSectionDivider.id = 'openwebrx-section-ant';
        antSectionDivider.classList.add('openwebrx-section-divider');
        antSectionDivider.onclick = () => UI.toggleSection(antSectionDivider);
        antSectionDivider.innerHTML = "&blacktriangledown;&nbsp;Antenna";

        // Append the container above the "openwebrx-section-modes"
        const targetElement = document.getElementById('openwebrx-section-modes');
        targetElement.parentNode.insertBefore(antSectionDivider, targetElement);
        targetElement.parentNode.insertBefore(antSection, targetElement);

        // Add event listener for the antenna switch
        select.addEventListener('change', (e) => { handleAntennaChange(e); });


    }

    async function loadAntennas() {
        try {
            // Fetch the antenna data from the server
            const response = await fetch(Plugins.OWRX_Antenna_manager.API_URL + '/getAntennas');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const antennas = await response.json();

            // Get the select element
            const selectElement = document.getElementById('antenna-switch');

            // Clear any existing options
            selectElement.innerHTML = '';

            // Populate the select element with the fetched antennas
            antennas.forEach(antenna => {
                const option = document.createElement('option');
                option.value = antenna.id;
                option.textContent = antenna.name;
                selectElement.appendChild(option);
            });
        } catch (error) {
            console.error('Error loading antennas:', error);
        }
    }

    // Function to handle antenna change
    function handleAntennaChange(event) {
        const selectedAntennaId = event.target.value;

        // Call the /setAntenna/{antenna_id} endpoint
        fetch(`${Plugins.OWRX_Antenna_manager.API_URL}/setAntenna/${selectedAntennaId}`, {
            method: 'POST',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Antenna switched return:', data);
            })
            .catch(error => {
                console.error('Error switching antenna:', error);
            });
    }

    // Function to listen for antenna events and display them
    function listenToAntennaEvents() {
        const eventSource = new EventSource(`${Plugins.OWRX_Antenna_manager.API_URL}/antennasEvents`);

        eventSource.onmessage = function (event) {
            // Parse the received message
            const eventData = JSON.parse(event.data);

            if (eventData.id) {
                const selectElement = document.getElementById('antenna-switch');
                if (selectElement.value != eventData.id) {
                    divlog(`Antenna switched to: ${eventData.name}<br>`); // log to the chat panel
                    selectElement.value = eventData.id;
                }
            }
        };

        eventSource.onerror = function (error) {
            console.error('Error with EventSource:', error);
            eventSource.close(); // Close the connection on error
        };
    }


    createAntennaSelector();
    loadAntennas();

    // Init function of the plugin
    // $(document).on('event:profile_changed', function (e, data) {
    //     console.log('profile change event: ' + data);
    // });

    $(document).ready(function () {
        listenToAntennaEvents();
    });



    return true;
};
