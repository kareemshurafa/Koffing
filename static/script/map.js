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

// function getAQI

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
        let params = {};
        params.zoom = zoom;
        params.x = coord.x;
        params.y = coord.y;
        const opacity = 0.45
        let heatmapURl = "https://airquality.googleapis.com/v1/mapTypes/UAQI_INDIGO_PERSIAN/heatmapTiles/{zoom}/{x}/{y}?key=AIzaSyD_oSOX6WnFcid5aYkNEcNIKeBQwcmzBio";
        heatmapURl = addParametersToURL(heatmapURl, params);
        div.innerHTML = `<img style="opacity: ${opacity}"src="${heatmapURl}" alt="Air Quality Tile">`;
        return div;
    };
}




// Initialise Google Map with AQI info
async function initMap() {
      // Create the search box and link it to the UI element.


    const location = { lat: 51.498356, lng: -0.176894};
    const AQInfo_URL = "https://airquality.googleapis.com/v1/currentConditions:lookup?key=AIzaSyD_oSOX6WnFcid5aYkNEcNIKeBQwcmzBio";

    //Initialise map
    const map = await new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: location,
        });
    const input = document.getElementById("search-box");
    const searchBox = new google.maps.places.SearchBox(input);
    // Create the initial InfoWindow.
    let marker = new google.maps.Marker({  
        position: location,
        map: map,
    });

    
    var dataLoc = {location:{latitude: 51.498356, longitude: -0.176894}, extraComputations:"HEALTH_RECOMMENDATIONS"};

    postData(AQInfo_URL, dataLoc, "POST").then((data) => {
        // const outputData = data.indexes[0];
        // outputData.rec = data.healthRecommendations["lungDiseasePopulation"];
        // infoWindow.setContent(JSON.stringify(outputData));        
        updateWidget(data, location.lat, location.lng);
    });
    // Get Historical AQI data from import function
    aqiChart(location.lat, location.lng);



    searchBox.addListener("places_changed", () =>{
        const places = searchBox.getPlaces();
        let lat = places[0].geometry.location.lat();
        let lng = places[0].geometry.location.lng();
        map.setCenter({lat: lat, lng:lng});
        // Removes and add new marker
        marker.setMap(null);
        marker = null;
        marker = new google.maps.Marker({
            position: { lat: lat, lng: lng},
            map: map,
        });
        const location = {
            latitude: lat,
            longitude: lng
        };
        
        // const extraComputations = "HEALTH_RECOMMENDATIONS";
        const dataLoc = {location, extraComputations:"HEALTH_RECOMMENDATIONS"};
        postData(AQInfo_URL, dataLoc,"POST").then((data) => {
            const outputData = data.indexes[0];
            // outputData.rec = data.healthRecommendations["lungDiseasePopulation"];
            // infoWindow.setContent(JSON.stringify(outputData));
            updateWidget(data, location.latitude, location.longitude);
        });
        
        // infoWindow.open(map);
        aqiChart(location.latitude, location.longitude);        
    });
    // Configure the click listener.
    map.addListener("click", (mapsMouseEvent) => {
        // Removes and add new marker
        marker.setMap(null);
        marker = null;
        marker = new google.maps.Marker({
            position: mapsMouseEvent.latLng,
            map: map
        });
        
        let newLoc = mapsMouseEvent.latLng.toJSON();

        const {lat, lng} = newLoc;
        const location = {
            latitude: lat,
            longitude: lng
        };
        
        // const extraComputations = "HEALTH_RECOMMENDATIONS";
        const dataLoc = {location, extraComputations:"HEALTH_RECOMMENDATIONS"};
        postData(AQInfo_URL, dataLoc,"POST").then((data) => {
            const outputData = data.indexes[0];
            updateWidget(data, location.latitude, location.longitude);
        });
        
        // infoWindow.open(map);
        aqiChart(location.latitude, location.longitude);
        });
        
        

    let airQualityOverlayVisible = true; // Initial state of heatmap (ON)
    const airQualitymap = new AirQualityHeatmap(new google.maps.Size(256, 256));
    map.overlayMapTypes.insertAt(0, airQualitymap);
    
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