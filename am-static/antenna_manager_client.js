// Function to fetch antennas and populate the select element
async function loadAntennas() {
    try {
        // Fetch the antenna data from the server
        const response = await fetch('/getAntennas');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const antennas = await response.json();

        // Get the select element
        const selectElement = document.getElementById('am-antenna-switch');

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

    // Call the /setAntenna endpoint with antenna_id in the request body
    fetch('/setAntenna', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ antenna_id: selectedAntennaId }),
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
    const eventSource = new EventSource('/antennasEvents');
    const eventsDiv = document.getElementById('am-antennas-events');
    const selectElement = document.getElementById('am-antenna-switch');

    eventSource.onmessage = function(event) {
        // Parse the received message
        const eventData = JSON.parse(event.data);

        // Update the events div with the received message
        const newMessage = document.createElement('div');
        newMessage.textContent = event.data;
        eventsDiv.appendChild(newMessage);

        // Align the select element with the received antenna ID
        if (eventData.id) {
            selectElement.value = eventData.id;
        }
    };

    eventSource.onerror = function(error) {
        console.error('Error with EventSource:', error);
        eventSource.close(); // Close the connection on error
    };
}


// Call the function to load antennas when the page loads
document.addEventListener('DOMContentLoaded', loadAntennas);

// Add event listener to the select element
document.addEventListener('DOMContentLoaded', () => {
    const selectElement = document.getElementById('am-antenna-switch');
    selectElement.addEventListener('change', handleAntennaChange);
});



// Start listening to antenna events when the page loads
// document.addEventListener('DOMContentLoaded', listenToAntennaEvents);
// Pause a bit to allow the antennas to be loaded
document.addEventListener('DOMContentLoaded', () => {
    const selectElement = document.getElementById('am-antenna-switch');
    selectElement.addEventListener('change', handleAntennaChange);

    // Introduce a delay before starting to listen to antenna events
    setTimeout(() => {
        listenToAntennaEvents();
    }, 100); // Delay in milliseconds (100ms = 0.1 seconds)
});


