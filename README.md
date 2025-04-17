# FINANCE API's TO DATABASE & GRAPH
#### Video Demo: https://youtube.com/shorts/3kiPUdGGRjI?feature=share
#### Description:

#### **IMPORTANT NOTE**: Before running script, acquire your free personal API keys from [Alpha Vantage](https://www.alphavantage.co/documentation/) and paste into api key variables at the start of the script (_forexkey_ and _alumkey_).

## KEY QUESTIONS:
#### How does FOREX currency rates affect commodity prices over time?
#### Can we collect this data, store it, and display the trends over time in a graphical format?

## USE:
#### This tool will be useful for users wanting to compare any currency pair rate against certain types of historical global commodity prices (if available). This can be adjusted depending on user query in the URL.

## OVERVIEW:
#### The program in app.py is a tool that can acquire API's from <ins>Alpha Vantage</ins>(or any other API host) with an API key (acquired from Alpha Vantage).
#### There are four main parts to this application (described in more detail below).
#### This raw data is converted to a PANDAS dataframe format, the values are calculated and cleaned, the data is then uploaded into a SQL database, and then the two sets of data are plotted using seaborn and Matlibplot.
#### This app collects realtime FOREX and historical commodity data and generates a single plot. To answer the key question as to whether currency rates affect commodity prices depends on further statistical analysis (outside the scope of this project) and user judgement.
#### In this example I have chosen to compare USD to CNY against the global aluminium prices since 2020. Alternatively, a user can pick another FOREX pair and/or another commodity with an adjusted URL and user-specific API keys.

## SECTIONS:

### <ins>1. API Requests</ins>:
#### Based on AlphaVantage documentation, API data in JSON format are saved via the _requests_ module.
#### Before proceeding with functions below, the request success is checked. If a request is unsuccessful, an error is displayed.
#### The main app is on line 105 after checking the API request. It then completes the following functions:

### <ins>2. PANDAS Dataframe Creation and Data cleaning</ins>:
#### There are two functions called _forexdata_ and _alumdata_ that return ready-to-plot dataframes.
#### The JSON format raw data is converted to a PANDAS dataframe. Column types are then adjusted with functions from the PANDAS library.
#### Data from both API's is cleaned (from na values if present), and then filtered based on date.
#### For FOREX data, an average is calculated by the mean of the High and Low columns.

### <ins>3. SQL Database (sqlite3) Upload</ins>:
#### There is one function called _sqlupload_ that returns a string if successful.
#### This function makes a database called _apidata_, then creates two new tables (if they don't exist yet). The two tables are for each API request dataframe.
#### Finally the function loops through each dataframe copying the values in the date and AvgFOREX column or AlumUSD column to SQL tables, respectively. Creation with two tables for each API request data
#### The tables have two columns each, one with the date and then the value of AvgFOREX or AlumUSD.

### <ins>4. Plotting The Data </ins>:
#### There is one function called _plot_ that takes in data frames from the functions in step 2 and outputs a plot using Seaborn and Matplotlib libraries.
#### This function combines both line graphs in the same plot using two y axes (with the same x axis).
#### Additional customisations were added to make graphs more presentable and user-friendly.

## FURTHER INFORMATION:
#### _Note_: Eleven lines have been written with assistance from Chatgpt (Noted in the comments of the code).
#### _Note_: Other sources are also noted in script comments.
#### _Note_: AlphaVantage only offers 25 free API query calls per day per user.
#### _Note_: Aluminium historical API source from International Monetary Fund, Federal Reserve Bank of St. Louis via AlphaVantage. [Alpha Vantage](https://www.alphavantage.co/documentation/).

