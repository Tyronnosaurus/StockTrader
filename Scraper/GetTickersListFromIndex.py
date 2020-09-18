import pandas as pd

#A ticker (AKA Symbol) is the identifying code used in the trading market for a particular company (ex. AAPL for Apple).
#This code automates the retrieval of a list of tickers given a particular trading index.
#It does so by scraping the index's page on Yahoo Finance, which contains a table of companies with a 'Symbol' column.


yahooConversion = {
    'DAX':'DAXI',
    'MDAX':'MDAXI',
    'IBEX':'IBEX'
}


#Given an index, return a list of tickers of all companies in that index
def GetTickersListFromIndex(index):

    #Store each html table from the page in a list of dataframes
    url = GetIndexUrl('^' + index)
    tables = pd.read_html(url)
    
    #The html page may have many tables. We only want the one containing the ticker symbols
    #This line gets the table index (i) and the column name that contains the symbols
    #(i,colName) = FindTickersColumn(tables)
    (i, colName) = (0, 'Symbol') #Yahoo Finance always uses same html format so we can hardcode these values

    #We now know the table and column name containing the tickers. Grab this column's values as a list
    tickersList = (tables[i][colName].values).tolist()

    #Remove tickers that have no data and cause warnings
    for delisted in ['SAZ.DE', 'MEO.DE']:
       if delisted in tickersList: tickersList.remove(delisted)

    return(tickersList)



def GetIndexUrl(indexName):  
    url = 'https://finance.yahoo.com/quote/' + indexName + '/components?p=' + indexName
    return(url)



def FindTickersColumn(tables):
    #Iterate through each table in the html page
    for i, table in enumerate(tables):
        #Inside the table, iterate through its column names (to find one that has 'ticker' in the name)
        columns = table.columns.values.tolist()
        for colName in columns:
            goodColName = str(colName).lower()  #Nameless columns get assigned an int as a name and must be converted to string. Also make it case-insensitive
            if('symbol' in goodColName): return(i,colName)    #Found the Symbol/Ticker column -> Return index of table in webpage, and name of column

    #Nothing found -> Return warning
    print('WARNING: No tickers table found in page')