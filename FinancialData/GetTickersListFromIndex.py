import pandas as pd

#A ticker (AKA Symbol) is the identifying code used in the trading market for a particular company (ex. AAPL for Apple).
#This code automates the retrieval of a list of tickers given a particular trading index.
#It does so by scraping the index's page on Yahoo Finance, which contains a table of companies with a 'Symbol' column.



#Given an index, return a list of tickers of all companies in that index
def GetTickersListFromIndex(index):

    #Store each table from Wikipedia article in a list of dataframes
    url = GetIndexUrl(index)
    tables = pd.read_html(url)
    
    #The html page may have many tables. We only want the one containing the ticker symbols
    #This line gets the table index (i) and the column name that contains the symbols
    (i,colName) = FindTickersColumn(tables)

    #We now know the table and column name containing the tickers. Grab this column's values and return it as a list
    return((tables[i][colName].values))



IndexUrlCode = {
    'DAX' : 'GDAXI',
    'MDAX' : 'MDAXI',
    'IBEX 35' : 'IBEX'
}

def GetIndexUrl(indexName):
    yahooIndex = IndexUrlCode[indexName]    #Yahoo doesn't use the exact nomenclature in the URL, so we must manually correct it for each index (e.g. IBEX 35 -> IBEX)
    url = 'https://finance.yahoo.com/quote/%5E' + yahooIndex + '/components?p=%5E' + yahooIndex
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
    print('WARNING: No tickers table found in Wikipedia article')