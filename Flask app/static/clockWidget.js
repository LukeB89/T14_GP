//define ip address of flask server - placeholder
var host = "http://127.0.0.1:5000/";

function updateClock() {
    //update the date & time information in the clock widget

    //create a date object with the current timestamp
    var date = new Date();

    //get day/mon/year/hour/min variables from date object
    var hour = date.getHours();
    var min = date.getMinutes();
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();

    //ensure hours & minutes displayed as double-digits
    if (hour < 10) {
        hour = "0" + hour;
    }
    if (min < 10) {
        min = "0" + min;
    }

    //write variables to page
    document.getElementById("clock-date").innerText = day + "/" + month + "/" + year;
    document.getElementById("clock-time").innerText = hour + ":" + min;
}

function updateWeather(gifsPath) {
    // updates the weather information displayed in the clock widget
    fetch("/get_weather_dublin", {mode: "cors", method: "GET",})
        .then(response => response.json())
        //.then(body => console.log(body))
        .then(
            function(body) {
                var weatherInfo = body;
                document.getElementById("clock-weatherDescription").innerText = weatherInfo.weather_description;
                document.getElementById("clock-weatherImg").src = "http://openweathermap.org/img/wn/" + weatherInfo.weather_icon + "@2x.png";
                document.getElementById("clock-weatherImg").alt = weatherInfo.weather_description + "image failed to load";
                document.getElementById("clock-temp").innerText = Number((weatherInfo.main_temp - 273.15).toFixed(2)) + " C\xB0";

                updateWeatherGif(gifsPath, weatherInfo.weather_main);
            })
        .catch(
            function(error) {
                console.log('Request failed', error);
        });
}

function updateWeatherGif(gifsPath, weather) {
    // updates the background image of the clock widget to reflect the current weather conditions
    var clock = document.getElementById("clockWidget");

    if (clock.style.backgroundImage.src !== (gifsPath + backgroundImages[weather])) {
        var url = gifsPath + backgroundImages[weather];
        clock.setAttribute("style", "background-image: url("+ url +");");
        clock.setAttribute("alt", weather);
    } else {
    }
}

function weatherAlert() {
    // displays a welcome alert message based on the predicted weather for the near future
}

//create a dictionary-like object to match weather types to background image urls
var backgroundImages = new Object;
backgroundImages["Thunderstorm"] = "thunder1.gif";
backgroundImages["Drizzle"] = "drizzle1.gif";
backgroundImages["Snow"] = "default_weather.gif";
backgroundImages["Mist"] = "default_weather.gif";
backgroundImages["Smoke"] = "default_weather.gif";
backgroundImages["Haze"] = "default_weather.gif";
backgroundImages["Dust"] = "default_weather.gif";
backgroundImages["Fog"] = "default_weather.gif";
backgroundImages["Sand"] = "default_weather.gif";
backgroundImages["Ash"] = "default_weather.gif";
backgroundImages["Squall"] = "default_weather.gif";
backgroundImages["Tornado"] = "default_weather.gif";
backgroundImages["Clear"] = "clear1.gif";
backgroundImages["Clouds"] = "clouds1.gif";
backgroundImages["Rain"] = "rain2.gif";

//create a dictionary-like object to match weather prediction types to alert messages
var alertMessages = new Object;
alertMessages["Rain"] = "Looks like it's going to be wet... Don't forget your umbrella!";