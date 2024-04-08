# import required libraries
import pandas as pd
from shiny import App, render, ui
import matplotlib.pyplot as plt

app_ui = ui.page_fluid(
    ui.input_date_range(
        "daterange", 
        "Date range", 
        start="2020-12-29", 
        end= '2023-03-09'
        ),  
    ui.output_plot('myplot'),
)

def server(input, output, session):
    @output
    @render.plot
    def myplot():
        
        # Read the data
        # select the data for Canada
        url = 'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/global_data/time_series_covid19_vaccine_global.csv'
        covid_df = pd.read_csv(url)

        covid_can_df = covid_df[covid_df['Country_Region']=='Canada']
        covid_can_df['Date'] = pd.to_datetime(covid_can_df['Date'])


        # If you call the data frame as `df`, then the 
        # following codes select the rows in the user 
        # selected date range
        covid_can_df = covid_can_df[covid_can_df['Date'] > pd.Timestamp(input.daterange()[0])]
        covid_can_df = covid_can_df[covid_can_df['Date'] < pd.Timestamp(input.daterange()[1])]
        
        # Create the plot using `df`
        plt.plot(covid_can_df['Date'], covid_can_df['Doses_admin'], label='Doses administered')
        plt.plot(covid_can_df['Date'], covid_can_df['People_at_least_one_dose'], label='People administered at least one dose')
        plt.title('Covid Vaccination Data Over Time')
        plt.yscale('log')
        plt.xticks(rotation=45)
        plt.grid()
        plt.legend() 

app = App(app_ui, server)