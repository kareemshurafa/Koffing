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

// updateWidget function
async function updateWidget(lat, long) {
    const dataH = {
        hours: 720, 
        pageSize: 100, 
        pageToken: "", 
        location: { latitude: lat, longitude: long }
    };
    console.log(dataH.location.latitude)
    const historicalDataUrl = 'https://airquality.googleapis.com/v1/history:lookup?key=AIzaSyD_oSOX6WnFcid5aYkNEcNIKeBQwcmzBio';

    let timeLabels = [];
    let aqiPoints = [];
    let state = true;

    while(state) {
        try {
            const data = await postDataHistorical(historicalDataUrl, dataH, "POST");

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
    return [aqiPoints.reverse(), timeLabels.reverse()];
}

// Exporting aqiChart as an ES6 module
export async function aqiChart(lat, long) {
    const [aqiPoints, timeLabels] = await updateWidget(lat, long);

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

    const config = {
        type: 'line',
        data: data,
        options: {
            scales: {
                y: { beginAtZero: true },
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
    if (currChart){
    //     currChart.data.labels.pop();
    //     currChart.data.dataset.pop();
        currChart.data.labels = data.labels;
        currChart.data.datasets = data.datasets;
        currChart.update('none');
    } else{
        currChart = new Chart(ctx, config);
    }
    return currChart
}