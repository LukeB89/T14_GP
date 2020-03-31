//define ip address of flask server - placeholder
var host = "http://127.0.0.1:5000/";

var times = ["05.00", "06.00", "07.00","08.00", "09.00", "10.00", "11.00", "12.00", "13.00", "14.00", "15.00", "16.00", "17.00", "18.00", "19.00", "20.00", "21.00", "22.00", "23.00", "24.00"];
var freeStands = [15, 34, 45, 56, 67, 45 , 1, 34, 78, 5, 15, 34, 45, 56, 67, 45 , 1 ,34, 78, 5];
var freeBikes = [75, 56, 45, 34, 23, 45, 89, 56, 12, 85, 75, 56, 45, 34, 23, 45, 89, 56, 12, 85];
var borderColours = ["rgb(64, 204, 219)", "rgb(184, 202, 204)"];
var fillColours = ["rgba(64, 204, 219, 0.8)", "rgba(184, 202, 204, 0.5)"];

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
        this.data = data;
        this.fill = fill;
        this.backgroundColor = fillColor;
        this.borderColor = borderColor;
        this.lineTension = lineTension;
        this.pointRadius = 0;
    }

    // get the chart container from the info.html page
    var ctx = document.getElementById(elemId);

    lines = [];
    for (var i = 0; i < dataPoints.length; i++) {
        var t = new DataSet(dataPoints[i], dataLabels[i], true, fillColours[i], borderColours[i], 0.1);
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
                }
            }
    });
}

function getChartData(stationId) {
    // request prediction data for the passed station ID for generating graphs

    fetch( host + "get_station_prediction?id=" + stationId, {mode: "cors", method: "GET",})
        .then(response => response.json())
        //.then(body => console.log(body))
        .then(
            function(body) {
                createChart("bikesByDay", body.labels, body.dataSeries, body.seriesLabels, borderColours, fillColours);
            })
        .catch(
            function(error) {
                console.log('Request failed', error);
        });
}

getChartData(25);

//createChart("bikesByDay", times, [freeStands, freeBikes], ["Free Stands", "Free Bikes"], borderColours, fillColours)

/*
var originalDraw = Chart.controllers.line.prototype.draw;
Chart.controllers.line.prototype.draw = function (ease) {
    originalDraw.call(this, ease);

    var point = dataValues[vm.incomeCentile];
    var scale = this.chart.scales['x-axis-0'];

    // calculate the portion of the axis and multiply by total axis width
    var left = (point.x / scale.end * (scale.right - scale.left));

    // draw line
    this.chart.chart.ctx.beginPath();
    this.chart.chart.ctx.strokeStyle = '#ff0000';
    this.chart.chart.ctx.moveTo(scale.left + left, 0);
    this.chart.chart.ctx.lineTo(scale.left + left, 1000000);
    this.chart.chart.ctx.stroke();

    // write label
    this.chart.chart.ctx.textAlign = 'center';
    this.chart.chart.ctx.fillText('YOU', scale.left + left, 200);
};
*/