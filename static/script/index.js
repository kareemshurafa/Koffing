
// function to Post data to API
async function postData(url = "", data) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data), // body data type must match "Content-Type" header
        });
        console.log(JSON.stringify(data))
        return response.json(); // parses JSON response into native JavaScript objects
    }

function initMap() {
    const constPos = { lat: 51.498356, lng: -0.176894};

    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: constPos,
    });
    // Create the initial InfoWindow.
    let infoWindow = new google.maps.InfoWindow({  

        position: constPos,
    });

    var location = { latitude: 51.498356, longitude: -0.176894};
    postData("https://airquality.googleapis.com/v1/currentConditions:lookup?key=AIzaSyD_oSOX6WnFcid5aYkNEcNIKeBQwcmzBio", {location}).then((data) => {
            infoWindow.setContent(
            JSON.stringify(data),
        );
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

        const { lat, lng} = newLoc;
        const location = {
            latitude: lat,
            longitude: lng
        };

        postData("https://airquality.googleapis.com/v1/currentConditions:lookup?key=AIzaSyD_oSOX6WnFcid5aYkNEcNIKeBQwcmzBio", {location}).then((data) => {
                infoWindow.setContent(
                JSON.stringify(data),
            );
            });  
        
        
        infoWindow.open(map);
        });
    }
window.initMap = initMap;