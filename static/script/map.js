// Import modules according to ES6 spec
import {aqiChart} from './historical_data.js'
// import {updateWidget} from './aqi_widget.js'
//--//

//--(Reference) Mozilla function to Post data to API--//
async function postData(url = "", data = {}, mode) {
    // Default options are marked with *
    try{
    const response = await fetch(url, {
        method: mode, // *GET, POST, PUT, DELETE, etc.
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data), // body data type must match "Content-Type" header
        });
        // console.log(JSON.stringify(data))
        return response.json(); // parses JSON response into native JavaScript objects
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
//--End of Reference--//

// Get Heatmap according to API spec
class AirQualityHeatmap{
    tileSize;
    minZoom = 0;
    maxZoom = 16;
    name = "Air Quality Heatmap";
    alt = "Heatmap";

    constructor(tileSize) {
        this.tileSize = tileSize;
    }
    getTile(coord, zoom, ownerDocument) {
        const div = ownerDocument.createElement('div');
        let heatmapURl = "https://airquality.googleapis.com/v1/mapTypes/UAQI_INDIGO_PERSIAN/heatmapTiles/{zoom}/{x}/{y}?key=AIzaSyD_oSOX6WnFcid5aYkNEcNIKeBQwcmzBio";
        let params = {};
        params.zoom = zoom;
        params.x = coord.x;
        params.y = coord.y;
        const opacity = 0.45

        heatmapURl = addParametersToURL(heatmapURl, params);
        div.innerHTML = `<img style="opacity: ${opacity}"src="${heatmapURl}" alt="Air Quality Tile">`;
        return div;
    };
}


//--(ChatGPT) Function to add parameters to the URL--//
function addParametersToURL(url, params) {
    let urlWithParams = url;

    // Replace placeholders in the URL with actual values
    for (let key in params) {
        if (params.hasOwnProperty(key)) {
        urlWithParams = urlWithParams.replace(`{${key}}`, encodeURIComponent(params[key]));
        }
    }
    return urlWithParams;
}
//--End of Reference--//


// //Map InfoWindow Widget layout
// const infoContent = '<div class="aqi-widget" id="aqiWidget">'+
// '<div class="aqi-header">AIR QUALITY</div>'+
// '<div class="aqi-level" id="aqiLevel"></div>'+
// '<div class="aqi-value" id="aqiValue"></div>'+
// '<div class="aqi-location" id="aqiLocation"></div>'+
// '<div class="aqi-update-time" id="aqiUpdateTime"></div>'+
// '</div>';


// Initialise Google Map with AQI info
async function initMap() {

    const location = { lat: 51.498356, lng: -0.176894};
    let parameters = {}
    const AQInfo_URL = "https://airquality.googleapis.com/v1/currentConditions:lookup?key={api_key}"
    parameters.api_key = "AIzaSyD_oSOX6WnFcid5aYkNEcNIKeBQwcmzBio"


    let getAQInfo = addParametersToURL(AQInfo_URL, parameters);

    //Initialise map
    const map = await new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: location,
        });

    // Create the initial InfoWindow.
    let infoWindow = new google.maps.InfoWindow({  
        // content: infoContent,
        position: location,
    });

    
    var dataLoc = {location:{latitude: 51.498356, longitude: -0.176894}, extraComputations:"HEALTH_RECOMMENDATIONS"};

    postData(getAQInfo, dataLoc, "POST").then((data) => {
        const outputData = data.indexes[0];
        outputData.rec = data.healthRecommendations["lungDiseasePopulation"];
        infoWindow.setContent(JSON.stringify(outputData));        
        updateWidget(data, location.lat, location.lng);
    });
    // Get Historical AQI data from import function
    aqiChart(location.lat, location.lng);

    
    infoWindow.open(map);
    // Configure the click listener.
    map.addListener("click", (mapsMouseEvent) => {
      // Close the current InfoWindow.
        infoWindow.close();
        // Create a new InfoWindow.
        infoWindow = new google.maps.InfoWindow({
            position: mapsMouseEvent.latLng,
        });
        let newLoc = mapsMouseEvent.latLng.toJSON();

        const {lat, lng} = newLoc;
        const location = {
            latitude: lat,
            longitude: lng
        };
        
        const extraComputations = "HEALTH_RECOMMENDATIONS";
        const dataLoc = {location, extraComputations};
        postData(getAQInfo, dataLoc,"POST").then((data) => {
            const outputData = data.indexes[0];
            outputData.rec = data.healthRecommendations["lungDiseasePopulation"];
            infoWindow.setContent(JSON.stringify(outputData));
            updateWidget(data, location.latitude, location.longitude);
        });
        
        infoWindow.open(map);
        aqiChart(location.latitude, location.longitude);
        });
        
        

    let airQualityOverlayVisible = false; // Initial state of heatmap (OFF)
    const airQualitymap = new AirQualityHeatmap(new google.maps.Size(256, 256));
    
    //Create Heatmap Toggle Button
    var toggleButton = document.createElement('button');
    toggleButton.textContent = 'Air Pollution Heatmap';
    toggleButton.addEventListener('click', function () {
        if (airQualityOverlayVisible) {
            // If the overlay is visible, remove it
            map.overlayMapTypes.removeAt(0);
        } else {
            // If the overlay is not visible, add it
            map.overlayMapTypes.insertAt(0, airQualitymap);
        }
        airQualityOverlayVisible = !airQualityOverlayVisible;
    });
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(toggleButton);
}


window.initMap = initMap;