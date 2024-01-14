// Get Google API Key securely
var apiKey = document.getElementById('apiKey').dataset.key;

// GET method
async function getData(url = "") {
    try{
        const response = await fetch(url, {
            method: "GET"
        });
        return response.json();
    }catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Parse location coordinate into Address
function locationFinder(lat, lng) {
    const url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${lat},${lng}&key=${apiKey}`;
    return url;
}

// Change Widget Colour according to current value
function getAqiColor(aqiValue) {
    if (aqiValue < 1) {
        return '#FF0000'; // Hazardous (Red)
    }else if (aqiValue >= 1 && aqiValue <= 19) {
        return '#dd3311'; // Very Unhealthy (Light Red)
    } else if (aqiValue >= 20 && aqiValue <= 39) {
        return '#FF8C00';// Unhealthy (Orange)
    } else if (aqiValue >= 40 && aqiValue <= 59) {
        return '#FFFF00'; // Moderate (Yellow)
    } else if (aqiValue >= 60 && aqiValue <= 79) {
        return '#84CF33'; // Good (Light Green)
    } else if (aqiValue >= 80 && aqiValue <= 100) {
        return '#009E3A'; // Excellent (Dark Green)
    }
}

// Update Widget based on data given
function updateWidget(data, lat, lng) {
    // Get Widget from HTML file
    var widget = document.getElementById('aqiWidget');
    var aqiValue = data.indexes[0].aqi;
    widget.style.backgroundColor = getAqiColor(aqiValue);

    //Update Widget information and elements
    document.getElementById('aqiLevel').innerText = data.indexes[0].category;
    document.getElementById('aqiValue').innerText = aqiValue;
    document.getElementById('aqiUpdateTime').innerText = `Updated ${new Date(data.dateTime).toLocaleTimeString()}`;
    document.getElementById('aqiHealthRecc').innerText = data.healthRecommendations["generalPopulation"];
    document.getElementById('aqiDomPollution').innerText = `Dominant Pollutant: ${data.indexes[0].dominantPollutant}`;

    // Get Current Location from coordinates
    getData(locationFinder(lat, lng)).then((data) => {;
        if (data.results[0].address_components[1] === undefined){
            document.getElementById('aqiLocation').innerText = data.results[0].address_components[0].long_name;
        } else {
            document.getElementById('aqiLocation').innerText = data.results[0].address_components[0].long_name.concat(", ",data.results[0].address_components[1].long_name); 
        }   
    })
}