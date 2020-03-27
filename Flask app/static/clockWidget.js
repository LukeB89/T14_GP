//define ip address of flask server - placeholder
var host = "http://127.0.0.1:5000/";

function updateClock() {
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

function updateWeather() {
    fetch( host + "get_weather_dublin", {mode: "cors", method: "GET",})
        .then(response => response.json())
        //.then(body => console.log(body))
        .then(
            function(body) {
                var weatherInfo = body;
                document.getElementById("clock-weatherDescription").innerText = weatherInfo.weather_main;
                document.getElementById("clock-weatherImg").src = "http://openweathermap.org/img/wn/" + weatherInfo.weather_icon + "@2x.png";
                document.getElementById("clock-weatherImg").alt = weatherInfo.weather_main + "image failed to load";
                document.getElementById("clock-temp").innerText = Number((weatherInfo.main_temp - 273.15).toFixed(2)) + " C\xB0";

                //updateWeatherGif();
            })
        .catch(
            function(error) {
                console.log('Request failed', error);
        });
}

function updateWeatherGif() {
    var weatherGif = document.getElementById("clockWidget").style.backgroundImage;
    var currentWeather = document.getElementById("clock-weatherDescription").innerText;
    if (weatherGif != backgroundImages[currentWeather]) {
        weatherGif = backgroundImages[currentWeather];
    }
}

//create a dict object to match weather types to background image urls
var backgroundImages = new Object;
backgroundImages["Thunderstorm"] = gifsPath + "default_weather.gif";
backgroundImages["Drizzle"] = gifsPath + "default_weather.gif";
backgroundImages["Snow"] = gifsPath + "default_weather.gif";
backgroundImages["Mist"] = gifsPath + "default_weather.gif";
backgroundImages["Smoke"] = gifsPath + "default_weather.gif";
backgroundImages["Haze"] = gifsPath + "default_weather.gif";
backgroundImages["Dust"] = gifsPath + "default_weather.gif";
backgroundImages["Fog"] = gifsPath + "default_weather.gif";
backgroundImages["Sand"] = gifsPath + "default_weather.gif";
backgroundImages["Ash"] = gifsPath + "default_weather.gif";
backgroundImages["Squall"] = gifsPath + "default_weather.gif";
backgroundImages["Tornado"] = gifsPath + "default_weather.gif";
backgroundImages["Clear"] = gifsPath + "default_weather.gif";
backgroundImages["Clouds"] = gifsPath + "default_weather.gif";