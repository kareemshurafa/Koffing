// GET method
async function getData(url = "") {
        const response = await fetch(url, {
            method: "GET", 
            });
            return response.json();
}

// Parse location coordinate to API
function locationFinder(lat, lng) {
    const url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${lat},${lng}&key=AIzaSyD_oSOX6WnFcid5aYkNEcNIKeBQwcmzBio`;
    return url;
}

// Change Widget Colour 
function getAqiColor(aqiValue) {
    if (aqiValue <= 20) {
        return '#75008D'; // Hazardous (Maroon)
    } else if (aqiValue <= 40) {
        return '##B40C22';// Very Unhealthy (Purple)
    } else if (aqiValue <= 60) {
        return '#FA5800'; // Unhealthy (Red)
    } else if (aqiValue <= 80) {
        return '#FDF90C'; //Moderate (Yellow)
    } else if (aqiValue <= 100) {
        return '#05b1a2'; // Excellent (Cyan)
    }
}

// Update Widget based on data given
function updateWidget(data, lat, lng) {
    var widget = document.getElementById('aqiWidget');
    var aqiValue = data.indexes[0].aqi;
    widget.style.backgroundColor = getAqiColor(aqiValue);
    document.getElementById('aqiLevel').innerText = data.indexes[0].category;
    document.getElementById('aqiValue').innerText = aqiValue;
    document.getElementById('aqiUpdateTime').innerText = `Updated ${new Date(data.dateTime).toLocaleTimeString()}`;
    getData(locationFinder(lat, lng)).then((data) => {
        document.getElementById('aqiLocation').innerText = data.results[0].address_components[2].long_name;    
    })
}