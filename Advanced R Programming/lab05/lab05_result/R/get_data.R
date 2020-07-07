#' Get current and forecasted weather data for a specified city
#'
#' This function requires a character of a city and optionally a forecast horizon to return a list with
#' geographical information about the city, data about the current weather and if specified also detailed
#' information for the forecasted time periode.
#'
#' @param city a character of the city for that weather needs to be fetched
#' @param forecast_horizon An integer between 0 and 7 to specify the maximum forecast horizon in days.
#' @param api_key a character of a valid 'Apixu' API key. If FALSE, the function uses the included standard API key.
#'
#' @return a list containing three main parts: 1) metaData: geographical information of the city,
#' 2) current: current weather information, 3) forecast: forecast weather information
#'
#' @export
#' @importFrom jsonlite fromJSON
#' @importFrom RCurl url.exists
#'
#' @examples get_data("Bangalore", 1)
#'
get_data <- function(city, forecast_horizon = 0, api_key = FALSE){

  # checking input
    # input_ciy
    if (!is.character(city)) stop("'city' should be a character.")

    # forecast_horizon
    if (!is.numeric(forecast_horizon) | !forecast_horizon %in% seq(0,7)) {
      stop("'forecast_horizon' should be of class numeric with a value within the range 0 to 7.")
    }

    # api_key
    if (isFALSE(api_key)) {
      api_key = "defd42234deb45f194a112828182609"
    } else {
      api_key = as.character(api_key)
      while (isFALSE(RCurl::url.exists(paste("http://api.apixu.com/v1/forecast.json?key=",
                                               api_key,
                                               "&q=Bremen",
                                               sep = "")))) {
        api_key = readline("The API key you specified is not valid. Insert a valid API key WITHOUT quotes. : ")
      }
    }

  # executing api request - returning json_data
  url = paste("http://api.apixu.com/v1/forecast.json?key=", api_key, "&q=", city, "&days=", forecast_horizon,
              sep = "")
  data_json = jsonlite::fromJSON(url)

  # transforming json_data to returnObject
  weatherObject = list(
    # metaData including information about the location
    metaData = list(name = data_json$location$name,
                    country = data_json$location$country,
                    latitude = data_json$location$lat,
                    longitude = data_json$location$lon),
    # current including current weather information
    current = list(currentTempC = data_json$current$temp_c,
                   currentWindKph = data_json$current$wind_kph,
                   currentHumidity = data_json$current$humidity,
                   currentCondition = data_json$current$condition$text),
    # forecast including forecast weather information
    forecast = setNames(
      as.data.frame(
        cbind(
          data_json$forecast$forecastday$date,
          data_json$forecast$forecastday$day$maxtemp_c,
          data_json$forecast$forecastday$day$mintemp_c,
          data_json$forecast$forecastday$day$avgtemp_c,
          data_json$forecast$forecastday$day$maxwind_kph,
          data_json$forecast$forecastday$day$avghumidity,
          data_json$forecast$forecastday$day$condition$text
        )
      ),
      c("date", "maxTempC", "minTempC", "avgTempC", "maxWindKph", "avgHumidity", "dayCondition")
    )
  )

  # returning returnObject
  return(weatherObject)
}
