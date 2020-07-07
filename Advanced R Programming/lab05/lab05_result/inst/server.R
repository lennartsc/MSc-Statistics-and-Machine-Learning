#' Server function that returns the weather information
#'
#' @param input for the server
#' @param output for server
#' @importFrom shiny renderText renderPrint
#' @importFrom rLab5 get_data
#'
#'

server <- function(input, output) {
  output$country = shiny::renderText(rLab5::get_data(input$city)$metaData$country)
  output$latitude = shiny::renderText(rLab5::get_data(input$city)$metaData$latitude)
  output$longitude = shiny::renderText(rLab5::get_data(input$city)$metaData$longitude)
  output$current = shiny::renderPrint({
    output = c()
    for(chosenParam in input$param) {
      output = cbind(output, rLab5::get_data(input$city)$current[[chosenParam]])
    }
    output = as.data.frame(output)
    colnames(output) = input$param
    print(output)
  })
  output$forecast = shiny::renderPrint({
    output = c()
    output = cbind(output, date = as.character(
      rLab5::get_data(input$city, input$forecast_horizon)$forecast$date))
    if ("currentTempC" %in% input$param) {
      output = cbind(output, maxTempC = as.character(
        rLab5::get_data(input$city, input$forecast_horizon)$forecast$maxTempC))
    }
    if ("currentWindKph" %in% input$param) {
      output = cbind(output, maxWindKph = as.character(
        rLab5::get_data(input$city, input$forecast_horizon)$forecast$maxWindKph))
    }
    if ("currentHumidity" %in% input$param) {
      output = cbind(output, avgHumidity = as.character(
        rLab5::get_data(input$city, input$forecast_horizon)$forecast$avgHumidity))
    }
    if ("currentCondition" %in% input$param) {
      output = cbind(output, dayCondition = as.character(
        rLab5::get_data(input$city, input$forecast_horizon)$forecast$dayCondition))
    }
    output = as.data.frame(output)
    print(output)
  })
}
