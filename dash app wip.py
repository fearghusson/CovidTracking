# importing libraries
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import csv
import dash
from dash import dcc
from dash import html

"""functions for state data"""
def hist_covid_state_data():
    '''func to get historic covid data by state'''
    
    url_hist = r"https://api.covidactnow.org/v2/states.timeseries.csv?apiKey=e00f7fdd626a4ac3a6531d10385bf552"

    response = requests.get(url_hist)

    # code to take the response and write it to a csv line by line
    with open('hist_state.csv', 'w') as f:
        writer = csv.writer(f)
        for line in response.iter_lines():
            writer.writerow(line.decode('utf-8').split(','))
            
            
    hist_data = pd.read_csv("hist_state.csv",index_col=[0]) # taking the csv into a df
    hist_data.dropna(how='all',inplace=True) # removing completely empty rows
    hist_data.to_csv("hist_state.csv") # saving the new df to a csv


def current_covid_state_data():
    '''function to get just current covid data by state 14 days ago'''

    state_df = pd.read_csv("hist_state.csv") #reading the csv
    last_item = state_df['date'].iloc[-14] # getting the last item in the date col
    filter_df = state_df['date'] == last_item 
    final_state_df = state_df[filter_df]
    
    final_state_df.to_csv("current_state.csv") # saving updated csv to file

    return final_state_df


hist_covid_state_data() # getting the state data

state_data_df = current_covid_state_data() # transforming the state data to be usable and storing a df


# converting the total cases and total deaths to ints first to remove the .0 at the end when converting to string later
state_data_df['actuals.cases'] = state_data_df['actuals.cases'].apply(int)
state_data_df['actuals.deaths'] = state_data_df['actuals.deaths'].apply(int)


# here im adding another col to the df, which is a string with extra infomation by state 
state_data_df['text'] = state_data_df['state']+'<br>'+\
    'Total Cases ' + state_data_df['actuals.cases'].astype(str)+ '<br>' + \
    'Total Deaths ' + state_data_df['actuals.deaths'].astype(str)


# building state map graph
fig_state = go.Figure(data=go.Choropleth(
    locations=state_data_df['state'], # Spatial coordinates
    z = state_data_df['metrics.testPositivityRatio'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "Ratio",
    text=state_data_df['text']
))

fig_state.update_layout(
    title_text = 'Ratio of Positive Tests in the Past 7 Days',
    geo_scope='usa', # limite map scope to USA
)



"""functions for US data"""
def hist_covid_us_data():
    '''func to get historic covid data by state'''
    
    url_hist = r"https://api.covidactnow.org/v2/country/US.timeseries.csv?apiKey=e00f7fdd626a4ac3a6531d10385bf552"

    response = requests.get(url_hist)

    # code to take the response and write it to a csv line by line
    with open('hist_us.csv', 'w') as f:
        writer = csv.writer(f)
        for line in response.iter_lines():
            writer.writerow(line.decode('utf-8').split(','))
            
            
    hist_data = pd.read_csv("hist_us.csv",index_col=[0]) # taking the csv into a df
    hist_data.dropna(how='all',inplace=True) # removing completely empty rows
    hist_data.to_csv("hist_us.csv") # saving the new df to a csv


def current_covid_us_data():
    '''function to get just current covid data by state 14 days ago'''

    us_df = pd.read_csv("hist_us.csv") #reading the csv
    last_item = us_df['date'].iloc[-14] # getting the last item in the date col
    filter_df = us_df['date'] == last_item 
    final_us_df = us_df[filter_df]
    
    final_us_df.to_csv("current_us.csv") # saving updated csv to file

    return final_us_df



hist_covid_us_data() # running func to get US historal data

us_df = pd.read_csv('hist_us.csv') # building df for us hist data



# building line chart for US cases
figure_us_hist = go.Figure()
figure_us_hist.add_trace(go.Scatter(x=us_df['date'],
                             y=us_df['metrics.caseDensity']))
figure_us_hist.update_layout(title='Number of cases per 100k population using a 7-day rolling average',
                      xaxis_title = 'Date',
                      yaxis_title='Cases',
                            plot_bgcolor='white')



# building a table graph for vaccines and other info
figure_vaccine = go.Figure(data=[go.Table(
    header=dict(values=['State',
                        'Complete Vaccination Ratio',
                       'ICU Bed Ratio',
                       'Case Density per 100K'],
                fill_color='lightsteelblue',
                line_color='black',
                align='left'),
    cells=dict(values=[state_data_df['state'], 
                       state_data_df['metrics.vaccinationsCompletedRatio'],
                       state_data_df['metrics.icuCapacityRatio'],
                      state_data_df['metrics.caseDensity']],
               fill_color='white',
               line_color='black',
               align='left'))
])

figure_vaccine.update_layout(title='Vaccine Completion, ICU Capacity, and Case Density Rates')



# building the dash app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.title = 'Covid Tracking WIP'
app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.Div([
            html.H1(children='Covid Tracking'),

            html.Div(children=''),

            dcc.Graph(
                id='graph1',
                figure=fig_state
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children='WIP'),

            html.Div(children=''),

            dcc.Graph(
                id='graph2',
                figure=figure_vaccine
            ),  
        ], className='six columns'),
    ], className='row'),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children=''),

        html.Div(children='''
        '''),

        dcc.Graph(
            id='graph3',
            figure=figure_us_hist
        ),  
    ], className='row'),
])



if __name__ == '__main__':
    app.run_server(debug=False) # this needs to be false for some reason


















