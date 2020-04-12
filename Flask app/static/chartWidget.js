// define the colours to use when drawing & filling charts & graphs
var borderColours = ["rgb(64, 204, 219)", "rgb(184, 202, 204)"];
var fillColours = ["rgba(64, 204, 219, 0.8)", "rgba(184, 202, 204, 0.5)"];

// an object for holding the predication data returned from the server for the currently selected stationId
var stationPredictionData = {};

// holds the numeric representation [0-6] for the current weekday displayed in the "bikesByDay" chart
// initialises to the current weekday
var dayNum = new Date().getDay() - 1;
if(dayNum<0){
    dayNum = 6;
}


// extend chart type "line" to include a vertical line denoting current hour/day/etc
// source: https://stackoverflow.com/questions/30256695/chart-js-drawing-an-arbitrary-vertical-line

Chart.defaults.lineCustom = Chart.defaults.line;
var myChart = Chart.controllers.line.extend({
    draw: function({arguments}) {
        // call the superclass draw function
        Chart.controllers.line.prototype.draw.apply(this, arguments);

        console.log(this.chart.options);

        /*
        // get the value showing which hour of the day to highlight
        var point = this._data[0][this.chart.options.lineAtIndex];
        var scale = this.scale;

        // draw line
        this.chart.ctx.beginPath();
        this.chart.ctx.moveTo(point.x, scale.startPoint + 24);
        this.chart.ctx.strokeStyle = '#ff0000';
        this.chart.ctx.lineTo(point.x, scale.endPoint);
        this.chart.ctx.stroke();

        // write TODAY
        this.chart.ctx.textAlign = 'center';
        this.chart.ctx.fillText("TODAY", point.x, scale.startPoint + 12);
        */
    }
});

Chart.controllers.linecustom = myChart;


function createChart(elemId, chartType, showLegend, labels, dataPoints, dataLabels,  borderColours, fillColours) {
    // creates a chartJS stacked-line-graph with a categorical x-axis in the passed html <canvas id=[elemId]> element
    // elemId: specifies the element Id of the container for the chart
    // labels: the labels for the x-axis categories
    // dataPoints: an array of arrays containing y co-ordinates for each line
    //          ie. [ [ line1: y1, y2, y3...], [ line2: y1, y2, y3, ...] ]
    // dataLabels: an array containing the labels for each line
    // borderColours: an array containing the line/border colour for each line
    // fillColours: an array containing the fill colour beneath each line

    function DataSet(data, label, fill, fillColor, borderColor, lineTension) {
        // formats the passed data as an object w/ instance variables to be passed
        // to the Chart() object constructor
        this.label = label;
        this.fill = fill;
        this.backgroundColor = fillColor;
        this.borderColor = borderColor;
        this.lineTension = lineTension;
        this.pointRadius = 0;
        this.barPercentage = 0.95;     // sets the relative width of bars in a bar chart
        this.categoryPercentage = 1;   // sets the relative width of bars in a bar chart

        var arr = new Array();


        Object.keys(data).forEach( function(item) {
            arr.push(data[item])
        })

        this.data = arr;
    }

    // get the chart container from the info.html page
    var ctx = document.getElementById(elemId);
    var lines = [];
    for (var i = 0; i < dataLabels.length; i++) {

        // make sure that categorical datapoints are in the correct position on the x axis
        var values = [];
        for (var l = 0; l <labels.length; l++) {
            thisLabel = labels[l]
            values.push(dataPoints[i][thisLabel]);
        }
        var t = new DataSet(values, dataLabels[i], true, fillColours[i], borderColours[i], 0.1);
        lines.push(t);
    }

    var someChart = new Chart(ctx, {
            type: chartType,
            data: {
                labels: labels,
                datasets: lines
            },
            options: {
                scales: {
                    yAxes: [{
                        stacked: true,
                        display: false,
                    }],
                    xAxes: [{
                    }]
                },
                legend : {
                    display: showLegend,
                    position: "top",
                    align: "center",
                    fullWidth: true
                },
                lineAtIndex: 2
            }
    });
    return someChart;
}

function getChartData(stationId, callback) {
    // request prediction data for the passed station ID for generating graphs

    fetch("/get_station_prediction?id=" + stationId, {mode: "cors", method: "GET",})
        .then(response => response.json())
        //.then(body => console.log(body))
        .then(
            function(body) {
                stationPredictionData = body;
                console.log("Data received");
                callback();
            })
        .catch(
            function(error) {
                console.log('Request failed', error);
                return false;
        });
}

function getWeatherForecast(stationId, dayNum, callback) {
    // request weather forecast data for the passed station ID & day for generating graphs

    fetch("/get_weather_forecast?id=" + stationId +"&day=" + dayNum, {mode: "cors", method: "GET",})
        .then(response => response.json())
        //.then(body => console.log(body))
        .then(
            function(body) {
                console.log("Data received");
                callback(body);
            })
        .catch(
            function(error) {
                console.log('Request failed', error);
                return false;
        });
}

function freeBikesPie(elemId, bikes, stands) {

    console.log(bikes);
    console.log(stands);

    // get the chart container from the info.html page
    var ctx = document.getElementById(elemId);

    // define the data values & config for the chart
    var config = {
            type: "doughnut",
            data: {
                labels: [
                    "Bikes",
                    "Stands"
                ],
                datasets: [{
                    data: [bikes, stands],
                    backgroundColor: fillColours,
                    label: "Bike Availability"
                }],
            },
            options: {
                title: {
                    display: true,
                    text: "Bike Availability"
                },
                legend : {
                    display: true,
                    position: "top",
                    align: "center",
                    fullWidth: true
                }
            }
    };

    console.log(config);
    // create the doughnut chart
    var someChart = new Chart(ctx, config);
    return someChart;
}

function populateSelectOptions(dropdownId, chartName) {
    // populates the dropdown selection box corresponding to the passed dropdownId
    // with the values contained in chartName.chartKeys

    // array to associate days of the week represented by the integers 0 - 6 with strings
    var days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    var dateDisp = displayDate(); 

    var selectionList = document.getElementById(dropdownId);
    options = Object.keys(stationPredictionData[chartName].dataSets);
    for (let i of options) {
        if(i == dayNum){
            document.getElementById("bikesByHourBtns").innerHTML += '<button type="button" class="btn" onclick=changeHourlyGraph(' + i + ') id="active">' + days[i] + '</button>'    
        }
        else{
            document.getElementById("bikesByHourBtns").innerHTML += '<button type="button" class="btn" onclick=changeHourlyGraph(' + i + ') id="nonactive">' + days[i] + '</button>'
        
        }
        //selectionList.innerHTML += '<option value="' + i + '" onclick=changeHourlyGraph(' + i + ') >' + i + '</option>';
    }
    document.getElementById("bikesByHourBtns").innerHTML += '<label class="switch"> <input id="showCovidDataSwitch" type="checkbox" onclick="changeHourlyGraph(dayNum)"><span class="slider"></span></label><span id="slabel"><strong>Pandemic Data</strong></span>'
    
    document.getElementById("bikesByHourBtns").innerHTML += '<div class="box-info"><h4><strong>Viewing Day</strong></h4><p id="date">' +dateDisp.getDate() + '/' + (dateDisp.getMonth()+1) + '/' + dateDisp.getFullYear() + '</p></div>'
}

function updateActiveButton(){
    var buttons = document.getElementsByClassName("btn");
    for(let btn of buttons){
        if(btn.getAttribute("id") == "active"){
            btn.setAttribute("id","nonactive")
        }
    }
    buttons[dayNum].setAttribute("id","active")
}

var icons = [ "04n","03n", "03d", "04d", "04n", "04n", "04n", "04n"];

function populateWeatherIcons(iconList) {

    // get the container for the images from the info.html page
    var ctx = document.getElementById("weatherIconsDiv");

    ctx.setAttribute("z-index", 16777271);
    ctx.style.top = "250px";

    for (let icon of iconList) {
        for (i = 0; i < 3;i++) {
            image = document.createElement("IMG");
            image.setAttribute("src", "http://openweathermap.org/img/wn/" + icon + "@2x.png");
            image.setAttribute("width", "4.3%");
            image.setAttribute("z-index", 16777271);

            ctx.appendChild(image);
        }
    }

    // remove the last child (because there's no slot for 23: - 24:00)
    ctx.removeChild(ctx.lastChild);
}

function displayDate(){
    // this code was found on stackoverflow:
    // https://stackoverflow.com/questions/12791378/get-the-most-recently-occurring-sunday
    var tempDay = dayNum +1 ;
    
    var now = new Date();
    var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    var dateToDisplay = new Date(today.setDate(today.getDate()-today.getDay()+tempDay));
    return dateToDisplay;
}

function chartMain() {

    // step 1: populate drop-down selection boxes where charts have
    // multiple dataSets (eg. 'bikesByHour')
    populateSelectOptions("weekDays", "bikesByHour");
    console.log("dayNum: " + dayNum)

    // step 3: draw charts (elemId, chartType, showLegend, labels, dataPoints, dataLabels,  borderColours, fillColours)
    hourlyChart = createChart("bikesByHour", "line", true, stationPredictionData.bikesByHour.xAxisLabels, stationPredictionData.bikesByHour.dataSets[dayNum], stationPredictionData.bikesByHour.seriesLabels, borderColours, fillColours);
    dailyChart = createChart("bikesByWeekday", "bar", false, stationPredictionData.bikesByWeekday.xAxisLabels, stationPredictionData.bikesByWeekday.dataSets.week, stationPredictionData.bikesByWeekday.seriesLabels, borderColours, fillColours);
    availabilityChart = freeBikesPie("bikeAvailability", stands[0].free_bikes, stands[0].free_stands);

    // request icons corresponding to weather forecast & display above hourly-bikes graph
    getWeatherForecast(stands[0].number, dayNum, populateWeatherIcons)
}

function changeHourlyGraph(day) {
    // remove the existing chart
    hourlyChart.destroy();

    // check if hourly prediction to be shown is for pre or post quarantine datatset
    var x = document.getElementById("showCovidDataSwitch").checked;
    if (x) {
        chartName =  "bikesByHourCovid";
    } else {
        chartName =  "bikesByHour";
    }
    
    // update dayNum var with new numeric representation of weekday
    dayNum = day;
    updateActiveButton();
    var dateDisp = displayDate();
    document.getElementById("date").innerHTML = dateDisp.getDate() + '/' + (dateDisp.getMonth() + 1) + '/' + dateDisp.getFullYear();

    // draw the new chart
    hourlyChart = createChart("bikesByHour", "line", true, stationPredictionData[chartName].xAxisLabels, stationPredictionData[chartName].dataSets[dayNum], stationPredictionData[chartName].seriesLabels, borderColours, fillColours);

    // clear existing & update weather icons forecast & display above hourly-bikes graph
    var iconBox= document.getElementById("weatherIconsDiv");
    iconBox.innerHTML = "";
    getWeatherForecast(stands[0].number, dayNum, populateWeatherIcons);
}