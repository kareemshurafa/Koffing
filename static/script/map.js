// Import modules according to ES6 spec
import {aqiChart} from './historical_data.js'

// Get Google API Key securely
var apiKey = document.getElementById('apiKey').dataset.key;

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
        return response.json(); // parses JSON response into native JavaScript objects
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
//--End of Reference--//


// Get Air Quality Data from API
async function getAQIData(dataLoc){
    const AQInfo_URL = `https://airquality.googleapis.com/v1/currentConditions:lookup?key=${apiKey}`;
    postData(AQInfo_URL, dataLoc, "POST").then((data) => {
        updateWidget(data, dataLoc.location.latitude, dataLoc.location.longitude);
    });
    // Get Historical AQI data from import function
    aqiChart(dataLoc.location.latitude, dataLoc.location.longitude);
}

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
        //Create a heatmap according to Google Map tile
        const div = ownerDocument.createElement('div');
        const opacity = 0.45
        let heatmapURl = `https://airquality.googleapis.com/v1/mapTypes/UAQI_RED_GREEN/heatmapTiles/${zoom}/${coord.x}/${coord.y}?key=${apiKey}`;
        //Pass Heatmap tile to Google Map
        div.innerHTML = `<img style="opacity: ${opacity}"src="${heatmapURl}" alt="Air Quality Tile">`;
        return div;
    };
}


// Initialise Google Map with AQI info
async function initMap() {
    let location;

    location = { lat: 51.498356, lng: -0.176894};
    
    //Initialise map
    const map = await new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        minZoom: 3,
        maxZoom: 16,
        center: location,
        });
    
    // Create the search box and link it to the UI element.
    const input = document.getElementById("search-box");
    const searchBox = new google.maps.places.SearchBox(input);

    // Create the initial Marker.
    let marker = new google.maps.Marker({  
        position: location,
        map: map,
    });

    // Format JSON file according to API spec
    var dataLoc = {location:{latitude:location.lat, longitude: location.lng}, extraComputations:"HEALTH_RECOMMENDATIONS"};
    getAQIData(dataLoc);

    // Change map according to input on the search box
    searchBox.addListener("places_changed", () =>{
        const places = searchBox.getPlaces();
        let lat = places[0].geometry.location.lat();
        let lng = places[0].geometry.location.lng();
        map.setCenter({lat: lat, lng:lng});
        map.setZoom(15);
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
        const dataLoc = {location, extraComputations:"HEALTH_RECOMMENDATIONS"};
        getAQIData(dataLoc);
    });

    // Configure the click listener on the map.
    map.addListener("click", (mapsMouseEvent) => {
        // Removes and add new marker
        marker.setMap(null);
        marker = null;
        marker = new google.maps.Marker({
            position: mapsMouseEvent.latLng,
            map: map
        });
        map.setCenter(mapsMouseEvent.latLng);
        map.setZoom(15);
        let newLoc = mapsMouseEvent.latLng.toJSON();

        const {lat, lng} = newLoc;
        const location = {
            latitude: lat,
            longitude: lng
        };
        const dataLoc = {location, extraComputations:"HEALTH_RECOMMENDATIONS"};
        getAQIData(dataLoc);
        
    });
    
    // Air Quality Heatmap
    let airQualityOverlayVisible = true; // Initial state of heatmap (ON)
    const airQualitymap = new AirQualityHeatmap(new google.maps.Size(256, 256));
    map.overlayMapTypes.insertAt(0, airQualitymap);
    
    //Create Heatmap Toggle Button
    var toggleButton = document.createElement('button');
    toggleButton.textContent = 'Air Pollution Heatmap';
    toggleButton.classList.add('air_heatmap_button');
    toggleButton.addEventListener('click', function () {
        if (airQualityOverlayVisible) {
            // If the overlay is visible, remove it
            map.overlayMapTypes.removeAt(0);
        } else {
            // If the overlay is not visible, add it
            map.overlayMapTypes.insertAt(0, airQualitymap);
        }
        
        //Change the current state of heatmap label
        airQualityOverlayVisible = !airQualityOverlayVisible;
    });

    //Add the heatmap button to the map
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(toggleButton);
}

window.initMap = initMap;