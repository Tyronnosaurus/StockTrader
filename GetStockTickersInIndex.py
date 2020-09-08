#Currently only DAX index is implemented (hardcoded)

import pandas as pd



#Given an index, return a list of tickers of all companies in that index. A tickers (AKA Symbol) is the codename for a particular stock (ex. AAPL for Apple) 
#Scrapes Wikipedia for the info.
def GetStockTickersInIndex(index):

    #Store each table from Wikipedia article in a list of dataframes
    tables = pd.read_html('https://en.wikipedia.org/wiki/DAX')
    #print(tables)
    
    #The Wikipedia article likely had many tables. We only want the one containing the ticker symbols
    #This line gets the table index (i) and the column name that contains the tickers
    (i,colName) = FindTickersColumn(tables)

    #We now know the table and column name containing the tickers. Grab this column's values and return it as a list
    return((tables[i][colName].values))



def FindTickersColumn(tables):
    #Iterate through each table in the Wikipedia article
    for i, table in enumerate(tables):
        #Inside the table, iterate through its column names (to find one that has 'ticker' in the name)
        columns = table.columns.values.tolist()
        for colName in columns:
            goodColName = str(colName).lower()  #Nameless columns get assigned an int as a name and must be converted to string. Also make it case-insensitive
            if('ticker' in goodColName): return(i,colName)    #Found the 'Tickers' column -> Return index of table in webpage, and index of column in table

    #Nothing found -> Return warning
    print('WARNING: No tickers table found in Wikipedia article')