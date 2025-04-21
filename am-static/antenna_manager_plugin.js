// Antenna manager UI plugin for OpenWebRX+
// License: MIT

Plugins.antenna_manager_plugin.API_URL ??= `${window.location.origin}/switch`;

Plugins.antenna_manager_plugin.no_css = true;

// Init function of the plugin
Plugins.antenna_manager_plugin.init = function () {


    function loadScript(url, callback) {
        const script = document.createElement('script');
        script.src = url;
        script.type = 'text/javascript';
        script.async = true;

        // Optional: Execute a callback function once the script is loaded
        script.onload = () => {
            console.log(`Script loaded: ${url}`);
            if (callback) callback();
        };

        script.onerror = () => {
            console.error(`Failed to load script: ${url}`);
        };

        document.head.appendChild(script);
    }


    // Load the antenna_manager_client.js file
    loadScript(`http://192.168.1.32:8000/am-static/antenna_manager_client.js`, () => {
        console.log('antenna_manager_client.js loaded successfully');
        // Initialize the plugin after the client script is loaded

    });


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
        // select.addEventListener('change', function() {
        //     const state = this.value;
        //     fetch(`${Plugins.antenna_switcher.API_URL}/${state}`, { method: 'POST' })
        //         .then(response => response.json())
        //         .then(data => console.log(data))
        //         .catch(error => console.error('Error:', error));
        // });
    }

    createAntennaSelector();

// Init function of the plugin
    $(document).on('event:profile_changed', function (e, data) {
        console.log('profile change event: ' + data);
    });

    // $(document).on('DOMContentLoaded', function (e, data) {
    //     loadAntennas();
    // });



    return true;
};