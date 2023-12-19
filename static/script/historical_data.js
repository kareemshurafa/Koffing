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

// JSON body request format according to API
var dataH = {hours:720, pageSize: 100, pageToken: "", location:{latitude: 51.498356, longitude: -0.176894}};

//  Historical Data Request URL
var historicalData = "https://airquality.googleapis.com/v1/history:lookup?key=AIzaSyD_oSOX6WnFcid5aYkNEcNIKeBQwcmzBio";

let timeLabels =[];
let dateLabels = [];
let aqiPoints =[];
let  state = true;

async function updateWidget() {
    while(state){
        await postData(historicalData, dataH, "POST").then((data) => {

                // Filter data that does not have any AQI info
                let filteredData = data.hoursInfo.filter(hourInfo => 
                    hourInfo.indexes && hourInfo.indexes.length > 0
                );
                // Get data and store in array
                timeLabels = timeLabels.concat(filteredData.map(info => new Date(info.dateTime).toLocaleTimeString()));
                dateLabels = dateLabels.concat(filteredData.map(info => new Date(info.dateTime).toLocaleDateString()));
                aqiPoints = aqiPoints.concat(filteredData.map(info =>info.indexes[0].aqi));
                
                // Check if JSON response is incomplete
                if('nextPageToken'  in data){
                    dataH.pageToken = data.nextPageToken;
                } else{
                    state = false;
                };
        })
    
    }
    console.log(timeLabels)
    console.log(dateLabels)
    console.log(aqiPoints)
}


updateWidget();