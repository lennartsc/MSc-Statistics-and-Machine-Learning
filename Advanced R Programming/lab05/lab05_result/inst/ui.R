#' Ui function that sets the ui
#'
#' @importFrom shiny fluidPage sidebarLayout sidebarPanel textInput selectInput mainPanel sliderInput checkboxGroupInput textOutput verbatimTextOutput conditionalPanel
#'
#'

ui = shiny::fluidPage(
  shiny::sidebarLayout(
    # Inputs
    shiny::sidebarPanel(
      shiny::p(shiny::strong(shiny::textInput(inputId = "city",
                                label = "City? (Letters should be without characters)",
                                value = "Bangalore"))),
      shiny::checkboxGroupInput(inputId = "param",
                                label = "Weather parameters?",
                                choices = c("Temperature in °C" = "currentTempC",
                                            "Wind speed in km/h" = "currentWindKph",
                                            "Humidity in %" = "currentHumidity",
                                            "Condition" = "currentCondition"),
                                selected = c("currentTempC","currentWindKph","currentHumidity","currentCondition")
      ),
      shiny::checkboxInput(inputId = "forecast_flag",
                           label = "Forecast?"
      ),
      shiny::conditionalPanel(
        condition = "input.forecast_flag",
        shiny::sliderInput(inputId = "forecast_horizon",
                           label = "Number of forecasted days?",
                           min = 0,
                           max = 7,
                           value = 0
        )
      )
    ),
    # Outputs
    shiny::mainPanel(
      shiny::p(shiny::strong("Country:")),
      shiny::textOutput(outputId = "country"),
      shiny::p(shiny::strong("Latitude:")),
      shiny::textOutput(outputId = "latitude"),
      shiny::p(shiny::strong("Longitude:")),
      shiny::textOutput(outputId = "longitude"),
      shiny::p(shiny::strong("Current weather data:")),
      shiny::verbatimTextOutput(outputId = "current"),
      shiny::conditionalPanel(
        condition = "input.forecast_flag",
        shiny::p(shiny::strong("Forecasted weather data:")),
        shiny::verbatimTextOutput(outputId = "forecast")
      )
    )
  )
)
