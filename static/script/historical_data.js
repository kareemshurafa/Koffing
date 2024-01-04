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
    const [aqiPoints, timeLabels] = await updateData(lat, long);
    
    //Format according to Chart.JS spec
    const data = {
        labels: timeLabels,
        datasets: [{
            label: 'AQI',
            data: aqiPoints,
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    };

    
    //Format according to Chart.JS spec
    const config = {
        type: 'line',
        data: data,
        options: {
            scales: {
                y: { beginAtZero: true,
                    max: 100
                },
                // Uncomment and configure x-axis if needed
            },
            elements: { point: { radius: 0 } },
            plugins: {
                tooltip: { enabled: true },
                decimation: { enabled: true }
            }
        }
    };

    const ctx = document.getElementById('acquisitions');

    //Check if there is chart output in Client-side
    if (currChart){
        currChart.data.labels = data.labels;
        currChart.data.datasets = data.datasets;
        currChart.update('none');
    } else{
        currChart = new Chart(ctx, config);
    }
    
    return currChart
}