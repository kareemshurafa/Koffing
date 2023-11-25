
// (Mozilla) function to Post data to API
async function postData(url = "", data = {}, mode) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: mode, // *GET, POST, PUT, DELETE, etc.
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data), // body data type must match "Content-Type" header
        });
        // console.log(JSON.stringify(data))
        return response.json(); // parses JSON response into native JavaScript objects
    }
async function getData(url = "") {

    const response = await fetch(url, {
        method: "GET", 
        });
        // console.log(response)
        return response; 
    }




// class CoordMapType {
//         tileSize;
//         maxZoom = 19;
//         name = "Heatmap";
//         alt = "Heatmap";
//         constructor(tileSize) {
//           this.tileSize = tileSize;
//         }
//         getTile(coord, zoom, ownerDocument) {
//           const div = ownerDocument.createElement("div");
      
//           div.innerHTML = String(coord);
//           div.style.width = this.tileSize.width + "px";
//           div.style.height = this.tileSize.height + "px";
//           div.style.fontSize = "10";
//           div.style.borderStyle = "solid";
//           div.style.borderWidth = "1px";
//           div.style.borderColor = "#AAAAAA";
//           div.style.backgroundColor = "#E5E3DF";
//           return div;
//         }
//         releaseTile(tile) {}
    // }

class CoordMapType {
        tileSize;
        maxZoom = 19;
        name = "Heatmap";
        alt = "Heatmap";
        constructor(tileSize) {
        this.tileSize = tileSize;
        }

        heatmapURl = "https://airquality.googleapis.com/v1/mapTypes/US_AQI/heatmapTiles/{zoom}/{x}/{y}?key=AIzaSyD_oSOX6WnFcid5aYkNEcNIKeBQwcmzBio"
        params = {}
        getTile(coord, zoom, ownerDocument) {
            var img = ownerDocument.createElement("img")
            this.params.zoom = zoom;
            this.params.x = coord.x;
            this.params.y = coord.y;

            this.heatmapURl = addParametersToURL(this.heatmapURl, this.params);

            getData(this.heatmapURl).then((data) => {
                // console.log(data)
                img = data;
                console.log(img);
                return img
            })
        }

        releaseTile(tile) {}
    }



//(ChatGPT) Function to add parameters to the URL
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

function initMap() {
    const constPos = { lat: 51.498356, lng: -0.176894};
    let parameters = {}
    const AQInfo_URL = "https://airquality.googleapis.com/v1/currentConditions:lookup?key={api_key}"
    parameters.api_key = "AIzaSyD_oSOX6WnFcid5aYkNEcNIKeBQwcmzBio"
    // console.log(parameters)


    let getAQInfo = addParametersToURL(AQInfo_URL, parameters);
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: constPos,
        mapTypeId: "coordinate",
        mapTypeControlOptions: {
            mapTypeIds: ["coordinate", "roadmap"],
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
        },
        });
    // Create the initial InfoWindow.
    let infoWindow = new google.maps.InfoWindow({  

        position: constPos,
    });

    var dataLoc = {location:{latitude: 51.498356, longitude: -0.176894}, extraComputations:"HEALTH_RECOMMENDATIONS"};
    postData(getAQInfo, dataLoc, "POST").then((data) => {
        const outputData = data.indexes[0];
        outputData.rec = data.healthRecommendations["lungDiseasePopulation"]

        infoWindow.setContent(JSON.stringify(outputData))
    });

    
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
            outputData.rec = data.healthRecommendations["lungDiseasePopulation"]
    
            infoWindow.setContent(JSON.stringify(outputData))
            // );
        });  
        
        infoWindow.open(map);
        });

    map.mapTypes.set("coordinate", new CoordMapType(new google.maps.Size(256, 256)));

        // map.overlayMapTypes.insertAt(0, coordMapType);

    }

window.initMap = initMap;