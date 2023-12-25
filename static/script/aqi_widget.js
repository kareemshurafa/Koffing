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
            return response.json();
        }

var dataLoc = {location:{latitude: 51.498356, longitude: -0.176894}, extraComputations:"HEALTH_RECOMMENDATIONS"};

const AQInfo_URL = "https://airquality.googleapis.com/v1/currentConditions:lookup?key=AIzaSyD_oSOX6WnFcid5aYkNEcNIKeBQwcmzBio";
var locationFinder = "https://maps.googleapis.com/maps/api/geocode/json?latlng=51.498356,-0.176894&key=AIzaSyD_oSOX6WnFcid5aYkNEcNIKeBQwcmzBio"

  // Replace with the actual AQI data
//   var aqiData = {
//     "dateTime": "2023-12-12T20:40:00Z",
//     "regionCode": "US",
//     "indexes": [
//         {
//             "type": "Hazardous",
//             "value": 0,
//             "trend": "up"
//         }
//     ],
//     "location": "Tahoe Keys Beach"
// };

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

function updateWidget() {
    postData(AQInfo_URL, dataLoc, "POST").then((data) => {
        var widget = document.getElementById('aqiWidget');
        var aqiValue = data.indexes[0].aqi;
        
        widget.style.backgroundColor = getAqiColor(aqiValue);
        
        document.getElementById('aqiLevel').innerText = data.indexes[0].category;
        document.getElementById('aqiValue').innerText = aqiValue;
        // document.getElementById('aqiLocation').innerText = aqiData.location;
        document.getElementById('aqiUpdateTime').innerText = `Updated ${new Date(data.dateTime).toLocaleTimeString()}`;
    })
    getData(locationFinder).then((data) => {

        document.getElementById('aqiLocation').innerText = data.results[0].address_components[2].long_name;
        // console.log(data.results[0].address_components[2].long_name)
        
    })

}

updateWidget();