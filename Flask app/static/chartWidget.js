//define ip address of flask server - placeholder
var host = "http://127.0.0.1:5000/";

var borderColours = ["rgb(64, 204, 219)", "rgb(184, 202, 204)"];
var fillColours = ["rgba(64, 204, 219, 0.8)", "rgba(184, 202, 204, 0.5)"];

// an object for holding the predication data returned from the server for the currently selected stationId
var stationPredictionData = {};

// holds the numeric representation [0-6] for the current weekday displayed in the "bikesByDay" chart
// initialises to the current weekday
var dayNum = new Date().getDay();

/*
// extend chart type "line" to include a vertical line denoting current hour/day/etc
// source: https://stackoverflow.com/questions/30256695/chart-js-drawing-an-arbitrary-vertical-line
var originalLineController = Chart.controllers.line;
Chart.controllers.line = Chart.controllers.line.extend({
    draw: function () {
        originalLineController.prototype.draw.apply(this, arguments);

        console.log(this);

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
    }
});
*/

function createChart(elemId, labels, dataPoints, dataLabels,  borderColours, fillColours) {
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

    new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: lines
            },
            options: {
                scales: {
                    yAxes: [{
                        stacked: true,
                        display: false,
                    }]
                },
                legend : {
                    position: "left"
                },
                lineAtIndex: 2
            }
    });
}

function getChartData(stationId, callback) {
    // request prediction data for the passed station ID for generating graphs

    fetch( "get_station_prediction?id=" + stationId, {mode: "cors", method: "GET",})
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


function populateSelectOptions(dropdownId, chartName) {
    // populates the dropdown selection box corresponding to the passed dropdownId
    // with the values contained in chartName.chartKeys

    // array to associate days of the week represented by the integers 0 - 6 with strings
    var days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];

    var selectionList = document.getElementById(dropdownId);
    options = Object.keys(stationPredictionData[chartName].dataSets);
    for (let i of options) {
        document.getElementById("bikesByHourBtns").innerHTML += '<button type="button" class="btn" onclick=changeHourlyGraph(' + i + ')>' + days[i] + '</button>'
        //selectionList.innerHTML += '<option value="' + i + '" onclick=changeHourlyGraph(' + i + ') >' + i + '</option>';
    }
}


function chartMain() {

    // step 1: populate drop-down selection boxes where charts have
    // multiple dataSets (eg. 'bikesByHour')
     populateSelectOptions("weekDays", "bikesByHour");


    // step 3: draw charts (elemId, labels, dataPoints, dataLabels,  borderColours, fillColours)
    createChart("bikesByHour", stationPredictionData.bikesByHour.xAxisLabels, stationPredictionData.bikesByHour.dataSets[dayNum], stationPredictionData.bikesByHour.seriesLabels, borderColours, fillColours);
    createChart("bikesByWeekday", stationPredictionData.bikesByWeekday.xAxisLabels, stationPredictionData.bikesByWeekday.dataSets.week, stationPredictionData.bikesByWeekday.seriesLabels, borderColours, fillColours);

}

function changeHourlyGraph(day) {
    // remove the existing chart
    document.getElementById("bikesByHour").innerHTML = "";

    // check if hourly prediction to be shown is for pre or post quarantine datatset
    var x = document.getElementById("showCovidDataSwitch").checked;
    if (x) {
        chartName =  "bikesByHourCovid";
    } else {
        chartName =  "bikesByHour";
    }

    // update dayNum var with new numeric representation of weekday
    dayNum = day;

    // draw the new chart
    createChart("bikesByHour", stationPredictionData[chartName].xAxisLabels, stationPredictionData[chartName].dataSets[day], stationPredictionData[chartName].seriesLabels, borderColours, fillColours);
}