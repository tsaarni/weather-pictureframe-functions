
# Weather picture-frame

Generates image for a digital picture frame to display the current time and weather information.


## Deploy 

Create `.env.yaml` and store [OpenWeatherMap](https://openweathermap.org/) API settings in the file:

    OW_LOCATION: city,countrycode
    OW_APIKEY: SECRET


Deploy function to Google Cloud Functions by running

    gcloud functions deploy image_get2 --env-vars-file .env.yaml --runtime python37 --trigger-http


## Credits

* Weathericons font from https://erikflowers.github.io/weather-icons/
* OpenSans font from https://fonts.google.com/
