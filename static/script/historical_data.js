// initialise AQI chart
let currChart = null;

// postData function
async function postDataHistorical(url = "", data = {}, mode) {
    try {
        const response = await fetch(url, {
            method: mode,
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });
        return response.json();
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// get current historical data
async function updateData(lat, long) {
    const dataH = {
        hours: 720, 
        pageSize: 100, 
        pageToken: "", 
        location: { latitude: lat, longitude: long }
    };

    const historicalDataUrl = 'https://airquality.googleapis.com/v1/history:lookup?key=AIzaSyD_oSOX6WnFcid5aYkNEcNIKeBQwcmzBio';

    let timeLabels = [];
    let aqiPoints = [];
    let state = true;

    while(state) {
        try {
            const data = await postDataHistorical(historicalDataUrl, dataH, "POST");

            //Filter data entries that are incomplete
            let filteredData = data.hoursInfo.filter(hourInfo => 
                hourInfo.indexes && hourInfo.indexes.length > 0
            );
            
            timeLabels = timeLabels.concat(
                filteredData.map(info => new Date(info.dateTime).toLocaleString())
            );
            aqiPoints = aqiPoints.concat(
                filteredData.map(info => info.indexes[0].aqi)
            );

            if ('nextPageToken' in data) {
                dataH.pageToken = data.nextPageToken;
            } else {
                state = false;
            }
        } catch (error) {
            console.error('Error in loop:', error);
            state = false;
        }
    }
    //List the datapoints in from earliest to latest
    return [aqiPoints.reverse(), timeLabels.reverse()];
}

// Exporting aqiChart as an ES6 module
export async function aqiChart(lat, long) {
    //Format according to Chart.JS spec

    if(!currChart){
        const config = {
            type: 'line',
            data: {
                labels: 'Loading',
                datasets: [{
                    label: 'Historical Data is Loading... Please Wait',
                    data: [],
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                scales: {
                    y: { beginAtZero: true,
                        max: 100
                    }, 
                },
                elements: { point: { radius: 0 } },
                plugins: {
                    tooltip: { enabled: true },
                    decimation: { enabled: true },
                    annotation: {
                        annotations: {
                            line: {
                                type: 'line',
                                // label: {
                                //     // backgroundColor: 'red',
                                //     // content: 'Unhealthy',
                                //     display: true
                                // },
                                yMin: 60,
                                yMax: 60,
                                borderWidth: 3,
                                borderColor: 'red',
                                position:{
                                    x:0,
                                    y:0
                                }
                            }
                        }
                    }
                }
            }
        };
        const ctx = document.getElementById('acquisitions');
        currChart = new Chart(ctx, config);   
    } else {
        // Clear the chart data before replotting
        currChart.data.labels = []; // Clear the labels
        currChart.data.datasets.forEach((dataset) => {
            dataset.data = []; // Clear the data points
            dataset.label = 'Historical Data is Loading... Please Wait';
        });
        currChart.update();
    };

    const [aqiPoints, timeLabels] = await updateData(lat, long);
    
    // Update the chart with the new data
    currChart.data.labels = timeLabels; // Set the new labels
    currChart.data.datasets.forEach((dataset) => {
        dataset.data = aqiPoints; // Set the new data points
        dataset.label = 'Air Quality Index'; // Update the label
    });
    currChart.update();
    

    
    return currChart
}