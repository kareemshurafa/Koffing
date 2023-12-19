

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


async function updateWidget() {
    // JSON body request format according to API
    var dataH = {hours:720, pageSize: 100, pageToken: "", location:{latitude: 51.498356, longitude: -0.176894}};

    //  Historical Data Request URL
    var historicalData = "https://airquality.googleapis.com/v1/history:lookup?key=AIzaSyD_oSOX6WnFcid5aYkNEcNIKeBQwcmzBio";



    let timeLabels =[];
    // let dateLabels = [];
    let aqiPoints =[];
    let  state = true;  
    while(state){
        await postData(historicalData, dataH, "POST").then((data) => {

                // Filter data that does not have any AQI info
                let filteredData = data.hoursInfo.filter(hourInfo => 
                    hourInfo.indexes && hourInfo.indexes.length > 0
                );
                // Get data and store in array
                timeLabels = timeLabels.concat(filteredData.map(info => new Date(info.dateTime).toLocaleString()));
                // dateLabels = dateLabels.concat(filteredData.map(info => new Date(info.dateTime).toLocaleDateString()));
                aqiPoints = aqiPoints.concat(filteredData.map(info =>info.indexes[0].aqi));
                
                // Check if JSON response is incomplete
                if('nextPageToken'  in data){
                    dataH.pageToken = data.nextPageToken;
                } else{
                    state = false;
                };
        })
    
    }
    return [aqiPoints.reverse(), timeLabels.reverse()]
}



async function aqiChart() {
    const dataObt = await updateWidget();
    const data = {
        labels: dataObt[1],
        datasets: [{
            label: 'AQI',
            data: dataObt[0],
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    };
      // Configuration options
    const config = {
        type: 'line',
        data: data,
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    },
                    // x:{
                    //     type: 'time',
                    //     time: {
                    //         parser: 'MM/DD/YYYY, h:mm:ss A', // Specify your date format here
                    //         tooltipFormat: 'll HH:mm:ss'
                    //     }
                    // }
                },
                elements: {
                    point: {
                        radius:0
                    }
                },
                plugins: {
                    tooltip: {
                    enabled: true
                    },
                decimation:{
                    enabled: true
                }
                
            }
        }
    }
    const ctx = document.getElementById('acquisitions');
    new Chart(ctx, config);
}


  // Create the chart
aqiChart();