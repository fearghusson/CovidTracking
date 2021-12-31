# Covid Tracking App
This is a basic script using dash and plotly to track different aspects of the covid 19 pandemic.
The python script gets data from the [Covid ActNow API](https://apidocs.covidactnow.org/),
reformats the data, and produces three visuals. The three visuals are a map of each US state
indicating current level of cases, a table showing the vaccination rates and ICU ben usage rates, and
a line chart showing historic levels of cases in the US. The script will also export the data sources to csv files.

Packages used: pandas, numpy, dash, plotly
